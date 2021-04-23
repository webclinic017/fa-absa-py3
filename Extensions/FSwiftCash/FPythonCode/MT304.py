# C:\Projects\Code\SwiftMessagingSolution_Python3\base\extensions\SwiftIntegration\Utilities\XSD\MT304.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:96afad3d20bbfe8d040a1a097fa388d9fecd10e3
# Generated 2019-11-06 16:29:02.634641 by PyXB version 1.2.6 using Python 3.7.4.final.0
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
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:7145bd64-0084-11ea-a8b3-509a4c321f2f')

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


# Atomic simple type: {http://www.w3schools.com}MT304_SequenceA_GeneralInformation_20_Type_Pattern
class MT304_SequenceA_GeneralInformation_20_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceA_GeneralInformation_20_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 3, 1)
    _Documentation = None
MT304_SequenceA_GeneralInformation_20_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT304_SequenceA_GeneralInformation_20_Type_Pattern._CF_pattern.addPattern(pattern="([^/]([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,16}[^/])")
MT304_SequenceA_GeneralInformation_20_Type_Pattern._InitializeFacetMap(MT304_SequenceA_GeneralInformation_20_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceA_GeneralInformation_20_Type_Pattern', MT304_SequenceA_GeneralInformation_20_Type_Pattern)
_module_typeBindings.MT304_SequenceA_GeneralInformation_20_Type_Pattern = MT304_SequenceA_GeneralInformation_20_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT304_SequenceA_GeneralInformation_21_Type_Pattern
class MT304_SequenceA_GeneralInformation_21_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceA_GeneralInformation_21_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 16, 1)
    _Documentation = None
MT304_SequenceA_GeneralInformation_21_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT304_SequenceA_GeneralInformation_21_Type_Pattern._CF_pattern.addPattern(pattern="([^/]([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,16}[^/])")
MT304_SequenceA_GeneralInformation_21_Type_Pattern._InitializeFacetMap(MT304_SequenceA_GeneralInformation_21_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceA_GeneralInformation_21_Type_Pattern', MT304_SequenceA_GeneralInformation_21_Type_Pattern)
_module_typeBindings.MT304_SequenceA_GeneralInformation_21_Type_Pattern = MT304_SequenceA_GeneralInformation_21_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT304_SequenceA_GeneralInformation_22A_Type_Pattern
class MT304_SequenceA_GeneralInformation_22A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceA_GeneralInformation_22A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 29, 1)
    _Documentation = None
MT304_SequenceA_GeneralInformation_22A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT304_SequenceA_GeneralInformation_22A_Type_Pattern._CF_pattern.addPattern(pattern='((AMND|CAMN|CCAN|CANC|DUPL|NEWT|CNEW))')
MT304_SequenceA_GeneralInformation_22A_Type_Pattern._InitializeFacetMap(MT304_SequenceA_GeneralInformation_22A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceA_GeneralInformation_22A_Type_Pattern', MT304_SequenceA_GeneralInformation_22A_Type_Pattern)
_module_typeBindings.MT304_SequenceA_GeneralInformation_22A_Type_Pattern = MT304_SequenceA_GeneralInformation_22A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT304_SequenceA_GeneralInformation_94A_Type_Pattern
class MT304_SequenceA_GeneralInformation_94A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceA_GeneralInformation_94A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 42, 1)
    _Documentation = None
MT304_SequenceA_GeneralInformation_94A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT304_SequenceA_GeneralInformation_94A_Type_Pattern._CF_pattern.addPattern(pattern='((AFWD|ANDF|ASET))')
MT304_SequenceA_GeneralInformation_94A_Type_Pattern._InitializeFacetMap(MT304_SequenceA_GeneralInformation_94A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceA_GeneralInformation_94A_Type_Pattern', MT304_SequenceA_GeneralInformation_94A_Type_Pattern)
_module_typeBindings.MT304_SequenceA_GeneralInformation_94A_Type_Pattern = MT304_SequenceA_GeneralInformation_94A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT304_SequenceA_GeneralInformation_17O_Type_Pattern
class MT304_SequenceA_GeneralInformation_17O_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceA_GeneralInformation_17O_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 55, 1)
    _Documentation = None
MT304_SequenceA_GeneralInformation_17O_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT304_SequenceA_GeneralInformation_17O_Type_Pattern._CF_pattern.addPattern(pattern='((N|Y))')
MT304_SequenceA_GeneralInformation_17O_Type_Pattern._InitializeFacetMap(MT304_SequenceA_GeneralInformation_17O_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceA_GeneralInformation_17O_Type_Pattern', MT304_SequenceA_GeneralInformation_17O_Type_Pattern)
_module_typeBindings.MT304_SequenceA_GeneralInformation_17O_Type_Pattern = MT304_SequenceA_GeneralInformation_17O_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT304_SequenceA_GeneralInformation_17F_Type_Pattern
class MT304_SequenceA_GeneralInformation_17F_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceA_GeneralInformation_17F_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 68, 1)
    _Documentation = None
MT304_SequenceA_GeneralInformation_17F_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT304_SequenceA_GeneralInformation_17F_Type_Pattern._CF_pattern.addPattern(pattern='((N|Y))')
MT304_SequenceA_GeneralInformation_17F_Type_Pattern._InitializeFacetMap(MT304_SequenceA_GeneralInformation_17F_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceA_GeneralInformation_17F_Type_Pattern', MT304_SequenceA_GeneralInformation_17F_Type_Pattern)
_module_typeBindings.MT304_SequenceA_GeneralInformation_17F_Type_Pattern = MT304_SequenceA_GeneralInformation_17F_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT304_SequenceA_GeneralInformation_17N_Type_Pattern
class MT304_SequenceA_GeneralInformation_17N_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceA_GeneralInformation_17N_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 81, 1)
    _Documentation = None
MT304_SequenceA_GeneralInformation_17N_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT304_SequenceA_GeneralInformation_17N_Type_Pattern._CF_pattern.addPattern(pattern='((N|Y))')
MT304_SequenceA_GeneralInformation_17N_Type_Pattern._InitializeFacetMap(MT304_SequenceA_GeneralInformation_17N_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceA_GeneralInformation_17N_Type_Pattern', MT304_SequenceA_GeneralInformation_17N_Type_Pattern)
_module_typeBindings.MT304_SequenceA_GeneralInformation_17N_Type_Pattern = MT304_SequenceA_GeneralInformation_17N_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT304_SequenceA_GeneralInformation_83A_Type_Pattern
class MT304_SequenceA_GeneralInformation_83A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceA_GeneralInformation_83A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 94, 1)
    _Documentation = None
MT304_SequenceA_GeneralInformation_83A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT304_SequenceA_GeneralInformation_83A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT304_SequenceA_GeneralInformation_83A_Type_Pattern._InitializeFacetMap(MT304_SequenceA_GeneralInformation_83A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceA_GeneralInformation_83A_Type_Pattern', MT304_SequenceA_GeneralInformation_83A_Type_Pattern)
_module_typeBindings.MT304_SequenceA_GeneralInformation_83A_Type_Pattern = MT304_SequenceA_GeneralInformation_83A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT304_SequenceA_GeneralInformation_83J_Type_Pattern
class MT304_SequenceA_GeneralInformation_83J_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceA_GeneralInformation_83J_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 107, 1)
    _Documentation = None
MT304_SequenceA_GeneralInformation_83J_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT304_SequenceA_GeneralInformation_83J_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,40}\\n?){1,5})")
MT304_SequenceA_GeneralInformation_83J_Type_Pattern._InitializeFacetMap(MT304_SequenceA_GeneralInformation_83J_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceA_GeneralInformation_83J_Type_Pattern', MT304_SequenceA_GeneralInformation_83J_Type_Pattern)
_module_typeBindings.MT304_SequenceA_GeneralInformation_83J_Type_Pattern = MT304_SequenceA_GeneralInformation_83J_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT304_SequenceA_GeneralInformation_82A_Type_Pattern
class MT304_SequenceA_GeneralInformation_82A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceA_GeneralInformation_82A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 120, 1)
    _Documentation = None
MT304_SequenceA_GeneralInformation_82A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT304_SequenceA_GeneralInformation_82A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT304_SequenceA_GeneralInformation_82A_Type_Pattern._InitializeFacetMap(MT304_SequenceA_GeneralInformation_82A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceA_GeneralInformation_82A_Type_Pattern', MT304_SequenceA_GeneralInformation_82A_Type_Pattern)
_module_typeBindings.MT304_SequenceA_GeneralInformation_82A_Type_Pattern = MT304_SequenceA_GeneralInformation_82A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT304_SequenceA_GeneralInformation_82J_Type_Pattern
class MT304_SequenceA_GeneralInformation_82J_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceA_GeneralInformation_82J_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 133, 1)
    _Documentation = None
MT304_SequenceA_GeneralInformation_82J_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT304_SequenceA_GeneralInformation_82J_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,40}\\n?){1,5})")
MT304_SequenceA_GeneralInformation_82J_Type_Pattern._InitializeFacetMap(MT304_SequenceA_GeneralInformation_82J_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceA_GeneralInformation_82J_Type_Pattern', MT304_SequenceA_GeneralInformation_82J_Type_Pattern)
_module_typeBindings.MT304_SequenceA_GeneralInformation_82J_Type_Pattern = MT304_SequenceA_GeneralInformation_82J_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT304_SequenceA_GeneralInformation_87A_Type_Pattern
class MT304_SequenceA_GeneralInformation_87A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceA_GeneralInformation_87A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 146, 1)
    _Documentation = None
MT304_SequenceA_GeneralInformation_87A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT304_SequenceA_GeneralInformation_87A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT304_SequenceA_GeneralInformation_87A_Type_Pattern._InitializeFacetMap(MT304_SequenceA_GeneralInformation_87A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceA_GeneralInformation_87A_Type_Pattern', MT304_SequenceA_GeneralInformation_87A_Type_Pattern)
_module_typeBindings.MT304_SequenceA_GeneralInformation_87A_Type_Pattern = MT304_SequenceA_GeneralInformation_87A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT304_SequenceA_GeneralInformation_87J_Type_Pattern
class MT304_SequenceA_GeneralInformation_87J_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceA_GeneralInformation_87J_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 159, 1)
    _Documentation = None
MT304_SequenceA_GeneralInformation_87J_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT304_SequenceA_GeneralInformation_87J_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,40}\\n?){1,5})")
MT304_SequenceA_GeneralInformation_87J_Type_Pattern._InitializeFacetMap(MT304_SequenceA_GeneralInformation_87J_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceA_GeneralInformation_87J_Type_Pattern', MT304_SequenceA_GeneralInformation_87J_Type_Pattern)
_module_typeBindings.MT304_SequenceA_GeneralInformation_87J_Type_Pattern = MT304_SequenceA_GeneralInformation_87J_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT304_SequenceA_GeneralInformation_81A_Type_Pattern
class MT304_SequenceA_GeneralInformation_81A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceA_GeneralInformation_81A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 172, 1)
    _Documentation = None
MT304_SequenceA_GeneralInformation_81A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT304_SequenceA_GeneralInformation_81A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT304_SequenceA_GeneralInformation_81A_Type_Pattern._InitializeFacetMap(MT304_SequenceA_GeneralInformation_81A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceA_GeneralInformation_81A_Type_Pattern', MT304_SequenceA_GeneralInformation_81A_Type_Pattern)
_module_typeBindings.MT304_SequenceA_GeneralInformation_81A_Type_Pattern = MT304_SequenceA_GeneralInformation_81A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT304_SequenceA_GeneralInformation_81D_Type_Pattern
class MT304_SequenceA_GeneralInformation_81D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceA_GeneralInformation_81D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 185, 1)
    _Documentation = None
MT304_SequenceA_GeneralInformation_81D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT304_SequenceA_GeneralInformation_81D_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT304_SequenceA_GeneralInformation_81D_Type_Pattern._InitializeFacetMap(MT304_SequenceA_GeneralInformation_81D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceA_GeneralInformation_81D_Type_Pattern', MT304_SequenceA_GeneralInformation_81D_Type_Pattern)
_module_typeBindings.MT304_SequenceA_GeneralInformation_81D_Type_Pattern = MT304_SequenceA_GeneralInformation_81D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT304_SequenceA_GeneralInformation_81J_Type_Pattern
class MT304_SequenceA_GeneralInformation_81J_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceA_GeneralInformation_81J_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 198, 1)
    _Documentation = None
MT304_SequenceA_GeneralInformation_81J_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT304_SequenceA_GeneralInformation_81J_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,40}\\n?){1,5})")
MT304_SequenceA_GeneralInformation_81J_Type_Pattern._InitializeFacetMap(MT304_SequenceA_GeneralInformation_81J_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceA_GeneralInformation_81J_Type_Pattern', MT304_SequenceA_GeneralInformation_81J_Type_Pattern)
_module_typeBindings.MT304_SequenceA_GeneralInformation_81J_Type_Pattern = MT304_SequenceA_GeneralInformation_81J_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT304_SequenceA_GeneralInformation_89A_Type_Pattern
class MT304_SequenceA_GeneralInformation_89A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceA_GeneralInformation_89A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 211, 1)
    _Documentation = None
MT304_SequenceA_GeneralInformation_89A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT304_SequenceA_GeneralInformation_89A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT304_SequenceA_GeneralInformation_89A_Type_Pattern._InitializeFacetMap(MT304_SequenceA_GeneralInformation_89A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceA_GeneralInformation_89A_Type_Pattern', MT304_SequenceA_GeneralInformation_89A_Type_Pattern)
_module_typeBindings.MT304_SequenceA_GeneralInformation_89A_Type_Pattern = MT304_SequenceA_GeneralInformation_89A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT304_SequenceA_GeneralInformation_89D_Type_Pattern
class MT304_SequenceA_GeneralInformation_89D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceA_GeneralInformation_89D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 224, 1)
    _Documentation = None
MT304_SequenceA_GeneralInformation_89D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT304_SequenceA_GeneralInformation_89D_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT304_SequenceA_GeneralInformation_89D_Type_Pattern._InitializeFacetMap(MT304_SequenceA_GeneralInformation_89D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceA_GeneralInformation_89D_Type_Pattern', MT304_SequenceA_GeneralInformation_89D_Type_Pattern)
_module_typeBindings.MT304_SequenceA_GeneralInformation_89D_Type_Pattern = MT304_SequenceA_GeneralInformation_89D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT304_SequenceA_GeneralInformation_89J_Type_Pattern
class MT304_SequenceA_GeneralInformation_89J_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceA_GeneralInformation_89J_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 237, 1)
    _Documentation = None
MT304_SequenceA_GeneralInformation_89J_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT304_SequenceA_GeneralInformation_89J_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,40}\\n?){1,5})")
MT304_SequenceA_GeneralInformation_89J_Type_Pattern._InitializeFacetMap(MT304_SequenceA_GeneralInformation_89J_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceA_GeneralInformation_89J_Type_Pattern', MT304_SequenceA_GeneralInformation_89J_Type_Pattern)
_module_typeBindings.MT304_SequenceA_GeneralInformation_89J_Type_Pattern = MT304_SequenceA_GeneralInformation_89J_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT304_SequenceA_GeneralInformation_17I_Type_Pattern
class MT304_SequenceA_GeneralInformation_17I_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceA_GeneralInformation_17I_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 250, 1)
    _Documentation = None
MT304_SequenceA_GeneralInformation_17I_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT304_SequenceA_GeneralInformation_17I_Type_Pattern._CF_pattern.addPattern(pattern='(N|[0-9])')
MT304_SequenceA_GeneralInformation_17I_Type_Pattern._InitializeFacetMap(MT304_SequenceA_GeneralInformation_17I_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceA_GeneralInformation_17I_Type_Pattern', MT304_SequenceA_GeneralInformation_17I_Type_Pattern)
_module_typeBindings.MT304_SequenceA_GeneralInformation_17I_Type_Pattern = MT304_SequenceA_GeneralInformation_17I_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT304_SequenceA_GeneralInformation_77H_Type_Pattern
class MT304_SequenceA_GeneralInformation_77H_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceA_GeneralInformation_77H_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 263, 1)
    _Documentation = None
MT304_SequenceA_GeneralInformation_77H_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT304_SequenceA_GeneralInformation_77H_Type_Pattern._CF_pattern.addPattern(pattern='((AFB|DERV|FBF|FEOMA|ICOM|IFEMA|ISDA|ISDACN|OTHER)(/[0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01]))?(//[0-9]{4})?)')
MT304_SequenceA_GeneralInformation_77H_Type_Pattern._InitializeFacetMap(MT304_SequenceA_GeneralInformation_77H_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceA_GeneralInformation_77H_Type_Pattern', MT304_SequenceA_GeneralInformation_77H_Type_Pattern)
_module_typeBindings.MT304_SequenceA_GeneralInformation_77H_Type_Pattern = MT304_SequenceA_GeneralInformation_77H_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT304_SequenceA_GeneralInformation_14C_Type_Pattern
class MT304_SequenceA_GeneralInformation_14C_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceA_GeneralInformation_14C_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 276, 1)
    _Documentation = None
MT304_SequenceA_GeneralInformation_14C_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT304_SequenceA_GeneralInformation_14C_Type_Pattern._CF_pattern.addPattern(pattern='([0-9]{4})')
MT304_SequenceA_GeneralInformation_14C_Type_Pattern._InitializeFacetMap(MT304_SequenceA_GeneralInformation_14C_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceA_GeneralInformation_14C_Type_Pattern', MT304_SequenceA_GeneralInformation_14C_Type_Pattern)
_module_typeBindings.MT304_SequenceA_GeneralInformation_14C_Type_Pattern = MT304_SequenceA_GeneralInformation_14C_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT304_SequenceA_GeneralInformation_32E_Type_Pattern
class MT304_SequenceA_GeneralInformation_32E_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceA_GeneralInformation_32E_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 289, 1)
    _Documentation = None
MT304_SequenceA_GeneralInformation_32E_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT304_SequenceA_GeneralInformation_32E_Type_Pattern._CF_pattern.addPattern(pattern='([A-Z]{3})')
MT304_SequenceA_GeneralInformation_32E_Type_Pattern._InitializeFacetMap(MT304_SequenceA_GeneralInformation_32E_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceA_GeneralInformation_32E_Type_Pattern', MT304_SequenceA_GeneralInformation_32E_Type_Pattern)
_module_typeBindings.MT304_SequenceA_GeneralInformation_32E_Type_Pattern = MT304_SequenceA_GeneralInformation_32E_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT304_SequenceA_GeneralInformation_30U_Type_Pattern
class MT304_SequenceA_GeneralInformation_30U_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceA_GeneralInformation_30U_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 302, 1)
    _Documentation = None
MT304_SequenceA_GeneralInformation_30U_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT304_SequenceA_GeneralInformation_30U_Type_Pattern._CF_pattern.addPattern(pattern='([0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01]))')
MT304_SequenceA_GeneralInformation_30U_Type_Pattern._InitializeFacetMap(MT304_SequenceA_GeneralInformation_30U_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceA_GeneralInformation_30U_Type_Pattern', MT304_SequenceA_GeneralInformation_30U_Type_Pattern)
_module_typeBindings.MT304_SequenceA_GeneralInformation_30U_Type_Pattern = MT304_SequenceA_GeneralInformation_30U_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT304_SequenceA_GeneralInformation_14S_Type_Pattern
class MT304_SequenceA_GeneralInformation_14S_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceA_GeneralInformation_14S_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 315, 1)
    _Documentation = None
MT304_SequenceA_GeneralInformation_14S_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT304_SequenceA_GeneralInformation_14S_Type_Pattern._CF_pattern.addPattern(pattern='([A-Z]{3}[0-9]{1,2}(/(0[0-9]|[1][0-9]|2[1-3])([0-5][0-9])/[A-Z0-9]{4})?)')
MT304_SequenceA_GeneralInformation_14S_Type_Pattern._InitializeFacetMap(MT304_SequenceA_GeneralInformation_14S_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceA_GeneralInformation_14S_Type_Pattern', MT304_SequenceA_GeneralInformation_14S_Type_Pattern)
_module_typeBindings.MT304_SequenceA_GeneralInformation_14S_Type_Pattern = MT304_SequenceA_GeneralInformation_14S_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT304_SequenceA_GeneralInformation_21A_Type_Pattern
class MT304_SequenceA_GeneralInformation_21A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceA_GeneralInformation_21A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 328, 1)
    _Documentation = None
MT304_SequenceA_GeneralInformation_21A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT304_SequenceA_GeneralInformation_21A_Type_Pattern._CF_pattern.addPattern(pattern="([^/]([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,16}[^/])")
MT304_SequenceA_GeneralInformation_21A_Type_Pattern._InitializeFacetMap(MT304_SequenceA_GeneralInformation_21A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceA_GeneralInformation_21A_Type_Pattern', MT304_SequenceA_GeneralInformation_21A_Type_Pattern)
_module_typeBindings.MT304_SequenceA_GeneralInformation_21A_Type_Pattern = MT304_SequenceA_GeneralInformation_21A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT304_SequenceA_GeneralInformation_14E_Type_Pattern
class MT304_SequenceA_GeneralInformation_14E_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceA_GeneralInformation_14E_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 341, 1)
    _Documentation = None
MT304_SequenceA_GeneralInformation_14E_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT304_SequenceA_GeneralInformation_14E_Type_Pattern._CF_pattern.addPattern(pattern="(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35})")
MT304_SequenceA_GeneralInformation_14E_Type_Pattern._InitializeFacetMap(MT304_SequenceA_GeneralInformation_14E_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceA_GeneralInformation_14E_Type_Pattern', MT304_SequenceA_GeneralInformation_14E_Type_Pattern)
_module_typeBindings.MT304_SequenceA_GeneralInformation_14E_Type_Pattern = MT304_SequenceA_GeneralInformation_14E_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT304_SequenceB_ForexTransactionDetails_30T_Type_Pattern
class MT304_SequenceB_ForexTransactionDetails_30T_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceB_ForexTransactionDetails_30T_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 354, 1)
    _Documentation = None
MT304_SequenceB_ForexTransactionDetails_30T_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT304_SequenceB_ForexTransactionDetails_30T_Type_Pattern._CF_pattern.addPattern(pattern='([0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01]))')
MT304_SequenceB_ForexTransactionDetails_30T_Type_Pattern._InitializeFacetMap(MT304_SequenceB_ForexTransactionDetails_30T_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceB_ForexTransactionDetails_30T_Type_Pattern', MT304_SequenceB_ForexTransactionDetails_30T_Type_Pattern)
_module_typeBindings.MT304_SequenceB_ForexTransactionDetails_30T_Type_Pattern = MT304_SequenceB_ForexTransactionDetails_30T_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT304_SequenceB_ForexTransactionDetails_30V_Type_Pattern
class MT304_SequenceB_ForexTransactionDetails_30V_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceB_ForexTransactionDetails_30V_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 367, 1)
    _Documentation = None
MT304_SequenceB_ForexTransactionDetails_30V_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT304_SequenceB_ForexTransactionDetails_30V_Type_Pattern._CF_pattern.addPattern(pattern='([0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01]))')
MT304_SequenceB_ForexTransactionDetails_30V_Type_Pattern._InitializeFacetMap(MT304_SequenceB_ForexTransactionDetails_30V_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceB_ForexTransactionDetails_30V_Type_Pattern', MT304_SequenceB_ForexTransactionDetails_30V_Type_Pattern)
_module_typeBindings.MT304_SequenceB_ForexTransactionDetails_30V_Type_Pattern = MT304_SequenceB_ForexTransactionDetails_30V_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT304_SequenceB_ForexTransactionDetails_36_Type_Pattern
class MT304_SequenceB_ForexTransactionDetails_36_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceB_ForexTransactionDetails_36_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 380, 1)
    _Documentation = None
MT304_SequenceB_ForexTransactionDetails_36_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT304_SequenceB_ForexTransactionDetails_36_Type_Pattern._CF_pattern.addPattern(pattern='([0-9,(?0-9)]{1,12})')
MT304_SequenceB_ForexTransactionDetails_36_Type_Pattern._InitializeFacetMap(MT304_SequenceB_ForexTransactionDetails_36_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceB_ForexTransactionDetails_36_Type_Pattern', MT304_SequenceB_ForexTransactionDetails_36_Type_Pattern)
_module_typeBindings.MT304_SequenceB_ForexTransactionDetails_36_Type_Pattern = MT304_SequenceB_ForexTransactionDetails_36_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT304_SequenceB_ForexTransactionDetails_39M_Type_Pattern
class MT304_SequenceB_ForexTransactionDetails_39M_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceB_ForexTransactionDetails_39M_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 393, 1)
    _Documentation = None
MT304_SequenceB_ForexTransactionDetails_39M_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT304_SequenceB_ForexTransactionDetails_39M_Type_Pattern._CF_pattern.addPattern(pattern='([A-Z]{2})')
MT304_SequenceB_ForexTransactionDetails_39M_Type_Pattern._InitializeFacetMap(MT304_SequenceB_ForexTransactionDetails_39M_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceB_ForexTransactionDetails_39M_Type_Pattern', MT304_SequenceB_ForexTransactionDetails_39M_Type_Pattern)
_module_typeBindings.MT304_SequenceB_ForexTransactionDetails_39M_Type_Pattern = MT304_SequenceB_ForexTransactionDetails_39M_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_32B_Type_Pattern
class MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_32B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_32B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 406, 1)
    _Documentation = None
MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_32B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_32B_Type_Pattern._CF_pattern.addPattern(pattern='((AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})')
MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_32B_Type_Pattern._InitializeFacetMap(MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_32B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_32B_Type_Pattern', MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_32B_Type_Pattern)
_module_typeBindings.MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_32B_Type_Pattern = MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_32B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_53A_Type_Pattern
class MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_53A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_53A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 419, 1)
    _Documentation = None
MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_53A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_53A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_53A_Type_Pattern._InitializeFacetMap(MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_53A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_53A_Type_Pattern', MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_53A_Type_Pattern)
_module_typeBindings.MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_53A_Type_Pattern = MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_53A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_53J_Type_Pattern
class MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_53J_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_53J_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 432, 1)
    _Documentation = None
MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_53J_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_53J_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,40}\\n?){1,5})")
MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_53J_Type_Pattern._InitializeFacetMap(MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_53J_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_53J_Type_Pattern', MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_53J_Type_Pattern)
_module_typeBindings.MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_53J_Type_Pattern = MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_53J_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_56A_Type_Pattern
class MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_56A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_56A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 445, 1)
    _Documentation = None
MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_56A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_56A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_56A_Type_Pattern._InitializeFacetMap(MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_56A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_56A_Type_Pattern', MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_56A_Type_Pattern)
_module_typeBindings.MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_56A_Type_Pattern = MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_56A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_56J_Type_Pattern
class MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_56J_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_56J_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 458, 1)
    _Documentation = None
MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_56J_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_56J_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,40}\\n?){1,5})")
MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_56J_Type_Pattern._InitializeFacetMap(MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_56J_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_56J_Type_Pattern', MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_56J_Type_Pattern)
_module_typeBindings.MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_56J_Type_Pattern = MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_56J_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_57A_Type_Pattern
class MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_57A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_57A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 471, 1)
    _Documentation = None
MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_57A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_57A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_57A_Type_Pattern._InitializeFacetMap(MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_57A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_57A_Type_Pattern', MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_57A_Type_Pattern)
_module_typeBindings.MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_57A_Type_Pattern = MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_57A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_57J_Type_Pattern
class MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_57J_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_57J_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 484, 1)
    _Documentation = None
MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_57J_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_57J_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,40}\\n?){1,5})")
MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_57J_Type_Pattern._InitializeFacetMap(MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_57J_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_57J_Type_Pattern', MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_57J_Type_Pattern)
_module_typeBindings.MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_57J_Type_Pattern = MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_57J_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_33B_Type_Pattern
class MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_33B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_33B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 497, 1)
    _Documentation = None
MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_33B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_33B_Type_Pattern._CF_pattern.addPattern(pattern='((AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})')
MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_33B_Type_Pattern._InitializeFacetMap(MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_33B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_33B_Type_Pattern', MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_33B_Type_Pattern)
_module_typeBindings.MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_33B_Type_Pattern = MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_33B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_53A_Type_Pattern
class MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_53A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_53A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 510, 1)
    _Documentation = None
MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_53A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_53A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_53A_Type_Pattern._InitializeFacetMap(MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_53A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_53A_Type_Pattern', MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_53A_Type_Pattern)
_module_typeBindings.MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_53A_Type_Pattern = MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_53A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_53J_Type_Pattern
class MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_53J_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_53J_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 523, 1)
    _Documentation = None
MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_53J_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_53J_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,40}\\n?){1,5})")
MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_53J_Type_Pattern._InitializeFacetMap(MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_53J_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_53J_Type_Pattern', MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_53J_Type_Pattern)
_module_typeBindings.MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_53J_Type_Pattern = MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_53J_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_56A_Type_Pattern
class MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_56A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_56A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 536, 1)
    _Documentation = None
MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_56A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_56A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_56A_Type_Pattern._InitializeFacetMap(MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_56A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_56A_Type_Pattern', MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_56A_Type_Pattern)
_module_typeBindings.MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_56A_Type_Pattern = MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_56A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_56J_Type_Pattern
class MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_56J_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_56J_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 549, 1)
    _Documentation = None
MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_56J_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_56J_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,40}\\n?){1,5})")
MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_56J_Type_Pattern._InitializeFacetMap(MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_56J_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_56J_Type_Pattern', MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_56J_Type_Pattern)
_module_typeBindings.MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_56J_Type_Pattern = MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_56J_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_57A_Type_Pattern
class MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_57A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_57A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 562, 1)
    _Documentation = None
MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_57A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_57A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_57A_Type_Pattern._InitializeFacetMap(MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_57A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_57A_Type_Pattern', MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_57A_Type_Pattern)
_module_typeBindings.MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_57A_Type_Pattern = MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_57A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_57J_Type_Pattern
class MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_57J_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_57J_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 575, 1)
    _Documentation = None
MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_57J_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_57J_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,40}\\n?){1,5})")
MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_57J_Type_Pattern._InitializeFacetMap(MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_57J_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_57J_Type_Pattern', MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_57J_Type_Pattern)
_module_typeBindings.MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_57J_Type_Pattern = MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_57J_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_58A_Type_Pattern
class MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_58A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_58A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 588, 1)
    _Documentation = None
MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_58A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_58A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_58A_Type_Pattern._InitializeFacetMap(MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_58A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_58A_Type_Pattern', MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_58A_Type_Pattern)
_module_typeBindings.MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_58A_Type_Pattern = MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_58A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_58J_Type_Pattern
class MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_58J_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_58J_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 601, 1)
    _Documentation = None
MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_58J_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_58J_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,40}\\n?){1,5})")
MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_58J_Type_Pattern._InitializeFacetMap(MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_58J_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_58J_Type_Pattern', MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_58J_Type_Pattern)
_module_typeBindings.MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_58J_Type_Pattern = MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_58J_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT304_SequenceC_OptionalGeneralInformation_21A_Type_Pattern
class MT304_SequenceC_OptionalGeneralInformation_21A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceC_OptionalGeneralInformation_21A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 614, 1)
    _Documentation = None
MT304_SequenceC_OptionalGeneralInformation_21A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT304_SequenceC_OptionalGeneralInformation_21A_Type_Pattern._CF_pattern.addPattern(pattern="([^/]([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,16}[^/])")
MT304_SequenceC_OptionalGeneralInformation_21A_Type_Pattern._InitializeFacetMap(MT304_SequenceC_OptionalGeneralInformation_21A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceC_OptionalGeneralInformation_21A_Type_Pattern', MT304_SequenceC_OptionalGeneralInformation_21A_Type_Pattern)
_module_typeBindings.MT304_SequenceC_OptionalGeneralInformation_21A_Type_Pattern = MT304_SequenceC_OptionalGeneralInformation_21A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT304_SequenceC_OptionalGeneralInformation_21G_Type_Pattern
class MT304_SequenceC_OptionalGeneralInformation_21G_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceC_OptionalGeneralInformation_21G_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 627, 1)
    _Documentation = None
MT304_SequenceC_OptionalGeneralInformation_21G_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT304_SequenceC_OptionalGeneralInformation_21G_Type_Pattern._CF_pattern.addPattern(pattern="([^/]([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,16}[^/])")
MT304_SequenceC_OptionalGeneralInformation_21G_Type_Pattern._InitializeFacetMap(MT304_SequenceC_OptionalGeneralInformation_21G_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceC_OptionalGeneralInformation_21G_Type_Pattern', MT304_SequenceC_OptionalGeneralInformation_21G_Type_Pattern)
_module_typeBindings.MT304_SequenceC_OptionalGeneralInformation_21G_Type_Pattern = MT304_SequenceC_OptionalGeneralInformation_21G_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_22L_Type_Pattern
class MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_22L_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_22L_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 640, 1)
    _Documentation = None
MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_22L_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_22L_Type_Pattern._CF_pattern.addPattern(pattern="(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35})")
MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_22L_Type_Pattern._InitializeFacetMap(MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_22L_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_22L_Type_Pattern', MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_22L_Type_Pattern)
_module_typeBindings.MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_22L_Type_Pattern = MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_22L_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_22M_Type_Pattern
class MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_22M_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_22M_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 653, 1)
    _Documentation = None
MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_22M_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_22M_Type_Pattern._CF_pattern.addPattern(pattern="(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,30})")
MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_22M_Type_Pattern._InitializeFacetMap(MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_22M_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_22M_Type_Pattern', MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_22M_Type_Pattern)
_module_typeBindings.MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_22M_Type_Pattern = MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_22M_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_22N_Type_Pattern
class MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_22N_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_22N_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 666, 1)
    _Documentation = None
MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_22N_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_22N_Type_Pattern._CF_pattern.addPattern(pattern="(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,32})")
MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_22N_Type_Pattern._InitializeFacetMap(MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_22N_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_22N_Type_Pattern', MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_22N_Type_Pattern)
_module_typeBindings.MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_22N_Type_Pattern = MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_22N_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_SubsequenceC1a_PriorUniqueTransactionIdentifier_22P_Type_Pattern
class MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_SubsequenceC1a_PriorUniqueTransactionIdentifier_22P_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_SubsequenceC1a_PriorUniqueTransactionIdentifier_22P_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 679, 1)
    _Documentation = None
MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_SubsequenceC1a_PriorUniqueTransactionIdentifier_22P_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_SubsequenceC1a_PriorUniqueTransactionIdentifier_22P_Type_Pattern._CF_pattern.addPattern(pattern="(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,30})")
MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_SubsequenceC1a_PriorUniqueTransactionIdentifier_22P_Type_Pattern._InitializeFacetMap(MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_SubsequenceC1a_PriorUniqueTransactionIdentifier_22P_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_SubsequenceC1a_PriorUniqueTransactionIdentifier_22P_Type_Pattern', MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_SubsequenceC1a_PriorUniqueTransactionIdentifier_22P_Type_Pattern)
_module_typeBindings.MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_SubsequenceC1a_PriorUniqueTransactionIdentifier_22P_Type_Pattern = MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_SubsequenceC1a_PriorUniqueTransactionIdentifier_22P_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_SubsequenceC1a_PriorUniqueTransactionIdentifier_22R_Type_Pattern
class MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_SubsequenceC1a_PriorUniqueTransactionIdentifier_22R_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_SubsequenceC1a_PriorUniqueTransactionIdentifier_22R_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 692, 1)
    _Documentation = None
MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_SubsequenceC1a_PriorUniqueTransactionIdentifier_22R_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_SubsequenceC1a_PriorUniqueTransactionIdentifier_22R_Type_Pattern._CF_pattern.addPattern(pattern="(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,32})")
MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_SubsequenceC1a_PriorUniqueTransactionIdentifier_22R_Type_Pattern._InitializeFacetMap(MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_SubsequenceC1a_PriorUniqueTransactionIdentifier_22R_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_SubsequenceC1a_PriorUniqueTransactionIdentifier_22R_Type_Pattern', MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_SubsequenceC1a_PriorUniqueTransactionIdentifier_22R_Type_Pattern)
_module_typeBindings.MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_SubsequenceC1a_PriorUniqueTransactionIdentifier_22R_Type_Pattern = MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_SubsequenceC1a_PriorUniqueTransactionIdentifier_22R_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT304_SequenceC_OptionalGeneralInformation_22U_Type_Pattern
class MT304_SequenceC_OptionalGeneralInformation_22U_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceC_OptionalGeneralInformation_22U_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 705, 1)
    _Documentation = None
MT304_SequenceC_OptionalGeneralInformation_22U_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT304_SequenceC_OptionalGeneralInformation_22U_Type_Pattern._CF_pattern.addPattern(pattern='([A-Z]{1,6})')
MT304_SequenceC_OptionalGeneralInformation_22U_Type_Pattern._InitializeFacetMap(MT304_SequenceC_OptionalGeneralInformation_22U_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceC_OptionalGeneralInformation_22U_Type_Pattern', MT304_SequenceC_OptionalGeneralInformation_22U_Type_Pattern)
_module_typeBindings.MT304_SequenceC_OptionalGeneralInformation_22U_Type_Pattern = MT304_SequenceC_OptionalGeneralInformation_22U_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT304_SequenceC_OptionalGeneralInformation_35B_Type_Pattern
class MT304_SequenceC_OptionalGeneralInformation_35B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceC_OptionalGeneralInformation_35B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 718, 1)
    _Documentation = None
MT304_SequenceC_OptionalGeneralInformation_35B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT304_SequenceC_OptionalGeneralInformation_35B_Type_Pattern._CF_pattern.addPattern(pattern="((ISIN {1}[A-Z0-9]{12})?(\\n)?((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})?)")
MT304_SequenceC_OptionalGeneralInformation_35B_Type_Pattern._InitializeFacetMap(MT304_SequenceC_OptionalGeneralInformation_35B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceC_OptionalGeneralInformation_35B_Type_Pattern', MT304_SequenceC_OptionalGeneralInformation_35B_Type_Pattern)
_module_typeBindings.MT304_SequenceC_OptionalGeneralInformation_35B_Type_Pattern = MT304_SequenceC_OptionalGeneralInformation_35B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT304_SequenceC_OptionalGeneralInformation_22V_Type_Pattern
class MT304_SequenceC_OptionalGeneralInformation_22V_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceC_OptionalGeneralInformation_22V_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 731, 1)
    _Documentation = None
MT304_SequenceC_OptionalGeneralInformation_22V_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT304_SequenceC_OptionalGeneralInformation_22V_Type_Pattern._CF_pattern.addPattern(pattern="(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35})")
MT304_SequenceC_OptionalGeneralInformation_22V_Type_Pattern._InitializeFacetMap(MT304_SequenceC_OptionalGeneralInformation_22V_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceC_OptionalGeneralInformation_22V_Type_Pattern', MT304_SequenceC_OptionalGeneralInformation_22V_Type_Pattern)
_module_typeBindings.MT304_SequenceC_OptionalGeneralInformation_22V_Type_Pattern = MT304_SequenceC_OptionalGeneralInformation_22V_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT304_SequenceC_OptionalGeneralInformation_98D_Type_Pattern
class MT304_SequenceC_OptionalGeneralInformation_98D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceC_OptionalGeneralInformation_98D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 744, 1)
    _Documentation = None
MT304_SequenceC_OptionalGeneralInformation_98D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT304_SequenceC_OptionalGeneralInformation_98D_Type_Pattern._CF_pattern.addPattern(pattern='([0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])(0[0-9]|[1][0-9]|2[1-3])([0-5][0-9])([0-5][0-9])(,[0-9]{1,3})?(/(N)?(0[0-9]|[1][0-9]|2[1-3])(([0-5][0-9]))?)?)')
MT304_SequenceC_OptionalGeneralInformation_98D_Type_Pattern._InitializeFacetMap(MT304_SequenceC_OptionalGeneralInformation_98D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceC_OptionalGeneralInformation_98D_Type_Pattern', MT304_SequenceC_OptionalGeneralInformation_98D_Type_Pattern)
_module_typeBindings.MT304_SequenceC_OptionalGeneralInformation_98D_Type_Pattern = MT304_SequenceC_OptionalGeneralInformation_98D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT304_SequenceC_OptionalGeneralInformation_98G_Type_Pattern
class MT304_SequenceC_OptionalGeneralInformation_98G_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceC_OptionalGeneralInformation_98G_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 757, 1)
    _Documentation = None
MT304_SequenceC_OptionalGeneralInformation_98G_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT304_SequenceC_OptionalGeneralInformation_98G_Type_Pattern._CF_pattern.addPattern(pattern='([0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])(0[0-9]|[1][0-9]|2[1-3])([0-5][0-9])([0-5][0-9])(,[0-9]{1,3})?(/(N)?(0[0-9]|[1][0-9]|2[1-3])(([0-5][0-9]))?)?)')
MT304_SequenceC_OptionalGeneralInformation_98G_Type_Pattern._InitializeFacetMap(MT304_SequenceC_OptionalGeneralInformation_98G_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceC_OptionalGeneralInformation_98G_Type_Pattern', MT304_SequenceC_OptionalGeneralInformation_98G_Type_Pattern)
_module_typeBindings.MT304_SequenceC_OptionalGeneralInformation_98G_Type_Pattern = MT304_SequenceC_OptionalGeneralInformation_98G_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT304_SequenceC_OptionalGeneralInformation_29A_Type_Pattern
class MT304_SequenceC_OptionalGeneralInformation_29A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceC_OptionalGeneralInformation_29A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 770, 1)
    _Documentation = None
MT304_SequenceC_OptionalGeneralInformation_29A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT304_SequenceC_OptionalGeneralInformation_29A_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT304_SequenceC_OptionalGeneralInformation_29A_Type_Pattern._InitializeFacetMap(MT304_SequenceC_OptionalGeneralInformation_29A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceC_OptionalGeneralInformation_29A_Type_Pattern', MT304_SequenceC_OptionalGeneralInformation_29A_Type_Pattern)
_module_typeBindings.MT304_SequenceC_OptionalGeneralInformation_29A_Type_Pattern = MT304_SequenceC_OptionalGeneralInformation_29A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT304_SequenceC_OptionalGeneralInformation_34C_Type_Pattern
class MT304_SequenceC_OptionalGeneralInformation_34C_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceC_OptionalGeneralInformation_34C_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 783, 1)
    _Documentation = None
MT304_SequenceC_OptionalGeneralInformation_34C_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT304_SequenceC_OptionalGeneralInformation_34C_Type_Pattern._CF_pattern.addPattern(pattern='([A-Z0-9]{4}/(N)?(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})')
MT304_SequenceC_OptionalGeneralInformation_34C_Type_Pattern._InitializeFacetMap(MT304_SequenceC_OptionalGeneralInformation_34C_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceC_OptionalGeneralInformation_34C_Type_Pattern', MT304_SequenceC_OptionalGeneralInformation_34C_Type_Pattern)
_module_typeBindings.MT304_SequenceC_OptionalGeneralInformation_34C_Type_Pattern = MT304_SequenceC_OptionalGeneralInformation_34C_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT304_SequenceD_AccountingInformation_21P_Type_Pattern
class MT304_SequenceD_AccountingInformation_21P_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceD_AccountingInformation_21P_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 804, 1)
    _Documentation = None
MT304_SequenceD_AccountingInformation_21P_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT304_SequenceD_AccountingInformation_21P_Type_Pattern._CF_pattern.addPattern(pattern="([^/]([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,16}[^/])")
MT304_SequenceD_AccountingInformation_21P_Type_Pattern._InitializeFacetMap(MT304_SequenceD_AccountingInformation_21P_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceD_AccountingInformation_21P_Type_Pattern', MT304_SequenceD_AccountingInformation_21P_Type_Pattern)
_module_typeBindings.MT304_SequenceD_AccountingInformation_21P_Type_Pattern = MT304_SequenceD_AccountingInformation_21P_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT304_SequenceD_AccountingInformation_17G_Type_Pattern
class MT304_SequenceD_AccountingInformation_17G_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceD_AccountingInformation_17G_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 817, 1)
    _Documentation = None
MT304_SequenceD_AccountingInformation_17G_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT304_SequenceD_AccountingInformation_17G_Type_Pattern._CF_pattern.addPattern(pattern='((N|Y))')
MT304_SequenceD_AccountingInformation_17G_Type_Pattern._InitializeFacetMap(MT304_SequenceD_AccountingInformation_17G_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceD_AccountingInformation_17G_Type_Pattern', MT304_SequenceD_AccountingInformation_17G_Type_Pattern)
_module_typeBindings.MT304_SequenceD_AccountingInformation_17G_Type_Pattern = MT304_SequenceD_AccountingInformation_17G_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT304_SequenceD_AccountingInformation_32G_Type_Pattern
class MT304_SequenceD_AccountingInformation_32G_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceD_AccountingInformation_32G_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 830, 1)
    _Documentation = None
MT304_SequenceD_AccountingInformation_32G_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT304_SequenceD_AccountingInformation_32G_Type_Pattern._CF_pattern.addPattern(pattern='((AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})')
MT304_SequenceD_AccountingInformation_32G_Type_Pattern._InitializeFacetMap(MT304_SequenceD_AccountingInformation_32G_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceD_AccountingInformation_32G_Type_Pattern', MT304_SequenceD_AccountingInformation_32G_Type_Pattern)
_module_typeBindings.MT304_SequenceD_AccountingInformation_32G_Type_Pattern = MT304_SequenceD_AccountingInformation_32G_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT304_SequenceD_AccountingInformation_34B_Type_Pattern
class MT304_SequenceD_AccountingInformation_34B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceD_AccountingInformation_34B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 843, 1)
    _Documentation = None
MT304_SequenceD_AccountingInformation_34B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT304_SequenceD_AccountingInformation_34B_Type_Pattern._CF_pattern.addPattern(pattern='((AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})')
MT304_SequenceD_AccountingInformation_34B_Type_Pattern._InitializeFacetMap(MT304_SequenceD_AccountingInformation_34B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceD_AccountingInformation_34B_Type_Pattern', MT304_SequenceD_AccountingInformation_34B_Type_Pattern)
_module_typeBindings.MT304_SequenceD_AccountingInformation_34B_Type_Pattern = MT304_SequenceD_AccountingInformation_34B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT304_SequenceD_AccountingInformation_30F_Type_Pattern
class MT304_SequenceD_AccountingInformation_30F_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceD_AccountingInformation_30F_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 856, 1)
    _Documentation = None
MT304_SequenceD_AccountingInformation_30F_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT304_SequenceD_AccountingInformation_30F_Type_Pattern._CF_pattern.addPattern(pattern='([0-9]{8})')
MT304_SequenceD_AccountingInformation_30F_Type_Pattern._InitializeFacetMap(MT304_SequenceD_AccountingInformation_30F_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceD_AccountingInformation_30F_Type_Pattern', MT304_SequenceD_AccountingInformation_30F_Type_Pattern)
_module_typeBindings.MT304_SequenceD_AccountingInformation_30F_Type_Pattern = MT304_SequenceD_AccountingInformation_30F_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT304_SequenceE_NetAmountToBeSettled_17G_Type_Pattern
class MT304_SequenceE_NetAmountToBeSettled_17G_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceE_NetAmountToBeSettled_17G_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 869, 1)
    _Documentation = None
MT304_SequenceE_NetAmountToBeSettled_17G_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT304_SequenceE_NetAmountToBeSettled_17G_Type_Pattern._CF_pattern.addPattern(pattern='((N|Y))')
MT304_SequenceE_NetAmountToBeSettled_17G_Type_Pattern._InitializeFacetMap(MT304_SequenceE_NetAmountToBeSettled_17G_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceE_NetAmountToBeSettled_17G_Type_Pattern', MT304_SequenceE_NetAmountToBeSettled_17G_Type_Pattern)
_module_typeBindings.MT304_SequenceE_NetAmountToBeSettled_17G_Type_Pattern = MT304_SequenceE_NetAmountToBeSettled_17G_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT304_SequenceE_NetAmountToBeSettled_32G_Type_Pattern
class MT304_SequenceE_NetAmountToBeSettled_32G_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceE_NetAmountToBeSettled_32G_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 882, 1)
    _Documentation = None
MT304_SequenceE_NetAmountToBeSettled_32G_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT304_SequenceE_NetAmountToBeSettled_32G_Type_Pattern._CF_pattern.addPattern(pattern='((AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})')
MT304_SequenceE_NetAmountToBeSettled_32G_Type_Pattern._InitializeFacetMap(MT304_SequenceE_NetAmountToBeSettled_32G_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceE_NetAmountToBeSettled_32G_Type_Pattern', MT304_SequenceE_NetAmountToBeSettled_32G_Type_Pattern)
_module_typeBindings.MT304_SequenceE_NetAmountToBeSettled_32G_Type_Pattern = MT304_SequenceE_NetAmountToBeSettled_32G_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT304_SequenceE_NetAmountToBeSettled_53A_Type_Pattern
class MT304_SequenceE_NetAmountToBeSettled_53A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceE_NetAmountToBeSettled_53A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 895, 1)
    _Documentation = None
MT304_SequenceE_NetAmountToBeSettled_53A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT304_SequenceE_NetAmountToBeSettled_53A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT304_SequenceE_NetAmountToBeSettled_53A_Type_Pattern._InitializeFacetMap(MT304_SequenceE_NetAmountToBeSettled_53A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceE_NetAmountToBeSettled_53A_Type_Pattern', MT304_SequenceE_NetAmountToBeSettled_53A_Type_Pattern)
_module_typeBindings.MT304_SequenceE_NetAmountToBeSettled_53A_Type_Pattern = MT304_SequenceE_NetAmountToBeSettled_53A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT304_SequenceE_NetAmountToBeSettled_53D_Type_Pattern
class MT304_SequenceE_NetAmountToBeSettled_53D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceE_NetAmountToBeSettled_53D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 908, 1)
    _Documentation = None
MT304_SequenceE_NetAmountToBeSettled_53D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT304_SequenceE_NetAmountToBeSettled_53D_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT304_SequenceE_NetAmountToBeSettled_53D_Type_Pattern._InitializeFacetMap(MT304_SequenceE_NetAmountToBeSettled_53D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceE_NetAmountToBeSettled_53D_Type_Pattern', MT304_SequenceE_NetAmountToBeSettled_53D_Type_Pattern)
_module_typeBindings.MT304_SequenceE_NetAmountToBeSettled_53D_Type_Pattern = MT304_SequenceE_NetAmountToBeSettled_53D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT304_SequenceE_NetAmountToBeSettled_53J_Type_Pattern
class MT304_SequenceE_NetAmountToBeSettled_53J_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceE_NetAmountToBeSettled_53J_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 921, 1)
    _Documentation = None
MT304_SequenceE_NetAmountToBeSettled_53J_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT304_SequenceE_NetAmountToBeSettled_53J_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,40}\\n?){1,5})")
MT304_SequenceE_NetAmountToBeSettled_53J_Type_Pattern._InitializeFacetMap(MT304_SequenceE_NetAmountToBeSettled_53J_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceE_NetAmountToBeSettled_53J_Type_Pattern', MT304_SequenceE_NetAmountToBeSettled_53J_Type_Pattern)
_module_typeBindings.MT304_SequenceE_NetAmountToBeSettled_53J_Type_Pattern = MT304_SequenceE_NetAmountToBeSettled_53J_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT304_SequenceE_NetAmountToBeSettled_56A_Type_Pattern
class MT304_SequenceE_NetAmountToBeSettled_56A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceE_NetAmountToBeSettled_56A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 934, 1)
    _Documentation = None
MT304_SequenceE_NetAmountToBeSettled_56A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT304_SequenceE_NetAmountToBeSettled_56A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT304_SequenceE_NetAmountToBeSettled_56A_Type_Pattern._InitializeFacetMap(MT304_SequenceE_NetAmountToBeSettled_56A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceE_NetAmountToBeSettled_56A_Type_Pattern', MT304_SequenceE_NetAmountToBeSettled_56A_Type_Pattern)
_module_typeBindings.MT304_SequenceE_NetAmountToBeSettled_56A_Type_Pattern = MT304_SequenceE_NetAmountToBeSettled_56A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT304_SequenceE_NetAmountToBeSettled_56D_Type_Pattern
class MT304_SequenceE_NetAmountToBeSettled_56D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceE_NetAmountToBeSettled_56D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 947, 1)
    _Documentation = None
MT304_SequenceE_NetAmountToBeSettled_56D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT304_SequenceE_NetAmountToBeSettled_56D_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT304_SequenceE_NetAmountToBeSettled_56D_Type_Pattern._InitializeFacetMap(MT304_SequenceE_NetAmountToBeSettled_56D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceE_NetAmountToBeSettled_56D_Type_Pattern', MT304_SequenceE_NetAmountToBeSettled_56D_Type_Pattern)
_module_typeBindings.MT304_SequenceE_NetAmountToBeSettled_56D_Type_Pattern = MT304_SequenceE_NetAmountToBeSettled_56D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT304_SequenceE_NetAmountToBeSettled_56J_Type_Pattern
class MT304_SequenceE_NetAmountToBeSettled_56J_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceE_NetAmountToBeSettled_56J_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 960, 1)
    _Documentation = None
MT304_SequenceE_NetAmountToBeSettled_56J_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT304_SequenceE_NetAmountToBeSettled_56J_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,40}\\n?){1,5})")
MT304_SequenceE_NetAmountToBeSettled_56J_Type_Pattern._InitializeFacetMap(MT304_SequenceE_NetAmountToBeSettled_56J_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceE_NetAmountToBeSettled_56J_Type_Pattern', MT304_SequenceE_NetAmountToBeSettled_56J_Type_Pattern)
_module_typeBindings.MT304_SequenceE_NetAmountToBeSettled_56J_Type_Pattern = MT304_SequenceE_NetAmountToBeSettled_56J_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT304_SequenceE_NetAmountToBeSettled_57A_Type_Pattern
class MT304_SequenceE_NetAmountToBeSettled_57A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceE_NetAmountToBeSettled_57A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 973, 1)
    _Documentation = None
MT304_SequenceE_NetAmountToBeSettled_57A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT304_SequenceE_NetAmountToBeSettled_57A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT304_SequenceE_NetAmountToBeSettled_57A_Type_Pattern._InitializeFacetMap(MT304_SequenceE_NetAmountToBeSettled_57A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceE_NetAmountToBeSettled_57A_Type_Pattern', MT304_SequenceE_NetAmountToBeSettled_57A_Type_Pattern)
_module_typeBindings.MT304_SequenceE_NetAmountToBeSettled_57A_Type_Pattern = MT304_SequenceE_NetAmountToBeSettled_57A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT304_SequenceE_NetAmountToBeSettled_57D_Type_Pattern
class MT304_SequenceE_NetAmountToBeSettled_57D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceE_NetAmountToBeSettled_57D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 986, 1)
    _Documentation = None
MT304_SequenceE_NetAmountToBeSettled_57D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT304_SequenceE_NetAmountToBeSettled_57D_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT304_SequenceE_NetAmountToBeSettled_57D_Type_Pattern._InitializeFacetMap(MT304_SequenceE_NetAmountToBeSettled_57D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceE_NetAmountToBeSettled_57D_Type_Pattern', MT304_SequenceE_NetAmountToBeSettled_57D_Type_Pattern)
_module_typeBindings.MT304_SequenceE_NetAmountToBeSettled_57D_Type_Pattern = MT304_SequenceE_NetAmountToBeSettled_57D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT304_SequenceE_NetAmountToBeSettled_57J_Type_Pattern
class MT304_SequenceE_NetAmountToBeSettled_57J_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceE_NetAmountToBeSettled_57J_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 999, 1)
    _Documentation = None
MT304_SequenceE_NetAmountToBeSettled_57J_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT304_SequenceE_NetAmountToBeSettled_57J_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,40}\\n?){1,5})")
MT304_SequenceE_NetAmountToBeSettled_57J_Type_Pattern._InitializeFacetMap(MT304_SequenceE_NetAmountToBeSettled_57J_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceE_NetAmountToBeSettled_57J_Type_Pattern', MT304_SequenceE_NetAmountToBeSettled_57J_Type_Pattern)
_module_typeBindings.MT304_SequenceE_NetAmountToBeSettled_57J_Type_Pattern = MT304_SequenceE_NetAmountToBeSettled_57J_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT304_SequenceE_NetAmountToBeSettled_58A_Type_Pattern
class MT304_SequenceE_NetAmountToBeSettled_58A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceE_NetAmountToBeSettled_58A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1012, 1)
    _Documentation = None
MT304_SequenceE_NetAmountToBeSettled_58A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT304_SequenceE_NetAmountToBeSettled_58A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT304_SequenceE_NetAmountToBeSettled_58A_Type_Pattern._InitializeFacetMap(MT304_SequenceE_NetAmountToBeSettled_58A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceE_NetAmountToBeSettled_58A_Type_Pattern', MT304_SequenceE_NetAmountToBeSettled_58A_Type_Pattern)
_module_typeBindings.MT304_SequenceE_NetAmountToBeSettled_58A_Type_Pattern = MT304_SequenceE_NetAmountToBeSettled_58A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT304_SequenceE_NetAmountToBeSettled_58D_Type_Pattern
class MT304_SequenceE_NetAmountToBeSettled_58D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceE_NetAmountToBeSettled_58D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1025, 1)
    _Documentation = None
MT304_SequenceE_NetAmountToBeSettled_58D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT304_SequenceE_NetAmountToBeSettled_58D_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT304_SequenceE_NetAmountToBeSettled_58D_Type_Pattern._InitializeFacetMap(MT304_SequenceE_NetAmountToBeSettled_58D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceE_NetAmountToBeSettled_58D_Type_Pattern', MT304_SequenceE_NetAmountToBeSettled_58D_Type_Pattern)
_module_typeBindings.MT304_SequenceE_NetAmountToBeSettled_58D_Type_Pattern = MT304_SequenceE_NetAmountToBeSettled_58D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT304_SequenceE_NetAmountToBeSettled_58J_Type_Pattern
class MT304_SequenceE_NetAmountToBeSettled_58J_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceE_NetAmountToBeSettled_58J_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1038, 1)
    _Documentation = None
MT304_SequenceE_NetAmountToBeSettled_58J_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT304_SequenceE_NetAmountToBeSettled_58J_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,40}\\n?){1,5})")
MT304_SequenceE_NetAmountToBeSettled_58J_Type_Pattern._InitializeFacetMap(MT304_SequenceE_NetAmountToBeSettled_58J_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceE_NetAmountToBeSettled_58J_Type_Pattern', MT304_SequenceE_NetAmountToBeSettled_58J_Type_Pattern)
_module_typeBindings.MT304_SequenceE_NetAmountToBeSettled_58J_Type_Pattern = MT304_SequenceE_NetAmountToBeSettled_58J_Type_Pattern

# Complex type {http://www.w3schools.com}MT304_SequenceC_OptionalGeneralInformation_72_Type with content type SIMPLE
class MT304_SequenceC_OptionalGeneralInformation_72_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT304_SequenceC_OptionalGeneralInformation_72_Type with content type SIMPLE"""
    _TypeDefinition = pyxb.binding.datatypes.string
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceC_OptionalGeneralInformation_72_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 796, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.string
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT304_SequenceC_OptionalGeneralInformation_72_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='72')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 799, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 799, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT304_SequenceC_OptionalGeneralInformation_72_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 800, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 800, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT304_SequenceC_OptionalGeneralInformation_72_Type = MT304_SequenceC_OptionalGeneralInformation_72_Type
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceC_OptionalGeneralInformation_72_Type', MT304_SequenceC_OptionalGeneralInformation_72_Type)


# Complex type {http://www.w3schools.com}MT304_SequenceA_GeneralInformation with content type ELEMENT_ONLY
class MT304_SequenceA_GeneralInformation (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT304_SequenceA_GeneralInformation with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceA_GeneralInformation')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1051, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}SendersReference uses Python identifier SendersReference
    __SendersReference = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SendersReference'), 'SendersReference', '__httpwww_w3schools_com_MT304_SequenceA_GeneralInformation_httpwww_w3schools_comSendersReference', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1053, 3), )

    
    SendersReference = property(__SendersReference.value, __SendersReference.set, None, None)

    
    # Element {http://www.w3schools.com}RelatedReference uses Python identifier RelatedReference
    __RelatedReference = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'RelatedReference'), 'RelatedReference', '__httpwww_w3schools_com_MT304_SequenceA_GeneralInformation_httpwww_w3schools_comRelatedReference', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1054, 3), )

    
    RelatedReference = property(__RelatedReference.value, __RelatedReference.set, None, None)

    
    # Element {http://www.w3schools.com}TypeOfOperation uses Python identifier TypeOfOperation
    __TypeOfOperation = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'TypeOfOperation'), 'TypeOfOperation', '__httpwww_w3schools_com_MT304_SequenceA_GeneralInformation_httpwww_w3schools_comTypeOfOperation', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1055, 3), )

    
    TypeOfOperation = property(__TypeOfOperation.value, __TypeOfOperation.set, None, None)

    
    # Element {http://www.w3schools.com}ScopeOfOperation uses Python identifier ScopeOfOperation
    __ScopeOfOperation = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ScopeOfOperation'), 'ScopeOfOperation', '__httpwww_w3schools_com_MT304_SequenceA_GeneralInformation_httpwww_w3schools_comScopeOfOperation', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1056, 3), )

    
    ScopeOfOperation = property(__ScopeOfOperation.value, __ScopeOfOperation.set, None, None)

    
    # Element {http://www.w3schools.com}OpenIndicator uses Python identifier OpenIndicator
    __OpenIndicator = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'OpenIndicator'), 'OpenIndicator', '__httpwww_w3schools_com_MT304_SequenceA_GeneralInformation_httpwww_w3schools_comOpenIndicator', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1057, 3), )

    
    OpenIndicator = property(__OpenIndicator.value, __OpenIndicator.set, None, None)

    
    # Element {http://www.w3schools.com}FinalCloseIndicator uses Python identifier FinalCloseIndicator
    __FinalCloseIndicator = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'FinalCloseIndicator'), 'FinalCloseIndicator', '__httpwww_w3schools_com_MT304_SequenceA_GeneralInformation_httpwww_w3schools_comFinalCloseIndicator', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1058, 3), )

    
    FinalCloseIndicator = property(__FinalCloseIndicator.value, __FinalCloseIndicator.set, None, None)

    
    # Element {http://www.w3schools.com}NetSettlementIndicator uses Python identifier NetSettlementIndicator
    __NetSettlementIndicator = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'NetSettlementIndicator'), 'NetSettlementIndicator', '__httpwww_w3schools_com_MT304_SequenceA_GeneralInformation_httpwww_w3schools_comNetSettlementIndicator', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1059, 3), )

    
    NetSettlementIndicator = property(__NetSettlementIndicator.value, __NetSettlementIndicator.set, None, None)

    
    # Element {http://www.w3schools.com}Fund_A uses Python identifier Fund_A
    __Fund_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Fund_A'), 'Fund_A', '__httpwww_w3schools_com_MT304_SequenceA_GeneralInformation_httpwww_w3schools_comFund_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1061, 4), )

    
    Fund_A = property(__Fund_A.value, __Fund_A.set, None, None)

    
    # Element {http://www.w3schools.com}Fund_J uses Python identifier Fund_J
    __Fund_J = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Fund_J'), 'Fund_J', '__httpwww_w3schools_com_MT304_SequenceA_GeneralInformation_httpwww_w3schools_comFund_J', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1062, 4), )

    
    Fund_J = property(__Fund_J.value, __Fund_J.set, None, None)

    
    # Element {http://www.w3schools.com}FundManager_A uses Python identifier FundManager_A
    __FundManager_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'FundManager_A'), 'FundManager_A', '__httpwww_w3schools_com_MT304_SequenceA_GeneralInformation_httpwww_w3schools_comFundManager_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1065, 4), )

    
    FundManager_A = property(__FundManager_A.value, __FundManager_A.set, None, None)

    
    # Element {http://www.w3schools.com}FundManager_J uses Python identifier FundManager_J
    __FundManager_J = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'FundManager_J'), 'FundManager_J', '__httpwww_w3schools_com_MT304_SequenceA_GeneralInformation_httpwww_w3schools_comFundManager_J', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1066, 4), )

    
    FundManager_J = property(__FundManager_J.value, __FundManager_J.set, None, None)

    
    # Element {http://www.w3schools.com}ExecutingBroker_A uses Python identifier ExecutingBroker_A
    __ExecutingBroker_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ExecutingBroker_A'), 'ExecutingBroker_A', '__httpwww_w3schools_com_MT304_SequenceA_GeneralInformation_httpwww_w3schools_comExecutingBroker_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1069, 4), )

    
    ExecutingBroker_A = property(__ExecutingBroker_A.value, __ExecutingBroker_A.set, None, None)

    
    # Element {http://www.w3schools.com}ExecutingBroker_J uses Python identifier ExecutingBroker_J
    __ExecutingBroker_J = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ExecutingBroker_J'), 'ExecutingBroker_J', '__httpwww_w3schools_com_MT304_SequenceA_GeneralInformation_httpwww_w3schools_comExecutingBroker_J', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1070, 4), )

    
    ExecutingBroker_J = property(__ExecutingBroker_J.value, __ExecutingBroker_J.set, None, None)

    
    # Element {http://www.w3schools.com}CentralCounterpartyClearingHouse_A uses Python identifier CentralCounterpartyClearingHouse_A
    __CentralCounterpartyClearingHouse_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'CentralCounterpartyClearingHouse_A'), 'CentralCounterpartyClearingHouse_A', '__httpwww_w3schools_com_MT304_SequenceA_GeneralInformation_httpwww_w3schools_comCentralCounterpartyClearingHouse_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1073, 4), )

    
    CentralCounterpartyClearingHouse_A = property(__CentralCounterpartyClearingHouse_A.value, __CentralCounterpartyClearingHouse_A.set, None, None)

    
    # Element {http://www.w3schools.com}CentralCounterpartyClearingHouse_D uses Python identifier CentralCounterpartyClearingHouse_D
    __CentralCounterpartyClearingHouse_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'CentralCounterpartyClearingHouse_D'), 'CentralCounterpartyClearingHouse_D', '__httpwww_w3schools_com_MT304_SequenceA_GeneralInformation_httpwww_w3schools_comCentralCounterpartyClearingHouse_D', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1074, 4), )

    
    CentralCounterpartyClearingHouse_D = property(__CentralCounterpartyClearingHouse_D.value, __CentralCounterpartyClearingHouse_D.set, None, None)

    
    # Element {http://www.w3schools.com}CentralCounterpartyClearingHouse_J uses Python identifier CentralCounterpartyClearingHouse_J
    __CentralCounterpartyClearingHouse_J = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'CentralCounterpartyClearingHouse_J'), 'CentralCounterpartyClearingHouse_J', '__httpwww_w3schools_com_MT304_SequenceA_GeneralInformation_httpwww_w3schools_comCentralCounterpartyClearingHouse_J', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1075, 4), )

    
    CentralCounterpartyClearingHouse_J = property(__CentralCounterpartyClearingHouse_J.value, __CentralCounterpartyClearingHouse_J.set, None, None)

    
    # Element {http://www.w3schools.com}ClearingBroker_A uses Python identifier ClearingBroker_A
    __ClearingBroker_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ClearingBroker_A'), 'ClearingBroker_A', '__httpwww_w3schools_com_MT304_SequenceA_GeneralInformation_httpwww_w3schools_comClearingBroker_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1078, 4), )

    
    ClearingBroker_A = property(__ClearingBroker_A.value, __ClearingBroker_A.set, None, None)

    
    # Element {http://www.w3schools.com}ClearingBroker_D uses Python identifier ClearingBroker_D
    __ClearingBroker_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ClearingBroker_D'), 'ClearingBroker_D', '__httpwww_w3schools_com_MT304_SequenceA_GeneralInformation_httpwww_w3schools_comClearingBroker_D', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1079, 4), )

    
    ClearingBroker_D = property(__ClearingBroker_D.value, __ClearingBroker_D.set, None, None)

    
    # Element {http://www.w3schools.com}ClearingBroker_J uses Python identifier ClearingBroker_J
    __ClearingBroker_J = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ClearingBroker_J'), 'ClearingBroker_J', '__httpwww_w3schools_com_MT304_SequenceA_GeneralInformation_httpwww_w3schools_comClearingBroker_J', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1080, 4), )

    
    ClearingBroker_J = property(__ClearingBroker_J.value, __ClearingBroker_J.set, None, None)

    
    # Element {http://www.w3schools.com}PaymentVersusPaymentSettlementIndicator uses Python identifier PaymentVersusPaymentSettlementIndicator
    __PaymentVersusPaymentSettlementIndicator = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PaymentVersusPaymentSettlementIndicator'), 'PaymentVersusPaymentSettlementIndicator', '__httpwww_w3schools_com_MT304_SequenceA_GeneralInformation_httpwww_w3schools_comPaymentVersusPaymentSettlementIndicator', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1082, 3), )

    
    PaymentVersusPaymentSettlementIndicator = property(__PaymentVersusPaymentSettlementIndicator.value, __PaymentVersusPaymentSettlementIndicator.set, None, None)

    
    # Element {http://www.w3schools.com}TypeDateVersionOfTheAgreement uses Python identifier TypeDateVersionOfTheAgreement
    __TypeDateVersionOfTheAgreement = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'TypeDateVersionOfTheAgreement'), 'TypeDateVersionOfTheAgreement', '__httpwww_w3schools_com_MT304_SequenceA_GeneralInformation_httpwww_w3schools_comTypeDateVersionOfTheAgreement', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1083, 3), )

    
    TypeDateVersionOfTheAgreement = property(__TypeDateVersionOfTheAgreement.value, __TypeDateVersionOfTheAgreement.set, None, None)

    
    # Element {http://www.w3schools.com}YearOfDefinitions uses Python identifier YearOfDefinitions
    __YearOfDefinitions = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'YearOfDefinitions'), 'YearOfDefinitions', '__httpwww_w3schools_com_MT304_SequenceA_GeneralInformation_httpwww_w3schools_comYearOfDefinitions', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1084, 3), )

    
    YearOfDefinitions = property(__YearOfDefinitions.value, __YearOfDefinitions.set, None, None)

    
    # Element {http://www.w3schools.com}SettlementCurrency uses Python identifier SettlementCurrency
    __SettlementCurrency = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SettlementCurrency'), 'SettlementCurrency', '__httpwww_w3schools_com_MT304_SequenceA_GeneralInformation_httpwww_w3schools_comSettlementCurrency', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1085, 3), )

    
    SettlementCurrency = property(__SettlementCurrency.value, __SettlementCurrency.set, None, None)

    
    # Element {http://www.w3schools.com}ValuationDate uses Python identifier ValuationDate
    __ValuationDate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ValuationDate'), 'ValuationDate', '__httpwww_w3schools_com_MT304_SequenceA_GeneralInformation_httpwww_w3schools_comValuationDate', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1086, 3), )

    
    ValuationDate = property(__ValuationDate.value, __ValuationDate.set, None, None)

    
    # Element {http://www.w3schools.com}SettlementRateSource uses Python identifier SettlementRateSource
    __SettlementRateSource = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SettlementRateSource'), 'SettlementRateSource', '__httpwww_w3schools_com_MT304_SequenceA_GeneralInformation_httpwww_w3schools_comSettlementRateSource', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1087, 3), )

    
    SettlementRateSource = property(__SettlementRateSource.value, __SettlementRateSource.set, None, None)

    
    # Element {http://www.w3schools.com}ReferenceToOpeningInstruction uses Python identifier ReferenceToOpeningInstruction
    __ReferenceToOpeningInstruction = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ReferenceToOpeningInstruction'), 'ReferenceToOpeningInstruction', '__httpwww_w3schools_com_MT304_SequenceA_GeneralInformation_httpwww_w3schools_comReferenceToOpeningInstruction', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1088, 3), )

    
    ReferenceToOpeningInstruction = property(__ReferenceToOpeningInstruction.value, __ReferenceToOpeningInstruction.set, None, None)

    
    # Element {http://www.w3schools.com}ClearingOrSettlementSession uses Python identifier ClearingOrSettlementSession
    __ClearingOrSettlementSession = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ClearingOrSettlementSession'), 'ClearingOrSettlementSession', '__httpwww_w3schools_com_MT304_SequenceA_GeneralInformation_httpwww_w3schools_comClearingOrSettlementSession', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1089, 3), )

    
    ClearingOrSettlementSession = property(__ClearingOrSettlementSession.value, __ClearingOrSettlementSession.set, None, None)

    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT304_SequenceA_GeneralInformation_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='15A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1091, 2)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1091, 2)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT304_SequenceA_GeneralInformation_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1092, 2)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1092, 2)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    
    # Attribute formatTag uses Python identifier formatTag
    __formatTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'formatTag'), 'formatTag', '__httpwww_w3schools_com_MT304_SequenceA_GeneralInformation_formatTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='False')
    __formatTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1093, 2)
    __formatTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1093, 2)
    
    formatTag = property(__formatTag.value, __formatTag.set, None, None)

    _ElementMap.update({
        __SendersReference.name() : __SendersReference,
        __RelatedReference.name() : __RelatedReference,
        __TypeOfOperation.name() : __TypeOfOperation,
        __ScopeOfOperation.name() : __ScopeOfOperation,
        __OpenIndicator.name() : __OpenIndicator,
        __FinalCloseIndicator.name() : __FinalCloseIndicator,
        __NetSettlementIndicator.name() : __NetSettlementIndicator,
        __Fund_A.name() : __Fund_A,
        __Fund_J.name() : __Fund_J,
        __FundManager_A.name() : __FundManager_A,
        __FundManager_J.name() : __FundManager_J,
        __ExecutingBroker_A.name() : __ExecutingBroker_A,
        __ExecutingBroker_J.name() : __ExecutingBroker_J,
        __CentralCounterpartyClearingHouse_A.name() : __CentralCounterpartyClearingHouse_A,
        __CentralCounterpartyClearingHouse_D.name() : __CentralCounterpartyClearingHouse_D,
        __CentralCounterpartyClearingHouse_J.name() : __CentralCounterpartyClearingHouse_J,
        __ClearingBroker_A.name() : __ClearingBroker_A,
        __ClearingBroker_D.name() : __ClearingBroker_D,
        __ClearingBroker_J.name() : __ClearingBroker_J,
        __PaymentVersusPaymentSettlementIndicator.name() : __PaymentVersusPaymentSettlementIndicator,
        __TypeDateVersionOfTheAgreement.name() : __TypeDateVersionOfTheAgreement,
        __YearOfDefinitions.name() : __YearOfDefinitions,
        __SettlementCurrency.name() : __SettlementCurrency,
        __ValuationDate.name() : __ValuationDate,
        __SettlementRateSource.name() : __SettlementRateSource,
        __ReferenceToOpeningInstruction.name() : __ReferenceToOpeningInstruction,
        __ClearingOrSettlementSession.name() : __ClearingOrSettlementSession
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory,
        __formatTag.name() : __formatTag
    })
_module_typeBindings.MT304_SequenceA_GeneralInformation = MT304_SequenceA_GeneralInformation
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceA_GeneralInformation', MT304_SequenceA_GeneralInformation)


# Complex type {http://www.w3schools.com}MT304_SequenceB_ForexTransactionDetails with content type ELEMENT_ONLY
class MT304_SequenceB_ForexTransactionDetails (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT304_SequenceB_ForexTransactionDetails with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceB_ForexTransactionDetails')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1095, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}TradeDate uses Python identifier TradeDate
    __TradeDate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'TradeDate'), 'TradeDate', '__httpwww_w3schools_com_MT304_SequenceB_ForexTransactionDetails_httpwww_w3schools_comTradeDate', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1097, 3), )

    
    TradeDate = property(__TradeDate.value, __TradeDate.set, None, None)

    
    # Element {http://www.w3schools.com}ValueDate uses Python identifier ValueDate
    __ValueDate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ValueDate'), 'ValueDate', '__httpwww_w3schools_com_MT304_SequenceB_ForexTransactionDetails_httpwww_w3schools_comValueDate', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1098, 3), )

    
    ValueDate = property(__ValueDate.value, __ValueDate.set, None, None)

    
    # Element {http://www.w3schools.com}ExchangeRate uses Python identifier ExchangeRate
    __ExchangeRate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ExchangeRate'), 'ExchangeRate', '__httpwww_w3schools_com_MT304_SequenceB_ForexTransactionDetails_httpwww_w3schools_comExchangeRate', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1099, 3), )

    
    ExchangeRate = property(__ExchangeRate.value, __ExchangeRate.set, None, None)

    
    # Element {http://www.w3schools.com}PaymentClearingCentre uses Python identifier PaymentClearingCentre
    __PaymentClearingCentre = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PaymentClearingCentre'), 'PaymentClearingCentre', '__httpwww_w3schools_com_MT304_SequenceB_ForexTransactionDetails_httpwww_w3schools_comPaymentClearingCentre', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1100, 3), )

    
    PaymentClearingCentre = property(__PaymentClearingCentre.value, __PaymentClearingCentre.set, None, None)

    
    # Element {http://www.w3schools.com}SubsequenceB1_AmountBought uses Python identifier SubsequenceB1_AmountBought
    __SubsequenceB1_AmountBought = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SubsequenceB1_AmountBought'), 'SubsequenceB1_AmountBought', '__httpwww_w3schools_com_MT304_SequenceB_ForexTransactionDetails_httpwww_w3schools_comSubsequenceB1_AmountBought', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1101, 3), )

    
    SubsequenceB1_AmountBought = property(__SubsequenceB1_AmountBought.value, __SubsequenceB1_AmountBought.set, None, None)

    
    # Element {http://www.w3schools.com}SubsequenceB2_AmountSold uses Python identifier SubsequenceB2_AmountSold
    __SubsequenceB2_AmountSold = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SubsequenceB2_AmountSold'), 'SubsequenceB2_AmountSold', '__httpwww_w3schools_com_MT304_SequenceB_ForexTransactionDetails_httpwww_w3schools_comSubsequenceB2_AmountSold', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1102, 3), )

    
    SubsequenceB2_AmountSold = property(__SubsequenceB2_AmountSold.value, __SubsequenceB2_AmountSold.set, None, None)

    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT304_SequenceB_ForexTransactionDetails_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='15B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1104, 2)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1104, 2)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT304_SequenceB_ForexTransactionDetails_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1105, 2)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1105, 2)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    
    # Attribute formatTag uses Python identifier formatTag
    __formatTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'formatTag'), 'formatTag', '__httpwww_w3schools_com_MT304_SequenceB_ForexTransactionDetails_formatTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='False')
    __formatTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1106, 2)
    __formatTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1106, 2)
    
    formatTag = property(__formatTag.value, __formatTag.set, None, None)

    _ElementMap.update({
        __TradeDate.name() : __TradeDate,
        __ValueDate.name() : __ValueDate,
        __ExchangeRate.name() : __ExchangeRate,
        __PaymentClearingCentre.name() : __PaymentClearingCentre,
        __SubsequenceB1_AmountBought.name() : __SubsequenceB1_AmountBought,
        __SubsequenceB2_AmountSold.name() : __SubsequenceB2_AmountSold
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory,
        __formatTag.name() : __formatTag
    })
_module_typeBindings.MT304_SequenceB_ForexTransactionDetails = MT304_SequenceB_ForexTransactionDetails
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceB_ForexTransactionDetails', MT304_SequenceB_ForexTransactionDetails)


# Complex type {http://www.w3schools.com}MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought with content type ELEMENT_ONLY
class MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1108, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}CurrencyAmountBought uses Python identifier CurrencyAmountBought
    __CurrencyAmountBought = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'CurrencyAmountBought'), 'CurrencyAmountBought', '__httpwww_w3schools_com_MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_httpwww_w3schools_comCurrencyAmountBought', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1110, 3), )

    
    CurrencyAmountBought = property(__CurrencyAmountBought.value, __CurrencyAmountBought.set, None, None)

    
    # Element {http://www.w3schools.com}DeliveryAgent_A uses Python identifier DeliveryAgent_A
    __DeliveryAgent_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_A'), 'DeliveryAgent_A', '__httpwww_w3schools_com_MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_httpwww_w3schools_comDeliveryAgent_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1112, 4), )

    
    DeliveryAgent_A = property(__DeliveryAgent_A.value, __DeliveryAgent_A.set, None, None)

    
    # Element {http://www.w3schools.com}DeliveryAgent_J uses Python identifier DeliveryAgent_J
    __DeliveryAgent_J = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_J'), 'DeliveryAgent_J', '__httpwww_w3schools_com_MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_httpwww_w3schools_comDeliveryAgent_J', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1113, 4), )

    
    DeliveryAgent_J = property(__DeliveryAgent_J.value, __DeliveryAgent_J.set, None, None)

    
    # Element {http://www.w3schools.com}Intermediary_A uses Python identifier Intermediary_A
    __Intermediary_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_A'), 'Intermediary_A', '__httpwww_w3schools_com_MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_httpwww_w3schools_comIntermediary_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1116, 4), )

    
    Intermediary_A = property(__Intermediary_A.value, __Intermediary_A.set, None, None)

    
    # Element {http://www.w3schools.com}Intermediary_J uses Python identifier Intermediary_J
    __Intermediary_J = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_J'), 'Intermediary_J', '__httpwww_w3schools_com_MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_httpwww_w3schools_comIntermediary_J', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1117, 4), )

    
    Intermediary_J = property(__Intermediary_J.value, __Intermediary_J.set, None, None)

    
    # Element {http://www.w3schools.com}ReceivingAgent_A uses Python identifier ReceivingAgent_A
    __ReceivingAgent_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_A'), 'ReceivingAgent_A', '__httpwww_w3schools_com_MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_httpwww_w3schools_comReceivingAgent_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1120, 4), )

    
    ReceivingAgent_A = property(__ReceivingAgent_A.value, __ReceivingAgent_A.set, None, None)

    
    # Element {http://www.w3schools.com}ReceivingAgent_J uses Python identifier ReceivingAgent_J
    __ReceivingAgent_J = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_J'), 'ReceivingAgent_J', '__httpwww_w3schools_com_MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_httpwww_w3schools_comReceivingAgent_J', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1121, 4), )

    
    ReceivingAgent_J = property(__ReceivingAgent_J.value, __ReceivingAgent_J.set, None, None)

    _ElementMap.update({
        __CurrencyAmountBought.name() : __CurrencyAmountBought,
        __DeliveryAgent_A.name() : __DeliveryAgent_A,
        __DeliveryAgent_J.name() : __DeliveryAgent_J,
        __Intermediary_A.name() : __Intermediary_A,
        __Intermediary_J.name() : __Intermediary_J,
        __ReceivingAgent_A.name() : __ReceivingAgent_A,
        __ReceivingAgent_J.name() : __ReceivingAgent_J
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought = MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought', MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought)


# Complex type {http://www.w3schools.com}MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold with content type ELEMENT_ONLY
class MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1125, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}CurrencyAmountSold uses Python identifier CurrencyAmountSold
    __CurrencyAmountSold = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'CurrencyAmountSold'), 'CurrencyAmountSold', '__httpwww_w3schools_com_MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_httpwww_w3schools_comCurrencyAmountSold', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1127, 3), )

    
    CurrencyAmountSold = property(__CurrencyAmountSold.value, __CurrencyAmountSold.set, None, None)

    
    # Element {http://www.w3schools.com}DeliveryAgent_A uses Python identifier DeliveryAgent_A
    __DeliveryAgent_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_A'), 'DeliveryAgent_A', '__httpwww_w3schools_com_MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_httpwww_w3schools_comDeliveryAgent_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1129, 4), )

    
    DeliveryAgent_A = property(__DeliveryAgent_A.value, __DeliveryAgent_A.set, None, None)

    
    # Element {http://www.w3schools.com}DeliveryAgent_J uses Python identifier DeliveryAgent_J
    __DeliveryAgent_J = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_J'), 'DeliveryAgent_J', '__httpwww_w3schools_com_MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_httpwww_w3schools_comDeliveryAgent_J', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1130, 4), )

    
    DeliveryAgent_J = property(__DeliveryAgent_J.value, __DeliveryAgent_J.set, None, None)

    
    # Element {http://www.w3schools.com}Intermediary_A uses Python identifier Intermediary_A
    __Intermediary_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_A'), 'Intermediary_A', '__httpwww_w3schools_com_MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_httpwww_w3schools_comIntermediary_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1133, 4), )

    
    Intermediary_A = property(__Intermediary_A.value, __Intermediary_A.set, None, None)

    
    # Element {http://www.w3schools.com}Intermediary_J uses Python identifier Intermediary_J
    __Intermediary_J = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_J'), 'Intermediary_J', '__httpwww_w3schools_com_MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_httpwww_w3schools_comIntermediary_J', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1134, 4), )

    
    Intermediary_J = property(__Intermediary_J.value, __Intermediary_J.set, None, None)

    
    # Element {http://www.w3schools.com}ReceivingAgent_A uses Python identifier ReceivingAgent_A
    __ReceivingAgent_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_A'), 'ReceivingAgent_A', '__httpwww_w3schools_com_MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_httpwww_w3schools_comReceivingAgent_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1137, 4), )

    
    ReceivingAgent_A = property(__ReceivingAgent_A.value, __ReceivingAgent_A.set, None, None)

    
    # Element {http://www.w3schools.com}ReceivingAgent_J uses Python identifier ReceivingAgent_J
    __ReceivingAgent_J = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_J'), 'ReceivingAgent_J', '__httpwww_w3schools_com_MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_httpwww_w3schools_comReceivingAgent_J', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1138, 4), )

    
    ReceivingAgent_J = property(__ReceivingAgent_J.value, __ReceivingAgent_J.set, None, None)

    
    # Element {http://www.w3schools.com}BeneficiaryInstitution_A uses Python identifier BeneficiaryInstitution_A
    __BeneficiaryInstitution_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_A'), 'BeneficiaryInstitution_A', '__httpwww_w3schools_com_MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_httpwww_w3schools_comBeneficiaryInstitution_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1141, 4), )

    
    BeneficiaryInstitution_A = property(__BeneficiaryInstitution_A.value, __BeneficiaryInstitution_A.set, None, None)

    
    # Element {http://www.w3schools.com}BeneficiaryInstitution_J uses Python identifier BeneficiaryInstitution_J
    __BeneficiaryInstitution_J = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_J'), 'BeneficiaryInstitution_J', '__httpwww_w3schools_com_MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_httpwww_w3schools_comBeneficiaryInstitution_J', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1142, 4), )

    
    BeneficiaryInstitution_J = property(__BeneficiaryInstitution_J.value, __BeneficiaryInstitution_J.set, None, None)

    _ElementMap.update({
        __CurrencyAmountSold.name() : __CurrencyAmountSold,
        __DeliveryAgent_A.name() : __DeliveryAgent_A,
        __DeliveryAgent_J.name() : __DeliveryAgent_J,
        __Intermediary_A.name() : __Intermediary_A,
        __Intermediary_J.name() : __Intermediary_J,
        __ReceivingAgent_A.name() : __ReceivingAgent_A,
        __ReceivingAgent_J.name() : __ReceivingAgent_J,
        __BeneficiaryInstitution_A.name() : __BeneficiaryInstitution_A,
        __BeneficiaryInstitution_J.name() : __BeneficiaryInstitution_J
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold = MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold', MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold)


# Complex type {http://www.w3schools.com}MT304_SequenceC_OptionalGeneralInformation with content type ELEMENT_ONLY
class MT304_SequenceC_OptionalGeneralInformation (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT304_SequenceC_OptionalGeneralInformation with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceC_OptionalGeneralInformation')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1146, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}ReferenceToTheAssociatedTrade uses Python identifier ReferenceToTheAssociatedTrade
    __ReferenceToTheAssociatedTrade = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ReferenceToTheAssociatedTrade'), 'ReferenceToTheAssociatedTrade', '__httpwww_w3schools_com_MT304_SequenceC_OptionalGeneralInformation_httpwww_w3schools_comReferenceToTheAssociatedTrade', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1148, 3), )

    
    ReferenceToTheAssociatedTrade = property(__ReferenceToTheAssociatedTrade.value, __ReferenceToTheAssociatedTrade.set, None, None)

    
    # Element {http://www.w3schools.com}ExecutingBrokersReference uses Python identifier ExecutingBrokersReference
    __ExecutingBrokersReference = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ExecutingBrokersReference'), 'ExecutingBrokersReference', '__httpwww_w3schools_com_MT304_SequenceC_OptionalGeneralInformation_httpwww_w3schools_comExecutingBrokersReference', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1149, 3), )

    
    ExecutingBrokersReference = property(__ExecutingBrokersReference.value, __ExecutingBrokersReference.set, None, None)

    
    # Element {http://www.w3schools.com}SubsequenceC1_UniqueTransactionIdentifier uses Python identifier SubsequenceC1_UniqueTransactionIdentifier
    __SubsequenceC1_UniqueTransactionIdentifier = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SubsequenceC1_UniqueTransactionIdentifier'), 'SubsequenceC1_UniqueTransactionIdentifier', '__httpwww_w3schools_com_MT304_SequenceC_OptionalGeneralInformation_httpwww_w3schools_comSubsequenceC1_UniqueTransactionIdentifier', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1150, 3), )

    
    SubsequenceC1_UniqueTransactionIdentifier = property(__SubsequenceC1_UniqueTransactionIdentifier.value, __SubsequenceC1_UniqueTransactionIdentifier.set, None, None)

    
    # Element {http://www.w3schools.com}UnderlyingProductIdentifier uses Python identifier UnderlyingProductIdentifier
    __UnderlyingProductIdentifier = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'UnderlyingProductIdentifier'), 'UnderlyingProductIdentifier', '__httpwww_w3schools_com_MT304_SequenceC_OptionalGeneralInformation_httpwww_w3schools_comUnderlyingProductIdentifier', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1151, 3), )

    
    UnderlyingProductIdentifier = property(__UnderlyingProductIdentifier.value, __UnderlyingProductIdentifier.set, None, None)

    
    # Element {http://www.w3schools.com}IdentificationOfFinancialInstrument uses Python identifier IdentificationOfFinancialInstrument
    __IdentificationOfFinancialInstrument = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'IdentificationOfFinancialInstrument'), 'IdentificationOfFinancialInstrument', '__httpwww_w3schools_com_MT304_SequenceC_OptionalGeneralInformation_httpwww_w3schools_comIdentificationOfFinancialInstrument', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1152, 3), )

    
    IdentificationOfFinancialInstrument = property(__IdentificationOfFinancialInstrument.value, __IdentificationOfFinancialInstrument.set, None, None)

    
    # Element {http://www.w3schools.com}ExecutionVenue uses Python identifier ExecutionVenue
    __ExecutionVenue = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ExecutionVenue'), 'ExecutionVenue', '__httpwww_w3schools_com_MT304_SequenceC_OptionalGeneralInformation_httpwww_w3schools_comExecutionVenue', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1153, 3), )

    
    ExecutionVenue = property(__ExecutionVenue.value, __ExecutionVenue.set, None, None)

    
    # Element {http://www.w3schools.com}ExecutionTimestamp uses Python identifier ExecutionTimestamp
    __ExecutionTimestamp = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ExecutionTimestamp'), 'ExecutionTimestamp', '__httpwww_w3schools_com_MT304_SequenceC_OptionalGeneralInformation_httpwww_w3schools_comExecutionTimestamp', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1154, 3), )

    
    ExecutionTimestamp = property(__ExecutionTimestamp.value, __ExecutionTimestamp.set, None, None)

    
    # Element {http://www.w3schools.com}ClearingTimestamp uses Python identifier ClearingTimestamp
    __ClearingTimestamp = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ClearingTimestamp'), 'ClearingTimestamp', '__httpwww_w3schools_com_MT304_SequenceC_OptionalGeneralInformation_httpwww_w3schools_comClearingTimestamp', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1155, 3), )

    
    ClearingTimestamp = property(__ClearingTimestamp.value, __ClearingTimestamp.set, None, None)

    
    # Element {http://www.w3schools.com}ContactInformation uses Python identifier ContactInformation
    __ContactInformation = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ContactInformation'), 'ContactInformation', '__httpwww_w3schools_com_MT304_SequenceC_OptionalGeneralInformation_httpwww_w3schools_comContactInformation', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1156, 3), )

    
    ContactInformation = property(__ContactInformation.value, __ContactInformation.set, None, None)

    
    # Element {http://www.w3schools.com}CommissionAndFees uses Python identifier CommissionAndFees
    __CommissionAndFees = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'CommissionAndFees'), 'CommissionAndFees', '__httpwww_w3schools_com_MT304_SequenceC_OptionalGeneralInformation_httpwww_w3schools_comCommissionAndFees', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1157, 3), )

    
    CommissionAndFees = property(__CommissionAndFees.value, __CommissionAndFees.set, None, None)

    
    # Element {http://www.w3schools.com}SenderToReceiverInformation uses Python identifier SenderToReceiverInformation
    __SenderToReceiverInformation = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SenderToReceiverInformation'), 'SenderToReceiverInformation', '__httpwww_w3schools_com_MT304_SequenceC_OptionalGeneralInformation_httpwww_w3schools_comSenderToReceiverInformation', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1158, 3), )

    
    SenderToReceiverInformation = property(__SenderToReceiverInformation.value, __SenderToReceiverInformation.set, None, None)

    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT304_SequenceC_OptionalGeneralInformation_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='15C')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1160, 2)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1160, 2)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT304_SequenceC_OptionalGeneralInformation_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1161, 2)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1161, 2)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    
    # Attribute formatTag uses Python identifier formatTag
    __formatTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'formatTag'), 'formatTag', '__httpwww_w3schools_com_MT304_SequenceC_OptionalGeneralInformation_formatTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='False')
    __formatTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1162, 2)
    __formatTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1162, 2)
    
    formatTag = property(__formatTag.value, __formatTag.set, None, None)

    _ElementMap.update({
        __ReferenceToTheAssociatedTrade.name() : __ReferenceToTheAssociatedTrade,
        __ExecutingBrokersReference.name() : __ExecutingBrokersReference,
        __SubsequenceC1_UniqueTransactionIdentifier.name() : __SubsequenceC1_UniqueTransactionIdentifier,
        __UnderlyingProductIdentifier.name() : __UnderlyingProductIdentifier,
        __IdentificationOfFinancialInstrument.name() : __IdentificationOfFinancialInstrument,
        __ExecutionVenue.name() : __ExecutionVenue,
        __ExecutionTimestamp.name() : __ExecutionTimestamp,
        __ClearingTimestamp.name() : __ClearingTimestamp,
        __ContactInformation.name() : __ContactInformation,
        __CommissionAndFees.name() : __CommissionAndFees,
        __SenderToReceiverInformation.name() : __SenderToReceiverInformation
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory,
        __formatTag.name() : __formatTag
    })
_module_typeBindings.MT304_SequenceC_OptionalGeneralInformation = MT304_SequenceC_OptionalGeneralInformation
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceC_OptionalGeneralInformation', MT304_SequenceC_OptionalGeneralInformation)


# Complex type {http://www.w3schools.com}MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier with content type ELEMENT_ONLY
class MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1164, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}ReportingJurisdiction uses Python identifier ReportingJurisdiction
    __ReportingJurisdiction = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ReportingJurisdiction'), 'ReportingJurisdiction', '__httpwww_w3schools_com_MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_httpwww_w3schools_comReportingJurisdiction', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1166, 3), )

    
    ReportingJurisdiction = property(__ReportingJurisdiction.value, __ReportingJurisdiction.set, None, None)

    
    # Element {http://www.w3schools.com}UTINamespaceIssuerCode uses Python identifier UTINamespaceIssuerCode
    __UTINamespaceIssuerCode = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'UTINamespaceIssuerCode'), 'UTINamespaceIssuerCode', '__httpwww_w3schools_com_MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_httpwww_w3schools_comUTINamespaceIssuerCode', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1167, 3), )

    
    UTINamespaceIssuerCode = property(__UTINamespaceIssuerCode.value, __UTINamespaceIssuerCode.set, None, None)

    
    # Element {http://www.w3schools.com}TransactionIdentifier uses Python identifier TransactionIdentifier
    __TransactionIdentifier = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'TransactionIdentifier'), 'TransactionIdentifier', '__httpwww_w3schools_com_MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_httpwww_w3schools_comTransactionIdentifier', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1168, 3), )

    
    TransactionIdentifier = property(__TransactionIdentifier.value, __TransactionIdentifier.set, None, None)

    
    # Element {http://www.w3schools.com}SubsequenceC1a_PriorUniqueTransactionIdentifier uses Python identifier SubsequenceC1a_PriorUniqueTransactionIdentifier
    __SubsequenceC1a_PriorUniqueTransactionIdentifier = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SubsequenceC1a_PriorUniqueTransactionIdentifier'), 'SubsequenceC1a_PriorUniqueTransactionIdentifier', '__httpwww_w3schools_com_MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_httpwww_w3schools_comSubsequenceC1a_PriorUniqueTransactionIdentifier', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1169, 3), )

    
    SubsequenceC1a_PriorUniqueTransactionIdentifier = property(__SubsequenceC1a_PriorUniqueTransactionIdentifier.value, __SubsequenceC1a_PriorUniqueTransactionIdentifier.set, None, None)

    _ElementMap.update({
        __ReportingJurisdiction.name() : __ReportingJurisdiction,
        __UTINamespaceIssuerCode.name() : __UTINamespaceIssuerCode,
        __TransactionIdentifier.name() : __TransactionIdentifier,
        __SubsequenceC1a_PriorUniqueTransactionIdentifier.name() : __SubsequenceC1a_PriorUniqueTransactionIdentifier
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier = MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier', MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier)


# Complex type {http://www.w3schools.com}MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_SubsequenceC1a_PriorUniqueTransactionIdentifier with content type ELEMENT_ONLY
class MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_SubsequenceC1a_PriorUniqueTransactionIdentifier (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_SubsequenceC1a_PriorUniqueTransactionIdentifier with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_SubsequenceC1a_PriorUniqueTransactionIdentifier')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1172, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}PUTINamespaceIssuerCode uses Python identifier PUTINamespaceIssuerCode
    __PUTINamespaceIssuerCode = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PUTINamespaceIssuerCode'), 'PUTINamespaceIssuerCode', '__httpwww_w3schools_com_MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_SubsequenceC1a_PriorUniqueTransactionIdentifier_httpwww_w3schools_comPUTINamespaceIssuerCode', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1174, 3), )

    
    PUTINamespaceIssuerCode = property(__PUTINamespaceIssuerCode.value, __PUTINamespaceIssuerCode.set, None, None)

    
    # Element {http://www.w3schools.com}PriorTransactionIdentifier uses Python identifier PriorTransactionIdentifier
    __PriorTransactionIdentifier = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PriorTransactionIdentifier'), 'PriorTransactionIdentifier', '__httpwww_w3schools_com_MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_SubsequenceC1a_PriorUniqueTransactionIdentifier_httpwww_w3schools_comPriorTransactionIdentifier', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1175, 3), )

    
    PriorTransactionIdentifier = property(__PriorTransactionIdentifier.value, __PriorTransactionIdentifier.set, None, None)

    _ElementMap.update({
        __PUTINamespaceIssuerCode.name() : __PUTINamespaceIssuerCode,
        __PriorTransactionIdentifier.name() : __PriorTransactionIdentifier
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_SubsequenceC1a_PriorUniqueTransactionIdentifier = MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_SubsequenceC1a_PriorUniqueTransactionIdentifier
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_SubsequenceC1a_PriorUniqueTransactionIdentifier', MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_SubsequenceC1a_PriorUniqueTransactionIdentifier)


# Complex type {http://www.w3schools.com}MT304_SequenceD_AccountingInformation with content type ELEMENT_ONLY
class MT304_SequenceD_AccountingInformation (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT304_SequenceD_AccountingInformation with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceD_AccountingInformation')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1178, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}ReferenceToPreviousDeals uses Python identifier ReferenceToPreviousDeals
    __ReferenceToPreviousDeals = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ReferenceToPreviousDeals'), 'ReferenceToPreviousDeals', '__httpwww_w3schools_com_MT304_SequenceD_AccountingInformation_httpwww_w3schools_comReferenceToPreviousDeals', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1180, 3), )

    
    ReferenceToPreviousDeals = property(__ReferenceToPreviousDeals.value, __ReferenceToPreviousDeals.set, None, None)

    
    # Element {http://www.w3schools.com}GainIndicator uses Python identifier GainIndicator
    __GainIndicator = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'GainIndicator'), 'GainIndicator', '__httpwww_w3schools_com_MT304_SequenceD_AccountingInformation_httpwww_w3schools_comGainIndicator', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1181, 3), )

    
    GainIndicator = property(__GainIndicator.value, __GainIndicator.set, None, None)

    
    # Element {http://www.w3schools.com}CurrencyAmount uses Python identifier CurrencyAmount
    __CurrencyAmount = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'CurrencyAmount'), 'CurrencyAmount', '__httpwww_w3schools_com_MT304_SequenceD_AccountingInformation_httpwww_w3schools_comCurrencyAmount', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1182, 3), )

    
    CurrencyAmount = property(__CurrencyAmount.value, __CurrencyAmount.set, None, None)

    
    # Element {http://www.w3schools.com}CommissionAndFeesCurrencyAndAmount uses Python identifier CommissionAndFeesCurrencyAndAmount
    __CommissionAndFeesCurrencyAndAmount = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'CommissionAndFeesCurrencyAndAmount'), 'CommissionAndFeesCurrencyAndAmount', '__httpwww_w3schools_com_MT304_SequenceD_AccountingInformation_httpwww_w3schools_comCommissionAndFeesCurrencyAndAmount', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1183, 3), )

    
    CommissionAndFeesCurrencyAndAmount = property(__CommissionAndFeesCurrencyAndAmount.value, __CommissionAndFeesCurrencyAndAmount.set, None, None)

    
    # Element {http://www.w3schools.com}CommissionAndFeesSettlementDate uses Python identifier CommissionAndFeesSettlementDate
    __CommissionAndFeesSettlementDate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'CommissionAndFeesSettlementDate'), 'CommissionAndFeesSettlementDate', '__httpwww_w3schools_com_MT304_SequenceD_AccountingInformation_httpwww_w3schools_comCommissionAndFeesSettlementDate', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1184, 3), )

    
    CommissionAndFeesSettlementDate = property(__CommissionAndFeesSettlementDate.value, __CommissionAndFeesSettlementDate.set, None, None)

    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT304_SequenceD_AccountingInformation_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='15D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1186, 2)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1186, 2)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT304_SequenceD_AccountingInformation_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1187, 2)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1187, 2)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    
    # Attribute formatTag uses Python identifier formatTag
    __formatTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'formatTag'), 'formatTag', '__httpwww_w3schools_com_MT304_SequenceD_AccountingInformation_formatTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='False')
    __formatTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1188, 2)
    __formatTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1188, 2)
    
    formatTag = property(__formatTag.value, __formatTag.set, None, None)

    _ElementMap.update({
        __ReferenceToPreviousDeals.name() : __ReferenceToPreviousDeals,
        __GainIndicator.name() : __GainIndicator,
        __CurrencyAmount.name() : __CurrencyAmount,
        __CommissionAndFeesCurrencyAndAmount.name() : __CommissionAndFeesCurrencyAndAmount,
        __CommissionAndFeesSettlementDate.name() : __CommissionAndFeesSettlementDate
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory,
        __formatTag.name() : __formatTag
    })
_module_typeBindings.MT304_SequenceD_AccountingInformation = MT304_SequenceD_AccountingInformation
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceD_AccountingInformation', MT304_SequenceD_AccountingInformation)


# Complex type {http://www.w3schools.com}MT304_SequenceE_NetAmountToBeSettled with content type ELEMENT_ONLY
class MT304_SequenceE_NetAmountToBeSettled (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT304_SequenceE_NetAmountToBeSettled with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceE_NetAmountToBeSettled')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1190, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}GainIndicator uses Python identifier GainIndicator
    __GainIndicator = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'GainIndicator'), 'GainIndicator', '__httpwww_w3schools_com_MT304_SequenceE_NetAmountToBeSettled_httpwww_w3schools_comGainIndicator', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1192, 3), )

    
    GainIndicator = property(__GainIndicator.value, __GainIndicator.set, None, None)

    
    # Element {http://www.w3schools.com}CurrencyAmount uses Python identifier CurrencyAmount
    __CurrencyAmount = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'CurrencyAmount'), 'CurrencyAmount', '__httpwww_w3schools_com_MT304_SequenceE_NetAmountToBeSettled_httpwww_w3schools_comCurrencyAmount', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1193, 3), )

    
    CurrencyAmount = property(__CurrencyAmount.value, __CurrencyAmount.set, None, None)

    
    # Element {http://www.w3schools.com}DeliveryAgent_A uses Python identifier DeliveryAgent_A
    __DeliveryAgent_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_A'), 'DeliveryAgent_A', '__httpwww_w3schools_com_MT304_SequenceE_NetAmountToBeSettled_httpwww_w3schools_comDeliveryAgent_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1195, 4), )

    
    DeliveryAgent_A = property(__DeliveryAgent_A.value, __DeliveryAgent_A.set, None, None)

    
    # Element {http://www.w3schools.com}DeliveryAgent_D uses Python identifier DeliveryAgent_D
    __DeliveryAgent_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_D'), 'DeliveryAgent_D', '__httpwww_w3schools_com_MT304_SequenceE_NetAmountToBeSettled_httpwww_w3schools_comDeliveryAgent_D', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1196, 4), )

    
    DeliveryAgent_D = property(__DeliveryAgent_D.value, __DeliveryAgent_D.set, None, None)

    
    # Element {http://www.w3schools.com}DeliveryAgent_J uses Python identifier DeliveryAgent_J
    __DeliveryAgent_J = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_J'), 'DeliveryAgent_J', '__httpwww_w3schools_com_MT304_SequenceE_NetAmountToBeSettled_httpwww_w3schools_comDeliveryAgent_J', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1197, 4), )

    
    DeliveryAgent_J = property(__DeliveryAgent_J.value, __DeliveryAgent_J.set, None, None)

    
    # Element {http://www.w3schools.com}Intermediary_A uses Python identifier Intermediary_A
    __Intermediary_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_A'), 'Intermediary_A', '__httpwww_w3schools_com_MT304_SequenceE_NetAmountToBeSettled_httpwww_w3schools_comIntermediary_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1200, 4), )

    
    Intermediary_A = property(__Intermediary_A.value, __Intermediary_A.set, None, None)

    
    # Element {http://www.w3schools.com}Intermediary_D uses Python identifier Intermediary_D
    __Intermediary_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_D'), 'Intermediary_D', '__httpwww_w3schools_com_MT304_SequenceE_NetAmountToBeSettled_httpwww_w3schools_comIntermediary_D', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1201, 4), )

    
    Intermediary_D = property(__Intermediary_D.value, __Intermediary_D.set, None, None)

    
    # Element {http://www.w3schools.com}Intermediary_J uses Python identifier Intermediary_J
    __Intermediary_J = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_J'), 'Intermediary_J', '__httpwww_w3schools_com_MT304_SequenceE_NetAmountToBeSettled_httpwww_w3schools_comIntermediary_J', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1202, 4), )

    
    Intermediary_J = property(__Intermediary_J.value, __Intermediary_J.set, None, None)

    
    # Element {http://www.w3schools.com}ReceivingAgent_A uses Python identifier ReceivingAgent_A
    __ReceivingAgent_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_A'), 'ReceivingAgent_A', '__httpwww_w3schools_com_MT304_SequenceE_NetAmountToBeSettled_httpwww_w3schools_comReceivingAgent_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1205, 4), )

    
    ReceivingAgent_A = property(__ReceivingAgent_A.value, __ReceivingAgent_A.set, None, None)

    
    # Element {http://www.w3schools.com}ReceivingAgent_D uses Python identifier ReceivingAgent_D
    __ReceivingAgent_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_D'), 'ReceivingAgent_D', '__httpwww_w3schools_com_MT304_SequenceE_NetAmountToBeSettled_httpwww_w3schools_comReceivingAgent_D', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1206, 4), )

    
    ReceivingAgent_D = property(__ReceivingAgent_D.value, __ReceivingAgent_D.set, None, None)

    
    # Element {http://www.w3schools.com}ReceivingAgent_J uses Python identifier ReceivingAgent_J
    __ReceivingAgent_J = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_J'), 'ReceivingAgent_J', '__httpwww_w3schools_com_MT304_SequenceE_NetAmountToBeSettled_httpwww_w3schools_comReceivingAgent_J', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1207, 4), )

    
    ReceivingAgent_J = property(__ReceivingAgent_J.value, __ReceivingAgent_J.set, None, None)

    
    # Element {http://www.w3schools.com}BeneficiaryInstitution_A uses Python identifier BeneficiaryInstitution_A
    __BeneficiaryInstitution_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_A'), 'BeneficiaryInstitution_A', '__httpwww_w3schools_com_MT304_SequenceE_NetAmountToBeSettled_httpwww_w3schools_comBeneficiaryInstitution_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1210, 4), )

    
    BeneficiaryInstitution_A = property(__BeneficiaryInstitution_A.value, __BeneficiaryInstitution_A.set, None, None)

    
    # Element {http://www.w3schools.com}BeneficiaryInstitution_D uses Python identifier BeneficiaryInstitution_D
    __BeneficiaryInstitution_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_D'), 'BeneficiaryInstitution_D', '__httpwww_w3schools_com_MT304_SequenceE_NetAmountToBeSettled_httpwww_w3schools_comBeneficiaryInstitution_D', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1211, 4), )

    
    BeneficiaryInstitution_D = property(__BeneficiaryInstitution_D.value, __BeneficiaryInstitution_D.set, None, None)

    
    # Element {http://www.w3schools.com}BeneficiaryInstitution_J uses Python identifier BeneficiaryInstitution_J
    __BeneficiaryInstitution_J = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_J'), 'BeneficiaryInstitution_J', '__httpwww_w3schools_com_MT304_SequenceE_NetAmountToBeSettled_httpwww_w3schools_comBeneficiaryInstitution_J', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1212, 4), )

    
    BeneficiaryInstitution_J = property(__BeneficiaryInstitution_J.value, __BeneficiaryInstitution_J.set, None, None)

    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT304_SequenceE_NetAmountToBeSettled_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='15E')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1215, 2)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1215, 2)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT304_SequenceE_NetAmountToBeSettled_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1216, 2)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1216, 2)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    
    # Attribute formatTag uses Python identifier formatTag
    __formatTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'formatTag'), 'formatTag', '__httpwww_w3schools_com_MT304_SequenceE_NetAmountToBeSettled_formatTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='False')
    __formatTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1217, 2)
    __formatTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1217, 2)
    
    formatTag = property(__formatTag.value, __formatTag.set, None, None)

    _ElementMap.update({
        __GainIndicator.name() : __GainIndicator,
        __CurrencyAmount.name() : __CurrencyAmount,
        __DeliveryAgent_A.name() : __DeliveryAgent_A,
        __DeliveryAgent_D.name() : __DeliveryAgent_D,
        __DeliveryAgent_J.name() : __DeliveryAgent_J,
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
_module_typeBindings.MT304_SequenceE_NetAmountToBeSettled = MT304_SequenceE_NetAmountToBeSettled
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceE_NetAmountToBeSettled', MT304_SequenceE_NetAmountToBeSettled)


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1220, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}SequenceA_GeneralInformation uses Python identifier SequenceA_GeneralInformation
    __SequenceA_GeneralInformation = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SequenceA_GeneralInformation'), 'SequenceA_GeneralInformation', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comSequenceA_GeneralInformation', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1222, 4), )

    
    SequenceA_GeneralInformation = property(__SequenceA_GeneralInformation.value, __SequenceA_GeneralInformation.set, None, None)

    
    # Element {http://www.w3schools.com}SequenceB_ForexTransactionDetails uses Python identifier SequenceB_ForexTransactionDetails
    __SequenceB_ForexTransactionDetails = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SequenceB_ForexTransactionDetails'), 'SequenceB_ForexTransactionDetails', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comSequenceB_ForexTransactionDetails', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1223, 4), )

    
    SequenceB_ForexTransactionDetails = property(__SequenceB_ForexTransactionDetails.value, __SequenceB_ForexTransactionDetails.set, None, None)

    
    # Element {http://www.w3schools.com}SequenceC_OptionalGeneralInformation uses Python identifier SequenceC_OptionalGeneralInformation
    __SequenceC_OptionalGeneralInformation = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SequenceC_OptionalGeneralInformation'), 'SequenceC_OptionalGeneralInformation', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comSequenceC_OptionalGeneralInformation', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1224, 4), )

    
    SequenceC_OptionalGeneralInformation = property(__SequenceC_OptionalGeneralInformation.value, __SequenceC_OptionalGeneralInformation.set, None, None)

    
    # Element {http://www.w3schools.com}SequenceD_AccountingInformation uses Python identifier SequenceD_AccountingInformation
    __SequenceD_AccountingInformation = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SequenceD_AccountingInformation'), 'SequenceD_AccountingInformation', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comSequenceD_AccountingInformation', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1225, 4), )

    
    SequenceD_AccountingInformation = property(__SequenceD_AccountingInformation.value, __SequenceD_AccountingInformation.set, None, None)

    
    # Element {http://www.w3schools.com}SequenceE_NetAmountToBeSettled uses Python identifier SequenceE_NetAmountToBeSettled
    __SequenceE_NetAmountToBeSettled = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SequenceE_NetAmountToBeSettled'), 'SequenceE_NetAmountToBeSettled', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comSequenceE_NetAmountToBeSettled', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1226, 4), )

    
    SequenceE_NetAmountToBeSettled = property(__SequenceE_NetAmountToBeSettled.value, __SequenceE_NetAmountToBeSettled.set, None, None)

    _ElementMap.update({
        __SequenceA_GeneralInformation.name() : __SequenceA_GeneralInformation,
        __SequenceB_ForexTransactionDetails.name() : __SequenceB_ForexTransactionDetails,
        __SequenceC_OptionalGeneralInformation.name() : __SequenceC_OptionalGeneralInformation,
        __SequenceD_AccountingInformation.name() : __SequenceD_AccountingInformation,
        __SequenceE_NetAmountToBeSettled.name() : __SequenceE_NetAmountToBeSettled
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON = CTD_ANON


# Complex type {http://www.w3schools.com}MT304_SequenceA_GeneralInformation_20_Type with content type SIMPLE
class MT304_SequenceA_GeneralInformation_20_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT304_SequenceA_GeneralInformation_20_Type with content type SIMPLE"""
    _TypeDefinition = MT304_SequenceA_GeneralInformation_20_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceA_GeneralInformation_20_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 8, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT304_SequenceA_GeneralInformation_20_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT304_SequenceA_GeneralInformation_20_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='20')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 11, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 11, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT304_SequenceA_GeneralInformation_20_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 12, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 12, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT304_SequenceA_GeneralInformation_20_Type = MT304_SequenceA_GeneralInformation_20_Type
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceA_GeneralInformation_20_Type', MT304_SequenceA_GeneralInformation_20_Type)


# Complex type {http://www.w3schools.com}MT304_SequenceA_GeneralInformation_21_Type with content type SIMPLE
class MT304_SequenceA_GeneralInformation_21_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT304_SequenceA_GeneralInformation_21_Type with content type SIMPLE"""
    _TypeDefinition = MT304_SequenceA_GeneralInformation_21_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceA_GeneralInformation_21_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 21, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT304_SequenceA_GeneralInformation_21_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT304_SequenceA_GeneralInformation_21_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='21')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 24, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 24, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT304_SequenceA_GeneralInformation_21_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 25, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 25, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT304_SequenceA_GeneralInformation_21_Type = MT304_SequenceA_GeneralInformation_21_Type
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceA_GeneralInformation_21_Type', MT304_SequenceA_GeneralInformation_21_Type)


# Complex type {http://www.w3schools.com}MT304_SequenceA_GeneralInformation_22A_Type with content type SIMPLE
class MT304_SequenceA_GeneralInformation_22A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT304_SequenceA_GeneralInformation_22A_Type with content type SIMPLE"""
    _TypeDefinition = MT304_SequenceA_GeneralInformation_22A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceA_GeneralInformation_22A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 34, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT304_SequenceA_GeneralInformation_22A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT304_SequenceA_GeneralInformation_22A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='22A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 37, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 37, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT304_SequenceA_GeneralInformation_22A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 38, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 38, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT304_SequenceA_GeneralInformation_22A_Type = MT304_SequenceA_GeneralInformation_22A_Type
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceA_GeneralInformation_22A_Type', MT304_SequenceA_GeneralInformation_22A_Type)


# Complex type {http://www.w3schools.com}MT304_SequenceA_GeneralInformation_94A_Type with content type SIMPLE
class MT304_SequenceA_GeneralInformation_94A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT304_SequenceA_GeneralInformation_94A_Type with content type SIMPLE"""
    _TypeDefinition = MT304_SequenceA_GeneralInformation_94A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceA_GeneralInformation_94A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 47, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT304_SequenceA_GeneralInformation_94A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT304_SequenceA_GeneralInformation_94A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='94A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 50, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 50, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT304_SequenceA_GeneralInformation_94A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 51, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 51, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT304_SequenceA_GeneralInformation_94A_Type = MT304_SequenceA_GeneralInformation_94A_Type
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceA_GeneralInformation_94A_Type', MT304_SequenceA_GeneralInformation_94A_Type)


# Complex type {http://www.w3schools.com}MT304_SequenceA_GeneralInformation_17O_Type with content type SIMPLE
class MT304_SequenceA_GeneralInformation_17O_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT304_SequenceA_GeneralInformation_17O_Type with content type SIMPLE"""
    _TypeDefinition = MT304_SequenceA_GeneralInformation_17O_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceA_GeneralInformation_17O_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 60, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT304_SequenceA_GeneralInformation_17O_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT304_SequenceA_GeneralInformation_17O_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='17O')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 63, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 63, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT304_SequenceA_GeneralInformation_17O_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 64, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 64, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT304_SequenceA_GeneralInformation_17O_Type = MT304_SequenceA_GeneralInformation_17O_Type
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceA_GeneralInformation_17O_Type', MT304_SequenceA_GeneralInformation_17O_Type)


# Complex type {http://www.w3schools.com}MT304_SequenceA_GeneralInformation_17F_Type with content type SIMPLE
class MT304_SequenceA_GeneralInformation_17F_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT304_SequenceA_GeneralInformation_17F_Type with content type SIMPLE"""
    _TypeDefinition = MT304_SequenceA_GeneralInformation_17F_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceA_GeneralInformation_17F_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 73, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT304_SequenceA_GeneralInformation_17F_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT304_SequenceA_GeneralInformation_17F_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='17F')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 76, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 76, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT304_SequenceA_GeneralInformation_17F_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 77, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 77, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT304_SequenceA_GeneralInformation_17F_Type = MT304_SequenceA_GeneralInformation_17F_Type
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceA_GeneralInformation_17F_Type', MT304_SequenceA_GeneralInformation_17F_Type)


# Complex type {http://www.w3schools.com}MT304_SequenceA_GeneralInformation_17N_Type with content type SIMPLE
class MT304_SequenceA_GeneralInformation_17N_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT304_SequenceA_GeneralInformation_17N_Type with content type SIMPLE"""
    _TypeDefinition = MT304_SequenceA_GeneralInformation_17N_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceA_GeneralInformation_17N_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 86, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT304_SequenceA_GeneralInformation_17N_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT304_SequenceA_GeneralInformation_17N_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='17N')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 89, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 89, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT304_SequenceA_GeneralInformation_17N_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 90, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 90, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT304_SequenceA_GeneralInformation_17N_Type = MT304_SequenceA_GeneralInformation_17N_Type
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceA_GeneralInformation_17N_Type', MT304_SequenceA_GeneralInformation_17N_Type)


# Complex type {http://www.w3schools.com}MT304_SequenceA_GeneralInformation_83A_Type with content type SIMPLE
class MT304_SequenceA_GeneralInformation_83A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT304_SequenceA_GeneralInformation_83A_Type with content type SIMPLE"""
    _TypeDefinition = MT304_SequenceA_GeneralInformation_83A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceA_GeneralInformation_83A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 99, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT304_SequenceA_GeneralInformation_83A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT304_SequenceA_GeneralInformation_83A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='83A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 102, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 102, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT304_SequenceA_GeneralInformation_83A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 103, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 103, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT304_SequenceA_GeneralInformation_83A_Type = MT304_SequenceA_GeneralInformation_83A_Type
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceA_GeneralInformation_83A_Type', MT304_SequenceA_GeneralInformation_83A_Type)


# Complex type {http://www.w3schools.com}MT304_SequenceA_GeneralInformation_83J_Type with content type SIMPLE
class MT304_SequenceA_GeneralInformation_83J_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT304_SequenceA_GeneralInformation_83J_Type with content type SIMPLE"""
    _TypeDefinition = MT304_SequenceA_GeneralInformation_83J_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceA_GeneralInformation_83J_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 112, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT304_SequenceA_GeneralInformation_83J_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT304_SequenceA_GeneralInformation_83J_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='83J')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 115, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 115, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT304_SequenceA_GeneralInformation_83J_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 116, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 116, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT304_SequenceA_GeneralInformation_83J_Type = MT304_SequenceA_GeneralInformation_83J_Type
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceA_GeneralInformation_83J_Type', MT304_SequenceA_GeneralInformation_83J_Type)


# Complex type {http://www.w3schools.com}MT304_SequenceA_GeneralInformation_82A_Type with content type SIMPLE
class MT304_SequenceA_GeneralInformation_82A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT304_SequenceA_GeneralInformation_82A_Type with content type SIMPLE"""
    _TypeDefinition = MT304_SequenceA_GeneralInformation_82A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceA_GeneralInformation_82A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 125, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT304_SequenceA_GeneralInformation_82A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT304_SequenceA_GeneralInformation_82A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='82A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 128, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 128, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT304_SequenceA_GeneralInformation_82A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 129, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 129, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT304_SequenceA_GeneralInformation_82A_Type = MT304_SequenceA_GeneralInformation_82A_Type
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceA_GeneralInformation_82A_Type', MT304_SequenceA_GeneralInformation_82A_Type)


# Complex type {http://www.w3schools.com}MT304_SequenceA_GeneralInformation_82J_Type with content type SIMPLE
class MT304_SequenceA_GeneralInformation_82J_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT304_SequenceA_GeneralInformation_82J_Type with content type SIMPLE"""
    _TypeDefinition = MT304_SequenceA_GeneralInformation_82J_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceA_GeneralInformation_82J_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 138, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT304_SequenceA_GeneralInformation_82J_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT304_SequenceA_GeneralInformation_82J_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='82J')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 141, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 141, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT304_SequenceA_GeneralInformation_82J_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 142, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 142, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT304_SequenceA_GeneralInformation_82J_Type = MT304_SequenceA_GeneralInformation_82J_Type
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceA_GeneralInformation_82J_Type', MT304_SequenceA_GeneralInformation_82J_Type)


# Complex type {http://www.w3schools.com}MT304_SequenceA_GeneralInformation_87A_Type with content type SIMPLE
class MT304_SequenceA_GeneralInformation_87A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT304_SequenceA_GeneralInformation_87A_Type with content type SIMPLE"""
    _TypeDefinition = MT304_SequenceA_GeneralInformation_87A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceA_GeneralInformation_87A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 151, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT304_SequenceA_GeneralInformation_87A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT304_SequenceA_GeneralInformation_87A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='87A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 154, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 154, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT304_SequenceA_GeneralInformation_87A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 155, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 155, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT304_SequenceA_GeneralInformation_87A_Type = MT304_SequenceA_GeneralInformation_87A_Type
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceA_GeneralInformation_87A_Type', MT304_SequenceA_GeneralInformation_87A_Type)


# Complex type {http://www.w3schools.com}MT304_SequenceA_GeneralInformation_87J_Type with content type SIMPLE
class MT304_SequenceA_GeneralInformation_87J_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT304_SequenceA_GeneralInformation_87J_Type with content type SIMPLE"""
    _TypeDefinition = MT304_SequenceA_GeneralInformation_87J_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceA_GeneralInformation_87J_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 164, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT304_SequenceA_GeneralInformation_87J_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT304_SequenceA_GeneralInformation_87J_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='87J')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 167, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 167, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT304_SequenceA_GeneralInformation_87J_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 168, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 168, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT304_SequenceA_GeneralInformation_87J_Type = MT304_SequenceA_GeneralInformation_87J_Type
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceA_GeneralInformation_87J_Type', MT304_SequenceA_GeneralInformation_87J_Type)


# Complex type {http://www.w3schools.com}MT304_SequenceA_GeneralInformation_81A_Type with content type SIMPLE
class MT304_SequenceA_GeneralInformation_81A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT304_SequenceA_GeneralInformation_81A_Type with content type SIMPLE"""
    _TypeDefinition = MT304_SequenceA_GeneralInformation_81A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceA_GeneralInformation_81A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 177, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT304_SequenceA_GeneralInformation_81A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT304_SequenceA_GeneralInformation_81A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='81A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 180, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 180, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT304_SequenceA_GeneralInformation_81A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 181, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 181, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT304_SequenceA_GeneralInformation_81A_Type = MT304_SequenceA_GeneralInformation_81A_Type
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceA_GeneralInformation_81A_Type', MT304_SequenceA_GeneralInformation_81A_Type)


# Complex type {http://www.w3schools.com}MT304_SequenceA_GeneralInformation_81D_Type with content type SIMPLE
class MT304_SequenceA_GeneralInformation_81D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT304_SequenceA_GeneralInformation_81D_Type with content type SIMPLE"""
    _TypeDefinition = MT304_SequenceA_GeneralInformation_81D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceA_GeneralInformation_81D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 190, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT304_SequenceA_GeneralInformation_81D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT304_SequenceA_GeneralInformation_81D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='81D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 193, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 193, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT304_SequenceA_GeneralInformation_81D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 194, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 194, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT304_SequenceA_GeneralInformation_81D_Type = MT304_SequenceA_GeneralInformation_81D_Type
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceA_GeneralInformation_81D_Type', MT304_SequenceA_GeneralInformation_81D_Type)


# Complex type {http://www.w3schools.com}MT304_SequenceA_GeneralInformation_81J_Type with content type SIMPLE
class MT304_SequenceA_GeneralInformation_81J_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT304_SequenceA_GeneralInformation_81J_Type with content type SIMPLE"""
    _TypeDefinition = MT304_SequenceA_GeneralInformation_81J_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceA_GeneralInformation_81J_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 203, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT304_SequenceA_GeneralInformation_81J_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT304_SequenceA_GeneralInformation_81J_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='81J')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 206, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 206, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT304_SequenceA_GeneralInformation_81J_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 207, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 207, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT304_SequenceA_GeneralInformation_81J_Type = MT304_SequenceA_GeneralInformation_81J_Type
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceA_GeneralInformation_81J_Type', MT304_SequenceA_GeneralInformation_81J_Type)


# Complex type {http://www.w3schools.com}MT304_SequenceA_GeneralInformation_89A_Type with content type SIMPLE
class MT304_SequenceA_GeneralInformation_89A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT304_SequenceA_GeneralInformation_89A_Type with content type SIMPLE"""
    _TypeDefinition = MT304_SequenceA_GeneralInformation_89A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceA_GeneralInformation_89A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 216, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT304_SequenceA_GeneralInformation_89A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT304_SequenceA_GeneralInformation_89A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='89A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 219, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 219, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT304_SequenceA_GeneralInformation_89A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 220, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 220, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT304_SequenceA_GeneralInformation_89A_Type = MT304_SequenceA_GeneralInformation_89A_Type
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceA_GeneralInformation_89A_Type', MT304_SequenceA_GeneralInformation_89A_Type)


# Complex type {http://www.w3schools.com}MT304_SequenceA_GeneralInformation_89D_Type with content type SIMPLE
class MT304_SequenceA_GeneralInformation_89D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT304_SequenceA_GeneralInformation_89D_Type with content type SIMPLE"""
    _TypeDefinition = MT304_SequenceA_GeneralInformation_89D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceA_GeneralInformation_89D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 229, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT304_SequenceA_GeneralInformation_89D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT304_SequenceA_GeneralInformation_89D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='89D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 232, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 232, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT304_SequenceA_GeneralInformation_89D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 233, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 233, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT304_SequenceA_GeneralInformation_89D_Type = MT304_SequenceA_GeneralInformation_89D_Type
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceA_GeneralInformation_89D_Type', MT304_SequenceA_GeneralInformation_89D_Type)


# Complex type {http://www.w3schools.com}MT304_SequenceA_GeneralInformation_89J_Type with content type SIMPLE
class MT304_SequenceA_GeneralInformation_89J_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT304_SequenceA_GeneralInformation_89J_Type with content type SIMPLE"""
    _TypeDefinition = MT304_SequenceA_GeneralInformation_89J_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceA_GeneralInformation_89J_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 242, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT304_SequenceA_GeneralInformation_89J_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT304_SequenceA_GeneralInformation_89J_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='89J')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 245, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 245, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT304_SequenceA_GeneralInformation_89J_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 246, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 246, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT304_SequenceA_GeneralInformation_89J_Type = MT304_SequenceA_GeneralInformation_89J_Type
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceA_GeneralInformation_89J_Type', MT304_SequenceA_GeneralInformation_89J_Type)


# Complex type {http://www.w3schools.com}MT304_SequenceA_GeneralInformation_17I_Type with content type SIMPLE
class MT304_SequenceA_GeneralInformation_17I_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT304_SequenceA_GeneralInformation_17I_Type with content type SIMPLE"""
    _TypeDefinition = MT304_SequenceA_GeneralInformation_17I_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceA_GeneralInformation_17I_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 255, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT304_SequenceA_GeneralInformation_17I_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT304_SequenceA_GeneralInformation_17I_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='17I')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 258, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 258, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT304_SequenceA_GeneralInformation_17I_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 259, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 259, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT304_SequenceA_GeneralInformation_17I_Type = MT304_SequenceA_GeneralInformation_17I_Type
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceA_GeneralInformation_17I_Type', MT304_SequenceA_GeneralInformation_17I_Type)


# Complex type {http://www.w3schools.com}MT304_SequenceA_GeneralInformation_77H_Type with content type SIMPLE
class MT304_SequenceA_GeneralInformation_77H_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT304_SequenceA_GeneralInformation_77H_Type with content type SIMPLE"""
    _TypeDefinition = MT304_SequenceA_GeneralInformation_77H_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceA_GeneralInformation_77H_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 268, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT304_SequenceA_GeneralInformation_77H_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT304_SequenceA_GeneralInformation_77H_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='77H')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 271, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 271, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT304_SequenceA_GeneralInformation_77H_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 272, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 272, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT304_SequenceA_GeneralInformation_77H_Type = MT304_SequenceA_GeneralInformation_77H_Type
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceA_GeneralInformation_77H_Type', MT304_SequenceA_GeneralInformation_77H_Type)


# Complex type {http://www.w3schools.com}MT304_SequenceA_GeneralInformation_14C_Type with content type SIMPLE
class MT304_SequenceA_GeneralInformation_14C_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT304_SequenceA_GeneralInformation_14C_Type with content type SIMPLE"""
    _TypeDefinition = MT304_SequenceA_GeneralInformation_14C_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceA_GeneralInformation_14C_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 281, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT304_SequenceA_GeneralInformation_14C_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT304_SequenceA_GeneralInformation_14C_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='14C')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 284, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 284, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT304_SequenceA_GeneralInformation_14C_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 285, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 285, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT304_SequenceA_GeneralInformation_14C_Type = MT304_SequenceA_GeneralInformation_14C_Type
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceA_GeneralInformation_14C_Type', MT304_SequenceA_GeneralInformation_14C_Type)


# Complex type {http://www.w3schools.com}MT304_SequenceA_GeneralInformation_32E_Type with content type SIMPLE
class MT304_SequenceA_GeneralInformation_32E_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT304_SequenceA_GeneralInformation_32E_Type with content type SIMPLE"""
    _TypeDefinition = MT304_SequenceA_GeneralInformation_32E_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceA_GeneralInformation_32E_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 294, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT304_SequenceA_GeneralInformation_32E_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT304_SequenceA_GeneralInformation_32E_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='32E')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 297, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 297, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT304_SequenceA_GeneralInformation_32E_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 298, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 298, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT304_SequenceA_GeneralInformation_32E_Type = MT304_SequenceA_GeneralInformation_32E_Type
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceA_GeneralInformation_32E_Type', MT304_SequenceA_GeneralInformation_32E_Type)


# Complex type {http://www.w3schools.com}MT304_SequenceA_GeneralInformation_30U_Type with content type SIMPLE
class MT304_SequenceA_GeneralInformation_30U_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT304_SequenceA_GeneralInformation_30U_Type with content type SIMPLE"""
    _TypeDefinition = MT304_SequenceA_GeneralInformation_30U_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceA_GeneralInformation_30U_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 307, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT304_SequenceA_GeneralInformation_30U_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT304_SequenceA_GeneralInformation_30U_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='30U')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 310, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 310, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT304_SequenceA_GeneralInformation_30U_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 311, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 311, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT304_SequenceA_GeneralInformation_30U_Type = MT304_SequenceA_GeneralInformation_30U_Type
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceA_GeneralInformation_30U_Type', MT304_SequenceA_GeneralInformation_30U_Type)


# Complex type {http://www.w3schools.com}MT304_SequenceA_GeneralInformation_14S_Type with content type SIMPLE
class MT304_SequenceA_GeneralInformation_14S_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT304_SequenceA_GeneralInformation_14S_Type with content type SIMPLE"""
    _TypeDefinition = MT304_SequenceA_GeneralInformation_14S_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceA_GeneralInformation_14S_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 320, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT304_SequenceA_GeneralInformation_14S_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT304_SequenceA_GeneralInformation_14S_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='14S')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 323, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 323, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT304_SequenceA_GeneralInformation_14S_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 324, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 324, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT304_SequenceA_GeneralInformation_14S_Type = MT304_SequenceA_GeneralInformation_14S_Type
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceA_GeneralInformation_14S_Type', MT304_SequenceA_GeneralInformation_14S_Type)


# Complex type {http://www.w3schools.com}MT304_SequenceA_GeneralInformation_21A_Type with content type SIMPLE
class MT304_SequenceA_GeneralInformation_21A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT304_SequenceA_GeneralInformation_21A_Type with content type SIMPLE"""
    _TypeDefinition = MT304_SequenceA_GeneralInformation_21A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceA_GeneralInformation_21A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 333, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT304_SequenceA_GeneralInformation_21A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT304_SequenceA_GeneralInformation_21A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='21A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 336, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 336, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT304_SequenceA_GeneralInformation_21A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 337, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 337, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT304_SequenceA_GeneralInformation_21A_Type = MT304_SequenceA_GeneralInformation_21A_Type
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceA_GeneralInformation_21A_Type', MT304_SequenceA_GeneralInformation_21A_Type)


# Complex type {http://www.w3schools.com}MT304_SequenceA_GeneralInformation_14E_Type with content type SIMPLE
class MT304_SequenceA_GeneralInformation_14E_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT304_SequenceA_GeneralInformation_14E_Type with content type SIMPLE"""
    _TypeDefinition = MT304_SequenceA_GeneralInformation_14E_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceA_GeneralInformation_14E_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 346, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT304_SequenceA_GeneralInformation_14E_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT304_SequenceA_GeneralInformation_14E_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='14E')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 349, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 349, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT304_SequenceA_GeneralInformation_14E_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 350, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 350, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT304_SequenceA_GeneralInformation_14E_Type = MT304_SequenceA_GeneralInformation_14E_Type
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceA_GeneralInformation_14E_Type', MT304_SequenceA_GeneralInformation_14E_Type)


# Complex type {http://www.w3schools.com}MT304_SequenceB_ForexTransactionDetails_30T_Type with content type SIMPLE
class MT304_SequenceB_ForexTransactionDetails_30T_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT304_SequenceB_ForexTransactionDetails_30T_Type with content type SIMPLE"""
    _TypeDefinition = MT304_SequenceB_ForexTransactionDetails_30T_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceB_ForexTransactionDetails_30T_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 359, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT304_SequenceB_ForexTransactionDetails_30T_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT304_SequenceB_ForexTransactionDetails_30T_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='30T')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 362, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 362, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT304_SequenceB_ForexTransactionDetails_30T_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 363, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 363, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT304_SequenceB_ForexTransactionDetails_30T_Type = MT304_SequenceB_ForexTransactionDetails_30T_Type
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceB_ForexTransactionDetails_30T_Type', MT304_SequenceB_ForexTransactionDetails_30T_Type)


# Complex type {http://www.w3schools.com}MT304_SequenceB_ForexTransactionDetails_30V_Type with content type SIMPLE
class MT304_SequenceB_ForexTransactionDetails_30V_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT304_SequenceB_ForexTransactionDetails_30V_Type with content type SIMPLE"""
    _TypeDefinition = MT304_SequenceB_ForexTransactionDetails_30V_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceB_ForexTransactionDetails_30V_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 372, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT304_SequenceB_ForexTransactionDetails_30V_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT304_SequenceB_ForexTransactionDetails_30V_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='30V')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 375, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 375, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT304_SequenceB_ForexTransactionDetails_30V_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 376, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 376, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT304_SequenceB_ForexTransactionDetails_30V_Type = MT304_SequenceB_ForexTransactionDetails_30V_Type
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceB_ForexTransactionDetails_30V_Type', MT304_SequenceB_ForexTransactionDetails_30V_Type)


# Complex type {http://www.w3schools.com}MT304_SequenceB_ForexTransactionDetails_36_Type with content type SIMPLE
class MT304_SequenceB_ForexTransactionDetails_36_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT304_SequenceB_ForexTransactionDetails_36_Type with content type SIMPLE"""
    _TypeDefinition = MT304_SequenceB_ForexTransactionDetails_36_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceB_ForexTransactionDetails_36_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 385, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT304_SequenceB_ForexTransactionDetails_36_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT304_SequenceB_ForexTransactionDetails_36_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='36')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 388, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 388, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT304_SequenceB_ForexTransactionDetails_36_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 389, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 389, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT304_SequenceB_ForexTransactionDetails_36_Type = MT304_SequenceB_ForexTransactionDetails_36_Type
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceB_ForexTransactionDetails_36_Type', MT304_SequenceB_ForexTransactionDetails_36_Type)


# Complex type {http://www.w3schools.com}MT304_SequenceB_ForexTransactionDetails_39M_Type with content type SIMPLE
class MT304_SequenceB_ForexTransactionDetails_39M_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT304_SequenceB_ForexTransactionDetails_39M_Type with content type SIMPLE"""
    _TypeDefinition = MT304_SequenceB_ForexTransactionDetails_39M_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceB_ForexTransactionDetails_39M_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 398, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT304_SequenceB_ForexTransactionDetails_39M_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT304_SequenceB_ForexTransactionDetails_39M_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='39M')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 401, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 401, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT304_SequenceB_ForexTransactionDetails_39M_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 402, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 402, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT304_SequenceB_ForexTransactionDetails_39M_Type = MT304_SequenceB_ForexTransactionDetails_39M_Type
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceB_ForexTransactionDetails_39M_Type', MT304_SequenceB_ForexTransactionDetails_39M_Type)


# Complex type {http://www.w3schools.com}MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_32B_Type with content type SIMPLE
class MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_32B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_32B_Type with content type SIMPLE"""
    _TypeDefinition = MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_32B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_32B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 411, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_32B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_32B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='32B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 414, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 414, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_32B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 415, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 415, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_32B_Type = MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_32B_Type
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_32B_Type', MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_32B_Type)


# Complex type {http://www.w3schools.com}MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_53A_Type with content type SIMPLE
class MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_53A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_53A_Type with content type SIMPLE"""
    _TypeDefinition = MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_53A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_53A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 424, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_53A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_53A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='53A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 427, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 427, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_53A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 428, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 428, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_53A_Type = MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_53A_Type
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_53A_Type', MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_53A_Type)


# Complex type {http://www.w3schools.com}MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_53J_Type with content type SIMPLE
class MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_53J_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_53J_Type with content type SIMPLE"""
    _TypeDefinition = MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_53J_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_53J_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 437, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_53J_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_53J_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='53J')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 440, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 440, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_53J_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 441, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 441, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_53J_Type = MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_53J_Type
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_53J_Type', MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_53J_Type)


# Complex type {http://www.w3schools.com}MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_56A_Type with content type SIMPLE
class MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_56A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_56A_Type with content type SIMPLE"""
    _TypeDefinition = MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_56A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_56A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 450, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_56A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_56A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='56A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 453, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 453, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_56A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 454, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 454, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_56A_Type = MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_56A_Type
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_56A_Type', MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_56A_Type)


# Complex type {http://www.w3schools.com}MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_56J_Type with content type SIMPLE
class MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_56J_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_56J_Type with content type SIMPLE"""
    _TypeDefinition = MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_56J_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_56J_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 463, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_56J_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_56J_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='56J')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 466, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 466, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_56J_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 467, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 467, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_56J_Type = MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_56J_Type
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_56J_Type', MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_56J_Type)


# Complex type {http://www.w3schools.com}MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_57A_Type with content type SIMPLE
class MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_57A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_57A_Type with content type SIMPLE"""
    _TypeDefinition = MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_57A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_57A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 476, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_57A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_57A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='57A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 479, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 479, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_57A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 480, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 480, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_57A_Type = MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_57A_Type
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_57A_Type', MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_57A_Type)


# Complex type {http://www.w3schools.com}MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_57J_Type with content type SIMPLE
class MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_57J_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_57J_Type with content type SIMPLE"""
    _TypeDefinition = MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_57J_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_57J_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 489, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_57J_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_57J_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='57J')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 492, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 492, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_57J_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 493, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 493, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_57J_Type = MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_57J_Type
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_57J_Type', MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_57J_Type)


# Complex type {http://www.w3schools.com}MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_33B_Type with content type SIMPLE
class MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_33B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_33B_Type with content type SIMPLE"""
    _TypeDefinition = MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_33B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_33B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 502, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_33B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_33B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='33B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 505, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 505, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_33B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 506, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 506, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_33B_Type = MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_33B_Type
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_33B_Type', MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_33B_Type)


# Complex type {http://www.w3schools.com}MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_53A_Type with content type SIMPLE
class MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_53A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_53A_Type with content type SIMPLE"""
    _TypeDefinition = MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_53A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_53A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 515, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_53A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_53A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='53A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 518, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 518, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_53A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 519, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 519, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_53A_Type = MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_53A_Type
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_53A_Type', MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_53A_Type)


# Complex type {http://www.w3schools.com}MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_53J_Type with content type SIMPLE
class MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_53J_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_53J_Type with content type SIMPLE"""
    _TypeDefinition = MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_53J_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_53J_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 528, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_53J_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_53J_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='53J')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 531, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 531, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_53J_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 532, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 532, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_53J_Type = MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_53J_Type
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_53J_Type', MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_53J_Type)


# Complex type {http://www.w3schools.com}MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_56A_Type with content type SIMPLE
class MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_56A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_56A_Type with content type SIMPLE"""
    _TypeDefinition = MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_56A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_56A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 541, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_56A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_56A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='56A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 544, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 544, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_56A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 545, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 545, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_56A_Type = MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_56A_Type
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_56A_Type', MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_56A_Type)


# Complex type {http://www.w3schools.com}MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_56J_Type with content type SIMPLE
class MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_56J_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_56J_Type with content type SIMPLE"""
    _TypeDefinition = MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_56J_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_56J_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 554, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_56J_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_56J_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='56J')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 557, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 557, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_56J_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 558, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 558, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_56J_Type = MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_56J_Type
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_56J_Type', MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_56J_Type)


# Complex type {http://www.w3schools.com}MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_57A_Type with content type SIMPLE
class MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_57A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_57A_Type with content type SIMPLE"""
    _TypeDefinition = MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_57A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_57A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 567, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_57A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_57A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='57A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 570, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 570, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_57A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 571, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 571, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_57A_Type = MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_57A_Type
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_57A_Type', MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_57A_Type)


# Complex type {http://www.w3schools.com}MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_57J_Type with content type SIMPLE
class MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_57J_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_57J_Type with content type SIMPLE"""
    _TypeDefinition = MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_57J_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_57J_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 580, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_57J_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_57J_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='57J')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 583, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 583, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_57J_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 584, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 584, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_57J_Type = MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_57J_Type
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_57J_Type', MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_57J_Type)


# Complex type {http://www.w3schools.com}MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_58A_Type with content type SIMPLE
class MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_58A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_58A_Type with content type SIMPLE"""
    _TypeDefinition = MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_58A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_58A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 593, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_58A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_58A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='58A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 596, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 596, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_58A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 597, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 597, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_58A_Type = MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_58A_Type
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_58A_Type', MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_58A_Type)


# Complex type {http://www.w3schools.com}MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_58J_Type with content type SIMPLE
class MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_58J_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_58J_Type with content type SIMPLE"""
    _TypeDefinition = MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_58J_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_58J_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 606, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_58J_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_58J_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='58J')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 609, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 609, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_58J_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 610, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 610, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_58J_Type = MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_58J_Type
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_58J_Type', MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_58J_Type)


# Complex type {http://www.w3schools.com}MT304_SequenceC_OptionalGeneralInformation_21A_Type with content type SIMPLE
class MT304_SequenceC_OptionalGeneralInformation_21A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT304_SequenceC_OptionalGeneralInformation_21A_Type with content type SIMPLE"""
    _TypeDefinition = MT304_SequenceC_OptionalGeneralInformation_21A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceC_OptionalGeneralInformation_21A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 619, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT304_SequenceC_OptionalGeneralInformation_21A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT304_SequenceC_OptionalGeneralInformation_21A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='21A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 622, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 622, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT304_SequenceC_OptionalGeneralInformation_21A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 623, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 623, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT304_SequenceC_OptionalGeneralInformation_21A_Type = MT304_SequenceC_OptionalGeneralInformation_21A_Type
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceC_OptionalGeneralInformation_21A_Type', MT304_SequenceC_OptionalGeneralInformation_21A_Type)


# Complex type {http://www.w3schools.com}MT304_SequenceC_OptionalGeneralInformation_21G_Type with content type SIMPLE
class MT304_SequenceC_OptionalGeneralInformation_21G_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT304_SequenceC_OptionalGeneralInformation_21G_Type with content type SIMPLE"""
    _TypeDefinition = MT304_SequenceC_OptionalGeneralInformation_21G_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceC_OptionalGeneralInformation_21G_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 632, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT304_SequenceC_OptionalGeneralInformation_21G_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT304_SequenceC_OptionalGeneralInformation_21G_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='21G')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 635, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 635, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT304_SequenceC_OptionalGeneralInformation_21G_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 636, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 636, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT304_SequenceC_OptionalGeneralInformation_21G_Type = MT304_SequenceC_OptionalGeneralInformation_21G_Type
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceC_OptionalGeneralInformation_21G_Type', MT304_SequenceC_OptionalGeneralInformation_21G_Type)


# Complex type {http://www.w3schools.com}MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_22L_Type with content type SIMPLE
class MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_22L_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_22L_Type with content type SIMPLE"""
    _TypeDefinition = MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_22L_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_22L_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 645, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_22L_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_22L_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='22L')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 648, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 648, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_22L_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 649, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 649, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_22L_Type = MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_22L_Type
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_22L_Type', MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_22L_Type)


# Complex type {http://www.w3schools.com}MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_22M_Type with content type SIMPLE
class MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_22M_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_22M_Type with content type SIMPLE"""
    _TypeDefinition = MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_22M_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_22M_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 658, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_22M_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_22M_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='22M')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 661, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 661, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_22M_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 662, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 662, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_22M_Type = MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_22M_Type
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_22M_Type', MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_22M_Type)


# Complex type {http://www.w3schools.com}MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_22N_Type with content type SIMPLE
class MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_22N_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_22N_Type with content type SIMPLE"""
    _TypeDefinition = MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_22N_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_22N_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 671, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_22N_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_22N_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='22N')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 674, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 674, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_22N_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 675, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 675, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_22N_Type = MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_22N_Type
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_22N_Type', MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_22N_Type)


# Complex type {http://www.w3schools.com}MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_SubsequenceC1a_PriorUniqueTransactionIdentifier_22P_Type with content type SIMPLE
class MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_SubsequenceC1a_PriorUniqueTransactionIdentifier_22P_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_SubsequenceC1a_PriorUniqueTransactionIdentifier_22P_Type with content type SIMPLE"""
    _TypeDefinition = MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_SubsequenceC1a_PriorUniqueTransactionIdentifier_22P_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_SubsequenceC1a_PriorUniqueTransactionIdentifier_22P_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 684, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_SubsequenceC1a_PriorUniqueTransactionIdentifier_22P_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_SubsequenceC1a_PriorUniqueTransactionIdentifier_22P_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='22P')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 687, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 687, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_SubsequenceC1a_PriorUniqueTransactionIdentifier_22P_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 688, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 688, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_SubsequenceC1a_PriorUniqueTransactionIdentifier_22P_Type = MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_SubsequenceC1a_PriorUniqueTransactionIdentifier_22P_Type
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_SubsequenceC1a_PriorUniqueTransactionIdentifier_22P_Type', MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_SubsequenceC1a_PriorUniqueTransactionIdentifier_22P_Type)


# Complex type {http://www.w3schools.com}MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_SubsequenceC1a_PriorUniqueTransactionIdentifier_22R_Type with content type SIMPLE
class MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_SubsequenceC1a_PriorUniqueTransactionIdentifier_22R_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_SubsequenceC1a_PriorUniqueTransactionIdentifier_22R_Type with content type SIMPLE"""
    _TypeDefinition = MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_SubsequenceC1a_PriorUniqueTransactionIdentifier_22R_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_SubsequenceC1a_PriorUniqueTransactionIdentifier_22R_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 697, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_SubsequenceC1a_PriorUniqueTransactionIdentifier_22R_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_SubsequenceC1a_PriorUniqueTransactionIdentifier_22R_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='22R')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 700, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 700, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_SubsequenceC1a_PriorUniqueTransactionIdentifier_22R_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 701, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 701, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_SubsequenceC1a_PriorUniqueTransactionIdentifier_22R_Type = MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_SubsequenceC1a_PriorUniqueTransactionIdentifier_22R_Type
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_SubsequenceC1a_PriorUniqueTransactionIdentifier_22R_Type', MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_SubsequenceC1a_PriorUniqueTransactionIdentifier_22R_Type)


# Complex type {http://www.w3schools.com}MT304_SequenceC_OptionalGeneralInformation_22U_Type with content type SIMPLE
class MT304_SequenceC_OptionalGeneralInformation_22U_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT304_SequenceC_OptionalGeneralInformation_22U_Type with content type SIMPLE"""
    _TypeDefinition = MT304_SequenceC_OptionalGeneralInformation_22U_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceC_OptionalGeneralInformation_22U_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 710, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT304_SequenceC_OptionalGeneralInformation_22U_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT304_SequenceC_OptionalGeneralInformation_22U_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='22U')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 713, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 713, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT304_SequenceC_OptionalGeneralInformation_22U_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 714, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 714, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT304_SequenceC_OptionalGeneralInformation_22U_Type = MT304_SequenceC_OptionalGeneralInformation_22U_Type
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceC_OptionalGeneralInformation_22U_Type', MT304_SequenceC_OptionalGeneralInformation_22U_Type)


# Complex type {http://www.w3schools.com}MT304_SequenceC_OptionalGeneralInformation_35B_Type with content type SIMPLE
class MT304_SequenceC_OptionalGeneralInformation_35B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT304_SequenceC_OptionalGeneralInformation_35B_Type with content type SIMPLE"""
    _TypeDefinition = MT304_SequenceC_OptionalGeneralInformation_35B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceC_OptionalGeneralInformation_35B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 723, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT304_SequenceC_OptionalGeneralInformation_35B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT304_SequenceC_OptionalGeneralInformation_35B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='35B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 726, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 726, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT304_SequenceC_OptionalGeneralInformation_35B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 727, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 727, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT304_SequenceC_OptionalGeneralInformation_35B_Type = MT304_SequenceC_OptionalGeneralInformation_35B_Type
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceC_OptionalGeneralInformation_35B_Type', MT304_SequenceC_OptionalGeneralInformation_35B_Type)


# Complex type {http://www.w3schools.com}MT304_SequenceC_OptionalGeneralInformation_22V_Type with content type SIMPLE
class MT304_SequenceC_OptionalGeneralInformation_22V_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT304_SequenceC_OptionalGeneralInformation_22V_Type with content type SIMPLE"""
    _TypeDefinition = MT304_SequenceC_OptionalGeneralInformation_22V_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceC_OptionalGeneralInformation_22V_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 736, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT304_SequenceC_OptionalGeneralInformation_22V_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT304_SequenceC_OptionalGeneralInformation_22V_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='22V')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 739, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 739, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT304_SequenceC_OptionalGeneralInformation_22V_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 740, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 740, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT304_SequenceC_OptionalGeneralInformation_22V_Type = MT304_SequenceC_OptionalGeneralInformation_22V_Type
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceC_OptionalGeneralInformation_22V_Type', MT304_SequenceC_OptionalGeneralInformation_22V_Type)


# Complex type {http://www.w3schools.com}MT304_SequenceC_OptionalGeneralInformation_98D_Type with content type SIMPLE
class MT304_SequenceC_OptionalGeneralInformation_98D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT304_SequenceC_OptionalGeneralInformation_98D_Type with content type SIMPLE"""
    _TypeDefinition = MT304_SequenceC_OptionalGeneralInformation_98D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceC_OptionalGeneralInformation_98D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 749, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT304_SequenceC_OptionalGeneralInformation_98D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT304_SequenceC_OptionalGeneralInformation_98D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='98D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 752, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 752, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT304_SequenceC_OptionalGeneralInformation_98D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 753, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 753, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT304_SequenceC_OptionalGeneralInformation_98D_Type = MT304_SequenceC_OptionalGeneralInformation_98D_Type
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceC_OptionalGeneralInformation_98D_Type', MT304_SequenceC_OptionalGeneralInformation_98D_Type)


# Complex type {http://www.w3schools.com}MT304_SequenceC_OptionalGeneralInformation_98G_Type with content type SIMPLE
class MT304_SequenceC_OptionalGeneralInformation_98G_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT304_SequenceC_OptionalGeneralInformation_98G_Type with content type SIMPLE"""
    _TypeDefinition = MT304_SequenceC_OptionalGeneralInformation_98G_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceC_OptionalGeneralInformation_98G_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 762, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT304_SequenceC_OptionalGeneralInformation_98G_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT304_SequenceC_OptionalGeneralInformation_98G_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='98G')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 765, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 765, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT304_SequenceC_OptionalGeneralInformation_98G_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 766, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 766, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT304_SequenceC_OptionalGeneralInformation_98G_Type = MT304_SequenceC_OptionalGeneralInformation_98G_Type
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceC_OptionalGeneralInformation_98G_Type', MT304_SequenceC_OptionalGeneralInformation_98G_Type)


# Complex type {http://www.w3schools.com}MT304_SequenceC_OptionalGeneralInformation_29A_Type with content type SIMPLE
class MT304_SequenceC_OptionalGeneralInformation_29A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT304_SequenceC_OptionalGeneralInformation_29A_Type with content type SIMPLE"""
    _TypeDefinition = MT304_SequenceC_OptionalGeneralInformation_29A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceC_OptionalGeneralInformation_29A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 775, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT304_SequenceC_OptionalGeneralInformation_29A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT304_SequenceC_OptionalGeneralInformation_29A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='29A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 778, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 778, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT304_SequenceC_OptionalGeneralInformation_29A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 779, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 779, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT304_SequenceC_OptionalGeneralInformation_29A_Type = MT304_SequenceC_OptionalGeneralInformation_29A_Type
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceC_OptionalGeneralInformation_29A_Type', MT304_SequenceC_OptionalGeneralInformation_29A_Type)


# Complex type {http://www.w3schools.com}MT304_SequenceC_OptionalGeneralInformation_34C_Type with content type SIMPLE
class MT304_SequenceC_OptionalGeneralInformation_34C_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT304_SequenceC_OptionalGeneralInformation_34C_Type with content type SIMPLE"""
    _TypeDefinition = MT304_SequenceC_OptionalGeneralInformation_34C_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceC_OptionalGeneralInformation_34C_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 788, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT304_SequenceC_OptionalGeneralInformation_34C_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT304_SequenceC_OptionalGeneralInformation_34C_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='34C')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 791, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 791, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT304_SequenceC_OptionalGeneralInformation_34C_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 792, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 792, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT304_SequenceC_OptionalGeneralInformation_34C_Type = MT304_SequenceC_OptionalGeneralInformation_34C_Type
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceC_OptionalGeneralInformation_34C_Type', MT304_SequenceC_OptionalGeneralInformation_34C_Type)


# Complex type {http://www.w3schools.com}MT304_SequenceD_AccountingInformation_21P_Type with content type SIMPLE
class MT304_SequenceD_AccountingInformation_21P_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT304_SequenceD_AccountingInformation_21P_Type with content type SIMPLE"""
    _TypeDefinition = MT304_SequenceD_AccountingInformation_21P_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceD_AccountingInformation_21P_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 809, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT304_SequenceD_AccountingInformation_21P_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT304_SequenceD_AccountingInformation_21P_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='21P')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 812, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 812, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT304_SequenceD_AccountingInformation_21P_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 813, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 813, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT304_SequenceD_AccountingInformation_21P_Type = MT304_SequenceD_AccountingInformation_21P_Type
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceD_AccountingInformation_21P_Type', MT304_SequenceD_AccountingInformation_21P_Type)


# Complex type {http://www.w3schools.com}MT304_SequenceD_AccountingInformation_17G_Type with content type SIMPLE
class MT304_SequenceD_AccountingInformation_17G_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT304_SequenceD_AccountingInformation_17G_Type with content type SIMPLE"""
    _TypeDefinition = MT304_SequenceD_AccountingInformation_17G_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceD_AccountingInformation_17G_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 822, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT304_SequenceD_AccountingInformation_17G_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT304_SequenceD_AccountingInformation_17G_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='17G')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 825, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 825, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT304_SequenceD_AccountingInformation_17G_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 826, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 826, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT304_SequenceD_AccountingInformation_17G_Type = MT304_SequenceD_AccountingInformation_17G_Type
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceD_AccountingInformation_17G_Type', MT304_SequenceD_AccountingInformation_17G_Type)


# Complex type {http://www.w3schools.com}MT304_SequenceD_AccountingInformation_32G_Type with content type SIMPLE
class MT304_SequenceD_AccountingInformation_32G_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT304_SequenceD_AccountingInformation_32G_Type with content type SIMPLE"""
    _TypeDefinition = MT304_SequenceD_AccountingInformation_32G_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceD_AccountingInformation_32G_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 835, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT304_SequenceD_AccountingInformation_32G_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT304_SequenceD_AccountingInformation_32G_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='32G')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 838, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 838, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT304_SequenceD_AccountingInformation_32G_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 839, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 839, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT304_SequenceD_AccountingInformation_32G_Type = MT304_SequenceD_AccountingInformation_32G_Type
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceD_AccountingInformation_32G_Type', MT304_SequenceD_AccountingInformation_32G_Type)


# Complex type {http://www.w3schools.com}MT304_SequenceD_AccountingInformation_34B_Type with content type SIMPLE
class MT304_SequenceD_AccountingInformation_34B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT304_SequenceD_AccountingInformation_34B_Type with content type SIMPLE"""
    _TypeDefinition = MT304_SequenceD_AccountingInformation_34B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceD_AccountingInformation_34B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 848, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT304_SequenceD_AccountingInformation_34B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT304_SequenceD_AccountingInformation_34B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='34B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 851, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 851, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT304_SequenceD_AccountingInformation_34B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 852, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 852, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT304_SequenceD_AccountingInformation_34B_Type = MT304_SequenceD_AccountingInformation_34B_Type
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceD_AccountingInformation_34B_Type', MT304_SequenceD_AccountingInformation_34B_Type)


# Complex type {http://www.w3schools.com}MT304_SequenceD_AccountingInformation_30F_Type with content type SIMPLE
class MT304_SequenceD_AccountingInformation_30F_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT304_SequenceD_AccountingInformation_30F_Type with content type SIMPLE"""
    _TypeDefinition = MT304_SequenceD_AccountingInformation_30F_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceD_AccountingInformation_30F_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 861, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT304_SequenceD_AccountingInformation_30F_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT304_SequenceD_AccountingInformation_30F_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='30F')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 864, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 864, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT304_SequenceD_AccountingInformation_30F_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 865, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 865, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT304_SequenceD_AccountingInformation_30F_Type = MT304_SequenceD_AccountingInformation_30F_Type
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceD_AccountingInformation_30F_Type', MT304_SequenceD_AccountingInformation_30F_Type)


# Complex type {http://www.w3schools.com}MT304_SequenceE_NetAmountToBeSettled_17G_Type with content type SIMPLE
class MT304_SequenceE_NetAmountToBeSettled_17G_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT304_SequenceE_NetAmountToBeSettled_17G_Type with content type SIMPLE"""
    _TypeDefinition = MT304_SequenceE_NetAmountToBeSettled_17G_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceE_NetAmountToBeSettled_17G_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 874, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT304_SequenceE_NetAmountToBeSettled_17G_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT304_SequenceE_NetAmountToBeSettled_17G_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='17G')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 877, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 877, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT304_SequenceE_NetAmountToBeSettled_17G_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 878, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 878, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT304_SequenceE_NetAmountToBeSettled_17G_Type = MT304_SequenceE_NetAmountToBeSettled_17G_Type
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceE_NetAmountToBeSettled_17G_Type', MT304_SequenceE_NetAmountToBeSettled_17G_Type)


# Complex type {http://www.w3schools.com}MT304_SequenceE_NetAmountToBeSettled_32G_Type with content type SIMPLE
class MT304_SequenceE_NetAmountToBeSettled_32G_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT304_SequenceE_NetAmountToBeSettled_32G_Type with content type SIMPLE"""
    _TypeDefinition = MT304_SequenceE_NetAmountToBeSettled_32G_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceE_NetAmountToBeSettled_32G_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 887, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT304_SequenceE_NetAmountToBeSettled_32G_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT304_SequenceE_NetAmountToBeSettled_32G_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='32G')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 890, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 890, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT304_SequenceE_NetAmountToBeSettled_32G_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 891, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 891, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT304_SequenceE_NetAmountToBeSettled_32G_Type = MT304_SequenceE_NetAmountToBeSettled_32G_Type
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceE_NetAmountToBeSettled_32G_Type', MT304_SequenceE_NetAmountToBeSettled_32G_Type)


# Complex type {http://www.w3schools.com}MT304_SequenceE_NetAmountToBeSettled_53A_Type with content type SIMPLE
class MT304_SequenceE_NetAmountToBeSettled_53A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT304_SequenceE_NetAmountToBeSettled_53A_Type with content type SIMPLE"""
    _TypeDefinition = MT304_SequenceE_NetAmountToBeSettled_53A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceE_NetAmountToBeSettled_53A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 900, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT304_SequenceE_NetAmountToBeSettled_53A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT304_SequenceE_NetAmountToBeSettled_53A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='53A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 903, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 903, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT304_SequenceE_NetAmountToBeSettled_53A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 904, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 904, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT304_SequenceE_NetAmountToBeSettled_53A_Type = MT304_SequenceE_NetAmountToBeSettled_53A_Type
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceE_NetAmountToBeSettled_53A_Type', MT304_SequenceE_NetAmountToBeSettled_53A_Type)


# Complex type {http://www.w3schools.com}MT304_SequenceE_NetAmountToBeSettled_53D_Type with content type SIMPLE
class MT304_SequenceE_NetAmountToBeSettled_53D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT304_SequenceE_NetAmountToBeSettled_53D_Type with content type SIMPLE"""
    _TypeDefinition = MT304_SequenceE_NetAmountToBeSettled_53D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceE_NetAmountToBeSettled_53D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 913, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT304_SequenceE_NetAmountToBeSettled_53D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT304_SequenceE_NetAmountToBeSettled_53D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='53D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 916, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 916, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT304_SequenceE_NetAmountToBeSettled_53D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 917, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 917, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT304_SequenceE_NetAmountToBeSettled_53D_Type = MT304_SequenceE_NetAmountToBeSettled_53D_Type
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceE_NetAmountToBeSettled_53D_Type', MT304_SequenceE_NetAmountToBeSettled_53D_Type)


# Complex type {http://www.w3schools.com}MT304_SequenceE_NetAmountToBeSettled_53J_Type with content type SIMPLE
class MT304_SequenceE_NetAmountToBeSettled_53J_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT304_SequenceE_NetAmountToBeSettled_53J_Type with content type SIMPLE"""
    _TypeDefinition = MT304_SequenceE_NetAmountToBeSettled_53J_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceE_NetAmountToBeSettled_53J_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 926, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT304_SequenceE_NetAmountToBeSettled_53J_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT304_SequenceE_NetAmountToBeSettled_53J_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='53J')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 929, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 929, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT304_SequenceE_NetAmountToBeSettled_53J_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 930, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 930, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT304_SequenceE_NetAmountToBeSettled_53J_Type = MT304_SequenceE_NetAmountToBeSettled_53J_Type
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceE_NetAmountToBeSettled_53J_Type', MT304_SequenceE_NetAmountToBeSettled_53J_Type)


# Complex type {http://www.w3schools.com}MT304_SequenceE_NetAmountToBeSettled_56A_Type with content type SIMPLE
class MT304_SequenceE_NetAmountToBeSettled_56A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT304_SequenceE_NetAmountToBeSettled_56A_Type with content type SIMPLE"""
    _TypeDefinition = MT304_SequenceE_NetAmountToBeSettled_56A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceE_NetAmountToBeSettled_56A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 939, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT304_SequenceE_NetAmountToBeSettled_56A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT304_SequenceE_NetAmountToBeSettled_56A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='56A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 942, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 942, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT304_SequenceE_NetAmountToBeSettled_56A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 943, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 943, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT304_SequenceE_NetAmountToBeSettled_56A_Type = MT304_SequenceE_NetAmountToBeSettled_56A_Type
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceE_NetAmountToBeSettled_56A_Type', MT304_SequenceE_NetAmountToBeSettled_56A_Type)


# Complex type {http://www.w3schools.com}MT304_SequenceE_NetAmountToBeSettled_56D_Type with content type SIMPLE
class MT304_SequenceE_NetAmountToBeSettled_56D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT304_SequenceE_NetAmountToBeSettled_56D_Type with content type SIMPLE"""
    _TypeDefinition = MT304_SequenceE_NetAmountToBeSettled_56D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceE_NetAmountToBeSettled_56D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 952, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT304_SequenceE_NetAmountToBeSettled_56D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT304_SequenceE_NetAmountToBeSettled_56D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='56D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 955, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 955, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT304_SequenceE_NetAmountToBeSettled_56D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 956, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 956, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT304_SequenceE_NetAmountToBeSettled_56D_Type = MT304_SequenceE_NetAmountToBeSettled_56D_Type
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceE_NetAmountToBeSettled_56D_Type', MT304_SequenceE_NetAmountToBeSettled_56D_Type)


# Complex type {http://www.w3schools.com}MT304_SequenceE_NetAmountToBeSettled_56J_Type with content type SIMPLE
class MT304_SequenceE_NetAmountToBeSettled_56J_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT304_SequenceE_NetAmountToBeSettled_56J_Type with content type SIMPLE"""
    _TypeDefinition = MT304_SequenceE_NetAmountToBeSettled_56J_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceE_NetAmountToBeSettled_56J_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 965, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT304_SequenceE_NetAmountToBeSettled_56J_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT304_SequenceE_NetAmountToBeSettled_56J_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='56J')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 968, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 968, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT304_SequenceE_NetAmountToBeSettled_56J_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 969, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 969, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT304_SequenceE_NetAmountToBeSettled_56J_Type = MT304_SequenceE_NetAmountToBeSettled_56J_Type
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceE_NetAmountToBeSettled_56J_Type', MT304_SequenceE_NetAmountToBeSettled_56J_Type)


# Complex type {http://www.w3schools.com}MT304_SequenceE_NetAmountToBeSettled_57A_Type with content type SIMPLE
class MT304_SequenceE_NetAmountToBeSettled_57A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT304_SequenceE_NetAmountToBeSettled_57A_Type with content type SIMPLE"""
    _TypeDefinition = MT304_SequenceE_NetAmountToBeSettled_57A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceE_NetAmountToBeSettled_57A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 978, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT304_SequenceE_NetAmountToBeSettled_57A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT304_SequenceE_NetAmountToBeSettled_57A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='57A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 981, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 981, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT304_SequenceE_NetAmountToBeSettled_57A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 982, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 982, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT304_SequenceE_NetAmountToBeSettled_57A_Type = MT304_SequenceE_NetAmountToBeSettled_57A_Type
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceE_NetAmountToBeSettled_57A_Type', MT304_SequenceE_NetAmountToBeSettled_57A_Type)


# Complex type {http://www.w3schools.com}MT304_SequenceE_NetAmountToBeSettled_57D_Type with content type SIMPLE
class MT304_SequenceE_NetAmountToBeSettled_57D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT304_SequenceE_NetAmountToBeSettled_57D_Type with content type SIMPLE"""
    _TypeDefinition = MT304_SequenceE_NetAmountToBeSettled_57D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceE_NetAmountToBeSettled_57D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 991, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT304_SequenceE_NetAmountToBeSettled_57D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT304_SequenceE_NetAmountToBeSettled_57D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='57D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 994, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 994, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT304_SequenceE_NetAmountToBeSettled_57D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 995, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 995, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT304_SequenceE_NetAmountToBeSettled_57D_Type = MT304_SequenceE_NetAmountToBeSettled_57D_Type
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceE_NetAmountToBeSettled_57D_Type', MT304_SequenceE_NetAmountToBeSettled_57D_Type)


# Complex type {http://www.w3schools.com}MT304_SequenceE_NetAmountToBeSettled_57J_Type with content type SIMPLE
class MT304_SequenceE_NetAmountToBeSettled_57J_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT304_SequenceE_NetAmountToBeSettled_57J_Type with content type SIMPLE"""
    _TypeDefinition = MT304_SequenceE_NetAmountToBeSettled_57J_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceE_NetAmountToBeSettled_57J_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1004, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT304_SequenceE_NetAmountToBeSettled_57J_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT304_SequenceE_NetAmountToBeSettled_57J_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='57J')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1007, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1007, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT304_SequenceE_NetAmountToBeSettled_57J_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1008, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1008, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT304_SequenceE_NetAmountToBeSettled_57J_Type = MT304_SequenceE_NetAmountToBeSettled_57J_Type
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceE_NetAmountToBeSettled_57J_Type', MT304_SequenceE_NetAmountToBeSettled_57J_Type)


# Complex type {http://www.w3schools.com}MT304_SequenceE_NetAmountToBeSettled_58A_Type with content type SIMPLE
class MT304_SequenceE_NetAmountToBeSettled_58A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT304_SequenceE_NetAmountToBeSettled_58A_Type with content type SIMPLE"""
    _TypeDefinition = MT304_SequenceE_NetAmountToBeSettled_58A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceE_NetAmountToBeSettled_58A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1017, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT304_SequenceE_NetAmountToBeSettled_58A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT304_SequenceE_NetAmountToBeSettled_58A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='58A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1020, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1020, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT304_SequenceE_NetAmountToBeSettled_58A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1021, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1021, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT304_SequenceE_NetAmountToBeSettled_58A_Type = MT304_SequenceE_NetAmountToBeSettled_58A_Type
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceE_NetAmountToBeSettled_58A_Type', MT304_SequenceE_NetAmountToBeSettled_58A_Type)


# Complex type {http://www.w3schools.com}MT304_SequenceE_NetAmountToBeSettled_58D_Type with content type SIMPLE
class MT304_SequenceE_NetAmountToBeSettled_58D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT304_SequenceE_NetAmountToBeSettled_58D_Type with content type SIMPLE"""
    _TypeDefinition = MT304_SequenceE_NetAmountToBeSettled_58D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceE_NetAmountToBeSettled_58D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1030, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT304_SequenceE_NetAmountToBeSettled_58D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT304_SequenceE_NetAmountToBeSettled_58D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='58D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1033, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1033, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT304_SequenceE_NetAmountToBeSettled_58D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1034, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1034, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT304_SequenceE_NetAmountToBeSettled_58D_Type = MT304_SequenceE_NetAmountToBeSettled_58D_Type
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceE_NetAmountToBeSettled_58D_Type', MT304_SequenceE_NetAmountToBeSettled_58D_Type)


# Complex type {http://www.w3schools.com}MT304_SequenceE_NetAmountToBeSettled_58J_Type with content type SIMPLE
class MT304_SequenceE_NetAmountToBeSettled_58J_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT304_SequenceE_NetAmountToBeSettled_58J_Type with content type SIMPLE"""
    _TypeDefinition = MT304_SequenceE_NetAmountToBeSettled_58J_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT304_SequenceE_NetAmountToBeSettled_58J_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1043, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT304_SequenceE_NetAmountToBeSettled_58J_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT304_SequenceE_NetAmountToBeSettled_58J_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='58J')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1046, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1046, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT304_SequenceE_NetAmountToBeSettled_58J_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1047, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1047, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT304_SequenceE_NetAmountToBeSettled_58J_Type = MT304_SequenceE_NetAmountToBeSettled_58J_Type
Namespace.addCategoryObject('typeBinding', 'MT304_SequenceE_NetAmountToBeSettled_58J_Type', MT304_SequenceE_NetAmountToBeSettled_58J_Type)


MT304 = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'MT304'), CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1219, 1))
Namespace.addCategoryObject('elementBinding', MT304.name().localName(), MT304)



MT304_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SendersReference'), MT304_SequenceA_GeneralInformation_20_Type, scope=MT304_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1053, 3)))

MT304_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'RelatedReference'), MT304_SequenceA_GeneralInformation_21_Type, scope=MT304_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1054, 3)))

MT304_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'TypeOfOperation'), MT304_SequenceA_GeneralInformation_22A_Type, scope=MT304_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1055, 3)))

MT304_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ScopeOfOperation'), MT304_SequenceA_GeneralInformation_94A_Type, scope=MT304_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1056, 3)))

MT304_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'OpenIndicator'), MT304_SequenceA_GeneralInformation_17O_Type, scope=MT304_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1057, 3)))

MT304_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'FinalCloseIndicator'), MT304_SequenceA_GeneralInformation_17F_Type, scope=MT304_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1058, 3)))

MT304_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'NetSettlementIndicator'), MT304_SequenceA_GeneralInformation_17N_Type, scope=MT304_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1059, 3)))

MT304_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Fund_A'), MT304_SequenceA_GeneralInformation_83A_Type, scope=MT304_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1061, 4)))

MT304_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Fund_J'), MT304_SequenceA_GeneralInformation_83J_Type, scope=MT304_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1062, 4)))

MT304_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'FundManager_A'), MT304_SequenceA_GeneralInformation_82A_Type, scope=MT304_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1065, 4)))

MT304_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'FundManager_J'), MT304_SequenceA_GeneralInformation_82J_Type, scope=MT304_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1066, 4)))

MT304_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ExecutingBroker_A'), MT304_SequenceA_GeneralInformation_87A_Type, scope=MT304_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1069, 4)))

MT304_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ExecutingBroker_J'), MT304_SequenceA_GeneralInformation_87J_Type, scope=MT304_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1070, 4)))

MT304_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'CentralCounterpartyClearingHouse_A'), MT304_SequenceA_GeneralInformation_81A_Type, scope=MT304_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1073, 4)))

MT304_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'CentralCounterpartyClearingHouse_D'), MT304_SequenceA_GeneralInformation_81D_Type, scope=MT304_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1074, 4)))

MT304_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'CentralCounterpartyClearingHouse_J'), MT304_SequenceA_GeneralInformation_81J_Type, scope=MT304_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1075, 4)))

MT304_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ClearingBroker_A'), MT304_SequenceA_GeneralInformation_89A_Type, scope=MT304_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1078, 4)))

MT304_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ClearingBroker_D'), MT304_SequenceA_GeneralInformation_89D_Type, scope=MT304_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1079, 4)))

MT304_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ClearingBroker_J'), MT304_SequenceA_GeneralInformation_89J_Type, scope=MT304_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1080, 4)))

MT304_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PaymentVersusPaymentSettlementIndicator'), MT304_SequenceA_GeneralInformation_17I_Type, scope=MT304_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1082, 3)))

MT304_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'TypeDateVersionOfTheAgreement'), MT304_SequenceA_GeneralInformation_77H_Type, scope=MT304_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1083, 3)))

MT304_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'YearOfDefinitions'), MT304_SequenceA_GeneralInformation_14C_Type, scope=MT304_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1084, 3)))

MT304_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SettlementCurrency'), MT304_SequenceA_GeneralInformation_32E_Type, scope=MT304_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1085, 3)))

MT304_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ValuationDate'), MT304_SequenceA_GeneralInformation_30U_Type, scope=MT304_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1086, 3)))

MT304_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SettlementRateSource'), MT304_SequenceA_GeneralInformation_14S_Type, scope=MT304_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1087, 3)))

MT304_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ReferenceToOpeningInstruction'), MT304_SequenceA_GeneralInformation_21A_Type, scope=MT304_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1088, 3)))

MT304_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ClearingOrSettlementSession'), MT304_SequenceA_GeneralInformation_14E_Type, scope=MT304_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1089, 3)))

def _BuildAutomaton ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1054, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1057, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1058, 3))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1059, 3))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1072, 3))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1073, 4))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1074, 4))
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1075, 4))
    counters.add(cc_7)
    cc_8 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1077, 3))
    counters.add(cc_8)
    cc_9 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1078, 4))
    counters.add(cc_9)
    cc_10 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1079, 4))
    counters.add(cc_10)
    cc_11 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1080, 4))
    counters.add(cc_11)
    cc_12 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1082, 3))
    counters.add(cc_12)
    cc_13 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1083, 3))
    counters.add(cc_13)
    cc_14 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1084, 3))
    counters.add(cc_14)
    cc_15 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1085, 3))
    counters.add(cc_15)
    cc_16 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1086, 3))
    counters.add(cc_16)
    cc_17 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1087, 3))
    counters.add(cc_17)
    cc_18 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1088, 3))
    counters.add(cc_18)
    cc_19 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1089, 3))
    counters.add(cc_19)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT304_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SendersReference')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1053, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT304_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'RelatedReference')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1054, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT304_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'TypeOfOperation')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1055, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT304_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ScopeOfOperation')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1056, 3))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT304_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'OpenIndicator')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1057, 3))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT304_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'FinalCloseIndicator')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1058, 3))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT304_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'NetSettlementIndicator')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1059, 3))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT304_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Fund_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1061, 4))
    st_7 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT304_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Fund_J')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1062, 4))
    st_8 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT304_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'FundManager_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1065, 4))
    st_9 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT304_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'FundManager_J')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1066, 4))
    st_10 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_10)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT304_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ExecutingBroker_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1069, 4))
    st_11 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_11)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT304_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ExecutingBroker_J')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1070, 4))
    st_12 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_12)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    final_update.add(fac.UpdateInstruction(cc_5, False))
    symbol = pyxb.binding.content.ElementUse(MT304_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'CentralCounterpartyClearingHouse_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1073, 4))
    st_13 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_13)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    final_update.add(fac.UpdateInstruction(cc_6, False))
    symbol = pyxb.binding.content.ElementUse(MT304_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'CentralCounterpartyClearingHouse_D')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1074, 4))
    st_14 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_14)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    final_update.add(fac.UpdateInstruction(cc_7, False))
    symbol = pyxb.binding.content.ElementUse(MT304_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'CentralCounterpartyClearingHouse_J')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1075, 4))
    st_15 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_15)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_8, False))
    final_update.add(fac.UpdateInstruction(cc_9, False))
    symbol = pyxb.binding.content.ElementUse(MT304_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ClearingBroker_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1078, 4))
    st_16 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_16)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_8, False))
    final_update.add(fac.UpdateInstruction(cc_10, False))
    symbol = pyxb.binding.content.ElementUse(MT304_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ClearingBroker_D')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1079, 4))
    st_17 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_17)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_8, False))
    final_update.add(fac.UpdateInstruction(cc_11, False))
    symbol = pyxb.binding.content.ElementUse(MT304_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ClearingBroker_J')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1080, 4))
    st_18 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_18)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_12, False))
    symbol = pyxb.binding.content.ElementUse(MT304_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PaymentVersusPaymentSettlementIndicator')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1082, 3))
    st_19 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_19)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_13, False))
    symbol = pyxb.binding.content.ElementUse(MT304_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'TypeDateVersionOfTheAgreement')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1083, 3))
    st_20 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_20)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_14, False))
    symbol = pyxb.binding.content.ElementUse(MT304_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'YearOfDefinitions')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1084, 3))
    st_21 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_21)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_15, False))
    symbol = pyxb.binding.content.ElementUse(MT304_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SettlementCurrency')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1085, 3))
    st_22 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_22)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_16, False))
    symbol = pyxb.binding.content.ElementUse(MT304_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ValuationDate')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1086, 3))
    st_23 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_23)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_17, False))
    symbol = pyxb.binding.content.ElementUse(MT304_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SettlementRateSource')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1087, 3))
    st_24 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_24)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_18, False))
    symbol = pyxb.binding.content.ElementUse(MT304_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ReferenceToOpeningInstruction')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1088, 3))
    st_25 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_25)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_19, False))
    symbol = pyxb.binding.content.ElementUse(MT304_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ClearingOrSettlementSession')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1089, 3))
    st_26 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_26)
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
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_3, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_3, False) ]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_9, [
         ]))
    transitions.append(fac.Transition(st_10, [
         ]))
    st_7._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_9, [
         ]))
    transitions.append(fac.Transition(st_10, [
         ]))
    st_8._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_11, [
         ]))
    transitions.append(fac.Transition(st_12, [
         ]))
    st_9._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_11, [
         ]))
    transitions.append(fac.Transition(st_12, [
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
    st_12._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_4, True),
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_5, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_4, True),
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_4, True),
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
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_22, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_23, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_24, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_25, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_26, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_5, False) ]))
    st_13._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_4, True),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_4, True),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_6, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_4, True),
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
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_22, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_23, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_24, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_25, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_26, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_6, False) ]))
    st_14._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_4, True),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_4, True),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_4, True),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_7, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_22, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_23, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_24, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_25, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_26, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_7, False) ]))
    st_15._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_8, True),
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_9, True) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_8, True),
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_8, True),
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_8, False),
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_8, False),
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_8, False),
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_22, [
        fac.UpdateInstruction(cc_8, False),
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_23, [
        fac.UpdateInstruction(cc_8, False),
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_24, [
        fac.UpdateInstruction(cc_8, False),
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_25, [
        fac.UpdateInstruction(cc_8, False),
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_26, [
        fac.UpdateInstruction(cc_8, False),
        fac.UpdateInstruction(cc_9, False) ]))
    st_16._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_8, True),
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_8, True),
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_10, True) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_8, True),
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_8, False),
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_8, False),
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_8, False),
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_22, [
        fac.UpdateInstruction(cc_8, False),
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_23, [
        fac.UpdateInstruction(cc_8, False),
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_24, [
        fac.UpdateInstruction(cc_8, False),
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_25, [
        fac.UpdateInstruction(cc_8, False),
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_26, [
        fac.UpdateInstruction(cc_8, False),
        fac.UpdateInstruction(cc_10, False) ]))
    st_17._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_8, True),
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_8, True),
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_8, True),
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_11, True) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_8, False),
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_8, False),
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_8, False),
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_22, [
        fac.UpdateInstruction(cc_8, False),
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_23, [
        fac.UpdateInstruction(cc_8, False),
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_24, [
        fac.UpdateInstruction(cc_8, False),
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_25, [
        fac.UpdateInstruction(cc_8, False),
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_26, [
        fac.UpdateInstruction(cc_8, False),
        fac.UpdateInstruction(cc_11, False) ]))
    st_18._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_12, True) ]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_12, False) ]))
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_12, False) ]))
    transitions.append(fac.Transition(st_22, [
        fac.UpdateInstruction(cc_12, False) ]))
    transitions.append(fac.Transition(st_23, [
        fac.UpdateInstruction(cc_12, False) ]))
    transitions.append(fac.Transition(st_24, [
        fac.UpdateInstruction(cc_12, False) ]))
    transitions.append(fac.Transition(st_25, [
        fac.UpdateInstruction(cc_12, False) ]))
    transitions.append(fac.Transition(st_26, [
        fac.UpdateInstruction(cc_12, False) ]))
    st_19._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_13, True) ]))
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
    st_20._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_14, True) ]))
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
    st_21._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_22, [
        fac.UpdateInstruction(cc_15, True) ]))
    transitions.append(fac.Transition(st_23, [
        fac.UpdateInstruction(cc_15, False) ]))
    transitions.append(fac.Transition(st_24, [
        fac.UpdateInstruction(cc_15, False) ]))
    transitions.append(fac.Transition(st_25, [
        fac.UpdateInstruction(cc_15, False) ]))
    transitions.append(fac.Transition(st_26, [
        fac.UpdateInstruction(cc_15, False) ]))
    st_22._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_23, [
        fac.UpdateInstruction(cc_16, True) ]))
    transitions.append(fac.Transition(st_24, [
        fac.UpdateInstruction(cc_16, False) ]))
    transitions.append(fac.Transition(st_25, [
        fac.UpdateInstruction(cc_16, False) ]))
    transitions.append(fac.Transition(st_26, [
        fac.UpdateInstruction(cc_16, False) ]))
    st_23._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_24, [
        fac.UpdateInstruction(cc_17, True) ]))
    transitions.append(fac.Transition(st_25, [
        fac.UpdateInstruction(cc_17, False) ]))
    transitions.append(fac.Transition(st_26, [
        fac.UpdateInstruction(cc_17, False) ]))
    st_24._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_25, [
        fac.UpdateInstruction(cc_18, True) ]))
    transitions.append(fac.Transition(st_26, [
        fac.UpdateInstruction(cc_18, False) ]))
    st_25._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_26, [
        fac.UpdateInstruction(cc_19, True) ]))
    st_26._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
MT304_SequenceA_GeneralInformation._Automaton = _BuildAutomaton()




MT304_SequenceB_ForexTransactionDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'TradeDate'), MT304_SequenceB_ForexTransactionDetails_30T_Type, scope=MT304_SequenceB_ForexTransactionDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1097, 3)))

MT304_SequenceB_ForexTransactionDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ValueDate'), MT304_SequenceB_ForexTransactionDetails_30V_Type, scope=MT304_SequenceB_ForexTransactionDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1098, 3)))

MT304_SequenceB_ForexTransactionDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ExchangeRate'), MT304_SequenceB_ForexTransactionDetails_36_Type, scope=MT304_SequenceB_ForexTransactionDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1099, 3)))

MT304_SequenceB_ForexTransactionDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PaymentClearingCentre'), MT304_SequenceB_ForexTransactionDetails_39M_Type, scope=MT304_SequenceB_ForexTransactionDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1100, 3)))

MT304_SequenceB_ForexTransactionDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SubsequenceB1_AmountBought'), MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought, scope=MT304_SequenceB_ForexTransactionDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1101, 3)))

MT304_SequenceB_ForexTransactionDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SubsequenceB2_AmountSold'), MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold, scope=MT304_SequenceB_ForexTransactionDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1102, 3)))

def _BuildAutomaton_ ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_
    del _BuildAutomaton_
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1100, 3))
    counters.add(cc_0)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT304_SequenceB_ForexTransactionDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'TradeDate')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1097, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT304_SequenceB_ForexTransactionDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ValueDate')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1098, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT304_SequenceB_ForexTransactionDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ExchangeRate')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1099, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT304_SequenceB_ForexTransactionDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PaymentClearingCentre')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1100, 3))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT304_SequenceB_ForexTransactionDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SubsequenceB1_AmountBought')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1101, 3))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT304_SequenceB_ForexTransactionDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SubsequenceB2_AmountSold')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1102, 3))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
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
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
         ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    st_5._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
MT304_SequenceB_ForexTransactionDetails._Automaton = _BuildAutomaton_()




MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'CurrencyAmountBought'), MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_32B_Type, scope=MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1110, 3)))

MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_A'), MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_53A_Type, scope=MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1112, 4)))

MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_J'), MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_53J_Type, scope=MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1113, 4)))

MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_A'), MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_56A_Type, scope=MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1116, 4)))

MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_J'), MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_56J_Type, scope=MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1117, 4)))

MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_A'), MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_57A_Type, scope=MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1120, 4)))

MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_J'), MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought_57J_Type, scope=MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1121, 4)))

def _BuildAutomaton_2 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_2
    del _BuildAutomaton_2
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1115, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1116, 4))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1117, 4))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1119, 3))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1120, 4))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1121, 4))
    counters.add(cc_5)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'CurrencyAmountBought')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1110, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1112, 4))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_J')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1113, 4))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1116, 4))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_J')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1117, 4))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1120, 4))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    final_update.add(fac.UpdateInstruction(cc_5, False))
    symbol = pyxb.binding.content.ElementUse(MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_J')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1121, 4))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    transitions.append(fac.Transition(st_2, [
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
    st_6._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
MT304_SequenceB_ForexTransactionDetails_SubsequenceB1_AmountBought._Automaton = _BuildAutomaton_2()




MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'CurrencyAmountSold'), MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_33B_Type, scope=MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1127, 3)))

MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_A'), MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_53A_Type, scope=MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1129, 4)))

MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_J'), MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_53J_Type, scope=MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1130, 4)))

MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_A'), MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_56A_Type, scope=MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1133, 4)))

MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_J'), MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_56J_Type, scope=MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1134, 4)))

MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_A'), MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_57A_Type, scope=MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1137, 4)))

MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_J'), MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_57J_Type, scope=MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1138, 4)))

MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_A'), MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_58A_Type, scope=MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1141, 4)))

MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_J'), MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold_58J_Type, scope=MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1142, 4)))

def _BuildAutomaton_3 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_3
    del _BuildAutomaton_3
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1128, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1129, 4))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1130, 4))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1132, 3))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1133, 4))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1134, 4))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1140, 3))
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1141, 4))
    counters.add(cc_7)
    cc_8 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1142, 4))
    counters.add(cc_8)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'CurrencyAmountSold')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1127, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1129, 4))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_J')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1130, 4))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1133, 4))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_J')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1134, 4))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1137, 4))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_J')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1138, 4))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_6, False))
    final_update.add(fac.UpdateInstruction(cc_7, False))
    symbol = pyxb.binding.content.ElementUse(MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1141, 4))
    st_7 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_6, False))
    final_update.add(fac.UpdateInstruction(cc_8, False))
    symbol = pyxb.binding.content.ElementUse(MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_J')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1142, 4))
    st_8 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
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
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_3, True),
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_4, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_3, True),
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_3, False),
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_3, False),
        fac.UpdateInstruction(cc_4, False) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_3, True),
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_3, True),
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_5, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_3, False),
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_3, False),
        fac.UpdateInstruction(cc_5, False) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
         ]))
    transitions.append(fac.Transition(st_8, [
         ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
         ]))
    transitions.append(fac.Transition(st_8, [
         ]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_6, True),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_7, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_6, True),
        fac.UpdateInstruction(cc_7, False) ]))
    st_7._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_6, True),
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_6, True),
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_8, True) ]))
    st_8._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
MT304_SequenceB_ForexTransactionDetails_SubsequenceB2_AmountSold._Automaton = _BuildAutomaton_3()




MT304_SequenceC_OptionalGeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ReferenceToTheAssociatedTrade'), MT304_SequenceC_OptionalGeneralInformation_21A_Type, scope=MT304_SequenceC_OptionalGeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1148, 3)))

MT304_SequenceC_OptionalGeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ExecutingBrokersReference'), MT304_SequenceC_OptionalGeneralInformation_21G_Type, scope=MT304_SequenceC_OptionalGeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1149, 3)))

MT304_SequenceC_OptionalGeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SubsequenceC1_UniqueTransactionIdentifier'), MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier, scope=MT304_SequenceC_OptionalGeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1150, 3)))

MT304_SequenceC_OptionalGeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'UnderlyingProductIdentifier'), MT304_SequenceC_OptionalGeneralInformation_22U_Type, scope=MT304_SequenceC_OptionalGeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1151, 3)))

MT304_SequenceC_OptionalGeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'IdentificationOfFinancialInstrument'), MT304_SequenceC_OptionalGeneralInformation_35B_Type, scope=MT304_SequenceC_OptionalGeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1152, 3)))

MT304_SequenceC_OptionalGeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ExecutionVenue'), MT304_SequenceC_OptionalGeneralInformation_22V_Type, scope=MT304_SequenceC_OptionalGeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1153, 3)))

MT304_SequenceC_OptionalGeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ExecutionTimestamp'), MT304_SequenceC_OptionalGeneralInformation_98D_Type, scope=MT304_SequenceC_OptionalGeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1154, 3)))

MT304_SequenceC_OptionalGeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ClearingTimestamp'), MT304_SequenceC_OptionalGeneralInformation_98G_Type, scope=MT304_SequenceC_OptionalGeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1155, 3)))

MT304_SequenceC_OptionalGeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ContactInformation'), MT304_SequenceC_OptionalGeneralInformation_29A_Type, scope=MT304_SequenceC_OptionalGeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1156, 3)))

MT304_SequenceC_OptionalGeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'CommissionAndFees'), MT304_SequenceC_OptionalGeneralInformation_34C_Type, scope=MT304_SequenceC_OptionalGeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1157, 3)))

MT304_SequenceC_OptionalGeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SenderToReceiverInformation'), MT304_SequenceC_OptionalGeneralInformation_72_Type, scope=MT304_SequenceC_OptionalGeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1158, 3)))

def _BuildAutomaton_4 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_4
    del _BuildAutomaton_4
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1148, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1149, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1150, 3))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1151, 3))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1152, 3))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1153, 3))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1154, 3))
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1155, 3))
    counters.add(cc_7)
    cc_8 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1156, 3))
    counters.add(cc_8)
    cc_9 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1157, 3))
    counters.add(cc_9)
    cc_10 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1158, 3))
    counters.add(cc_10)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(MT304_SequenceC_OptionalGeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ReferenceToTheAssociatedTrade')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1148, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(MT304_SequenceC_OptionalGeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ExecutingBrokersReference')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1149, 3))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(MT304_SequenceC_OptionalGeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SubsequenceC1_UniqueTransactionIdentifier')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1150, 3))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(MT304_SequenceC_OptionalGeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'UnderlyingProductIdentifier')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1151, 3))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(MT304_SequenceC_OptionalGeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'IdentificationOfFinancialInstrument')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1152, 3))
    st_4 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_5, False))
    symbol = pyxb.binding.content.ElementUse(MT304_SequenceC_OptionalGeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ExecutionVenue')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1153, 3))
    st_5 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_6, False))
    symbol = pyxb.binding.content.ElementUse(MT304_SequenceC_OptionalGeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ExecutionTimestamp')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1154, 3))
    st_6 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_7, False))
    symbol = pyxb.binding.content.ElementUse(MT304_SequenceC_OptionalGeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ClearingTimestamp')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1155, 3))
    st_7 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_8, False))
    symbol = pyxb.binding.content.ElementUse(MT304_SequenceC_OptionalGeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ContactInformation')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1156, 3))
    st_8 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_9, False))
    symbol = pyxb.binding.content.ElementUse(MT304_SequenceC_OptionalGeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'CommissionAndFees')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1157, 3))
    st_9 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_10, False))
    symbol = pyxb.binding.content.ElementUse(MT304_SequenceC_OptionalGeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SenderToReceiverInformation')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1158, 3))
    st_10 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_10)
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
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_3, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_3, False) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_4, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_4, False) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_5, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_5, False) ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_6, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_6, False) ]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_7, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_7, False) ]))
    st_7._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_8, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_8, False) ]))
    st_8._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_9, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_9, False) ]))
    st_9._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_10, True) ]))
    st_10._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
MT304_SequenceC_OptionalGeneralInformation._Automaton = _BuildAutomaton_4()




MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ReportingJurisdiction'), MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_22L_Type, scope=MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1166, 3)))

MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'UTINamespaceIssuerCode'), MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_22M_Type, scope=MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1167, 3)))

MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'TransactionIdentifier'), MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_22N_Type, scope=MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1168, 3)))

MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SubsequenceC1a_PriorUniqueTransactionIdentifier'), MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_SubsequenceC1a_PriorUniqueTransactionIdentifier, scope=MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1169, 3)))

def _BuildAutomaton_5 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_5
    del _BuildAutomaton_5
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1169, 3))
    counters.add(cc_0)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ReportingJurisdiction')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1166, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'UTINamespaceIssuerCode')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1167, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'TransactionIdentifier')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1168, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SubsequenceC1a_PriorUniqueTransactionIdentifier')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1169, 3))
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
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_3._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier._Automaton = _BuildAutomaton_5()




MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_SubsequenceC1a_PriorUniqueTransactionIdentifier._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PUTINamespaceIssuerCode'), MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_SubsequenceC1a_PriorUniqueTransactionIdentifier_22P_Type, scope=MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_SubsequenceC1a_PriorUniqueTransactionIdentifier, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1174, 3)))

MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_SubsequenceC1a_PriorUniqueTransactionIdentifier._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PriorTransactionIdentifier'), MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_SubsequenceC1a_PriorUniqueTransactionIdentifier_22R_Type, scope=MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_SubsequenceC1a_PriorUniqueTransactionIdentifier, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1175, 3)))

def _BuildAutomaton_6 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_6
    del _BuildAutomaton_6
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_SubsequenceC1a_PriorUniqueTransactionIdentifier._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PUTINamespaceIssuerCode')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1174, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_SubsequenceC1a_PriorUniqueTransactionIdentifier._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PriorTransactionIdentifier')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1175, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
MT304_SequenceC_OptionalGeneralInformation_SubsequenceC1_UniqueTransactionIdentifier_SubsequenceC1a_PriorUniqueTransactionIdentifier._Automaton = _BuildAutomaton_6()




MT304_SequenceD_AccountingInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ReferenceToPreviousDeals'), MT304_SequenceD_AccountingInformation_21P_Type, scope=MT304_SequenceD_AccountingInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1180, 3)))

MT304_SequenceD_AccountingInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'GainIndicator'), MT304_SequenceD_AccountingInformation_17G_Type, scope=MT304_SequenceD_AccountingInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1181, 3)))

MT304_SequenceD_AccountingInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'CurrencyAmount'), MT304_SequenceD_AccountingInformation_32G_Type, scope=MT304_SequenceD_AccountingInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1182, 3)))

MT304_SequenceD_AccountingInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'CommissionAndFeesCurrencyAndAmount'), MT304_SequenceD_AccountingInformation_34B_Type, scope=MT304_SequenceD_AccountingInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1183, 3)))

MT304_SequenceD_AccountingInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'CommissionAndFeesSettlementDate'), MT304_SequenceD_AccountingInformation_30F_Type, scope=MT304_SequenceD_AccountingInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1184, 3)))

def _BuildAutomaton_7 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_7
    del _BuildAutomaton_7
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1180, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1181, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1182, 3))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1183, 3))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1184, 3))
    counters.add(cc_4)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(MT304_SequenceD_AccountingInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ReferenceToPreviousDeals')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1180, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(MT304_SequenceD_AccountingInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'GainIndicator')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1181, 3))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(MT304_SequenceD_AccountingInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'CurrencyAmount')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1182, 3))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(MT304_SequenceD_AccountingInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'CommissionAndFeesCurrencyAndAmount')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1183, 3))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(MT304_SequenceD_AccountingInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'CommissionAndFeesSettlementDate')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1184, 3))
    st_4 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
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
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_3, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_3, False) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_4, True) ]))
    st_4._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
MT304_SequenceD_AccountingInformation._Automaton = _BuildAutomaton_7()




MT304_SequenceE_NetAmountToBeSettled._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'GainIndicator'), MT304_SequenceE_NetAmountToBeSettled_17G_Type, scope=MT304_SequenceE_NetAmountToBeSettled, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1192, 3)))

MT304_SequenceE_NetAmountToBeSettled._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'CurrencyAmount'), MT304_SequenceE_NetAmountToBeSettled_32G_Type, scope=MT304_SequenceE_NetAmountToBeSettled, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1193, 3)))

MT304_SequenceE_NetAmountToBeSettled._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_A'), MT304_SequenceE_NetAmountToBeSettled_53A_Type, scope=MT304_SequenceE_NetAmountToBeSettled, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1195, 4)))

MT304_SequenceE_NetAmountToBeSettled._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_D'), MT304_SequenceE_NetAmountToBeSettled_53D_Type, scope=MT304_SequenceE_NetAmountToBeSettled, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1196, 4)))

MT304_SequenceE_NetAmountToBeSettled._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_J'), MT304_SequenceE_NetAmountToBeSettled_53J_Type, scope=MT304_SequenceE_NetAmountToBeSettled, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1197, 4)))

MT304_SequenceE_NetAmountToBeSettled._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_A'), MT304_SequenceE_NetAmountToBeSettled_56A_Type, scope=MT304_SequenceE_NetAmountToBeSettled, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1200, 4)))

MT304_SequenceE_NetAmountToBeSettled._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_D'), MT304_SequenceE_NetAmountToBeSettled_56D_Type, scope=MT304_SequenceE_NetAmountToBeSettled, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1201, 4)))

MT304_SequenceE_NetAmountToBeSettled._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_J'), MT304_SequenceE_NetAmountToBeSettled_56J_Type, scope=MT304_SequenceE_NetAmountToBeSettled, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1202, 4)))

MT304_SequenceE_NetAmountToBeSettled._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_A'), MT304_SequenceE_NetAmountToBeSettled_57A_Type, scope=MT304_SequenceE_NetAmountToBeSettled, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1205, 4)))

MT304_SequenceE_NetAmountToBeSettled._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_D'), MT304_SequenceE_NetAmountToBeSettled_57D_Type, scope=MT304_SequenceE_NetAmountToBeSettled, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1206, 4)))

MT304_SequenceE_NetAmountToBeSettled._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_J'), MT304_SequenceE_NetAmountToBeSettled_57J_Type, scope=MT304_SequenceE_NetAmountToBeSettled, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1207, 4)))

MT304_SequenceE_NetAmountToBeSettled._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_A'), MT304_SequenceE_NetAmountToBeSettled_58A_Type, scope=MT304_SequenceE_NetAmountToBeSettled, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1210, 4)))

MT304_SequenceE_NetAmountToBeSettled._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_D'), MT304_SequenceE_NetAmountToBeSettled_58D_Type, scope=MT304_SequenceE_NetAmountToBeSettled, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1211, 4)))

MT304_SequenceE_NetAmountToBeSettled._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_J'), MT304_SequenceE_NetAmountToBeSettled_58J_Type, scope=MT304_SequenceE_NetAmountToBeSettled, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1212, 4)))

def _BuildAutomaton_8 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_8
    del _BuildAutomaton_8
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1194, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1195, 4))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1196, 4))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1197, 4))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1199, 3))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1200, 4))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1201, 4))
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1202, 4))
    counters.add(cc_7)
    cc_8 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1204, 3))
    counters.add(cc_8)
    cc_9 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1205, 4))
    counters.add(cc_9)
    cc_10 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1206, 4))
    counters.add(cc_10)
    cc_11 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1207, 4))
    counters.add(cc_11)
    cc_12 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1209, 3))
    counters.add(cc_12)
    cc_13 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1210, 4))
    counters.add(cc_13)
    cc_14 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1211, 4))
    counters.add(cc_14)
    cc_15 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1212, 4))
    counters.add(cc_15)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT304_SequenceE_NetAmountToBeSettled._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'GainIndicator')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1192, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT304_SequenceE_NetAmountToBeSettled._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'CurrencyAmount')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1193, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(MT304_SequenceE_NetAmountToBeSettled._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1195, 4))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(MT304_SequenceE_NetAmountToBeSettled._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_D')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1196, 4))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(MT304_SequenceE_NetAmountToBeSettled._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_J')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1197, 4))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    final_update.add(fac.UpdateInstruction(cc_5, False))
    symbol = pyxb.binding.content.ElementUse(MT304_SequenceE_NetAmountToBeSettled._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1200, 4))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    final_update.add(fac.UpdateInstruction(cc_6, False))
    symbol = pyxb.binding.content.ElementUse(MT304_SequenceE_NetAmountToBeSettled._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_D')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1201, 4))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    final_update.add(fac.UpdateInstruction(cc_7, False))
    symbol = pyxb.binding.content.ElementUse(MT304_SequenceE_NetAmountToBeSettled._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_J')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1202, 4))
    st_7 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_8, False))
    final_update.add(fac.UpdateInstruction(cc_9, False))
    symbol = pyxb.binding.content.ElementUse(MT304_SequenceE_NetAmountToBeSettled._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1205, 4))
    st_8 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_8, False))
    final_update.add(fac.UpdateInstruction(cc_10, False))
    symbol = pyxb.binding.content.ElementUse(MT304_SequenceE_NetAmountToBeSettled._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_D')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1206, 4))
    st_9 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_8, False))
    final_update.add(fac.UpdateInstruction(cc_11, False))
    symbol = pyxb.binding.content.ElementUse(MT304_SequenceE_NetAmountToBeSettled._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_J')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1207, 4))
    st_10 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_10)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_12, False))
    final_update.add(fac.UpdateInstruction(cc_13, False))
    symbol = pyxb.binding.content.ElementUse(MT304_SequenceE_NetAmountToBeSettled._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1210, 4))
    st_11 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_11)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_12, False))
    final_update.add(fac.UpdateInstruction(cc_14, False))
    symbol = pyxb.binding.content.ElementUse(MT304_SequenceE_NetAmountToBeSettled._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_D')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1211, 4))
    st_12 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_12)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_12, False))
    final_update.add(fac.UpdateInstruction(cc_15, False))
    symbol = pyxb.binding.content.ElementUse(MT304_SequenceE_NetAmountToBeSettled._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_J')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1212, 4))
    st_13 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_13)
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
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_12, True),
        fac.UpdateInstruction(cc_13, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_13, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_12, True),
        fac.UpdateInstruction(cc_13, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_12, True),
        fac.UpdateInstruction(cc_13, False) ]))
    st_11._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_12, True),
        fac.UpdateInstruction(cc_14, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_12, True),
        fac.UpdateInstruction(cc_14, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_14, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_12, True),
        fac.UpdateInstruction(cc_14, False) ]))
    st_12._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_12, True),
        fac.UpdateInstruction(cc_15, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_12, True),
        fac.UpdateInstruction(cc_15, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_12, True),
        fac.UpdateInstruction(cc_15, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_15, True) ]))
    st_13._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
MT304_SequenceE_NetAmountToBeSettled._Automaton = _BuildAutomaton_8()




CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SequenceA_GeneralInformation'), MT304_SequenceA_GeneralInformation, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1222, 4)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SequenceB_ForexTransactionDetails'), MT304_SequenceB_ForexTransactionDetails, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1223, 4)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SequenceC_OptionalGeneralInformation'), MT304_SequenceC_OptionalGeneralInformation, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1224, 4)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SequenceD_AccountingInformation'), MT304_SequenceD_AccountingInformation, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1225, 4)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SequenceE_NetAmountToBeSettled'), MT304_SequenceE_NetAmountToBeSettled, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1226, 4)))

def _BuildAutomaton_9 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_9
    del _BuildAutomaton_9
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1224, 4))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1225, 4))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1226, 4))
    counters.add(cc_2)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SequenceA_GeneralInformation')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1222, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SequenceB_ForexTransactionDetails')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1223, 4))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SequenceC_OptionalGeneralInformation')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1224, 4))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SequenceD_AccountingInformation')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1225, 4))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SequenceE_NetAmountToBeSettled')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT304.xsd', 1226, 4))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
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
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_2, True) ]))
    st_4._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON._Automaton = _BuildAutomaton_9()


