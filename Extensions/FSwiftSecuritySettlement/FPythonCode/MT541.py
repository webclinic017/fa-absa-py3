# C:\Projects\Code\SwiftMessagingSolution_Python3\base\extensions\SwiftIntegration\Utilities\TemplateFiles\MT541.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:96afad3d20bbfe8d040a1a097fa388d9fecd10e3
# Generated 2019-11-07 14:10:40.123824 by PyXB version 1.2.6 using Python 3.7.4.final.0
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
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:46f4d406-013a-11ea-b5fd-509a4c321f2f')

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


# Atomic simple type: {http://www.w3schools.com}MT541_SequenceA_GeneralInformation_20C_Type_Pattern
class MT541_SequenceA_GeneralInformation_20C_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceA_GeneralInformation_20C_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 3, 1)
    _Documentation = None
MT541_SequenceA_GeneralInformation_20C_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceA_GeneralInformation_20C_Type_Pattern._CF_pattern.addPattern(pattern="(:(SEME)//[^/]([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,16}[^/])")
MT541_SequenceA_GeneralInformation_20C_Type_Pattern._InitializeFacetMap(MT541_SequenceA_GeneralInformation_20C_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceA_GeneralInformation_20C_Type_Pattern', MT541_SequenceA_GeneralInformation_20C_Type_Pattern)
_module_typeBindings.MT541_SequenceA_GeneralInformation_20C_Type_Pattern = MT541_SequenceA_GeneralInformation_20C_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceA_GeneralInformation_23G_Type_Pattern
class MT541_SequenceA_GeneralInformation_23G_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceA_GeneralInformation_23G_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 16, 1)
    _Documentation = None
MT541_SequenceA_GeneralInformation_23G_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceA_GeneralInformation_23G_Type_Pattern._CF_pattern.addPattern(pattern='((CANC|NEWM|PREA)(/(CODU|COPY|DUPL|RECO))?)')
MT541_SequenceA_GeneralInformation_23G_Type_Pattern._InitializeFacetMap(MT541_SequenceA_GeneralInformation_23G_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceA_GeneralInformation_23G_Type_Pattern', MT541_SequenceA_GeneralInformation_23G_Type_Pattern)
_module_typeBindings.MT541_SequenceA_GeneralInformation_23G_Type_Pattern = MT541_SequenceA_GeneralInformation_23G_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceA_GeneralInformation_98A_Type_Pattern
class MT541_SequenceA_GeneralInformation_98A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceA_GeneralInformation_98A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 29, 1)
    _Documentation = None
MT541_SequenceA_GeneralInformation_98A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceA_GeneralInformation_98A_Type_Pattern._CF_pattern.addPattern(pattern='(:(PREP)//[0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01]))')
MT541_SequenceA_GeneralInformation_98A_Type_Pattern._InitializeFacetMap(MT541_SequenceA_GeneralInformation_98A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceA_GeneralInformation_98A_Type_Pattern', MT541_SequenceA_GeneralInformation_98A_Type_Pattern)
_module_typeBindings.MT541_SequenceA_GeneralInformation_98A_Type_Pattern = MT541_SequenceA_GeneralInformation_98A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceA_GeneralInformation_98C_Type_Pattern
class MT541_SequenceA_GeneralInformation_98C_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceA_GeneralInformation_98C_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 42, 1)
    _Documentation = None
MT541_SequenceA_GeneralInformation_98C_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceA_GeneralInformation_98C_Type_Pattern._CF_pattern.addPattern(pattern='(:(PREP)//[0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])(0[0-9]|[1][0-9]|2[1-3])([0-5][0-9])([0-5][0-9]))')
MT541_SequenceA_GeneralInformation_98C_Type_Pattern._InitializeFacetMap(MT541_SequenceA_GeneralInformation_98C_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceA_GeneralInformation_98C_Type_Pattern', MT541_SequenceA_GeneralInformation_98C_Type_Pattern)
_module_typeBindings.MT541_SequenceA_GeneralInformation_98C_Type_Pattern = MT541_SequenceA_GeneralInformation_98C_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceA_GeneralInformation_98E_Type_Pattern
class MT541_SequenceA_GeneralInformation_98E_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceA_GeneralInformation_98E_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 55, 1)
    _Documentation = None
MT541_SequenceA_GeneralInformation_98E_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceA_GeneralInformation_98E_Type_Pattern._CF_pattern.addPattern(pattern='(:(PREP)//[0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])(0[0-9]|[1][0-9]|2[1-3])([0-5][0-9])([0-5][0-9])(,[0-9]{1,3})?(/(N)?(0[0-9]|[1][0-9]|2[1-3])(([0-5][0-9]))?)?)')
MT541_SequenceA_GeneralInformation_98E_Type_Pattern._InitializeFacetMap(MT541_SequenceA_GeneralInformation_98E_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceA_GeneralInformation_98E_Type_Pattern', MT541_SequenceA_GeneralInformation_98E_Type_Pattern)
_module_typeBindings.MT541_SequenceA_GeneralInformation_98E_Type_Pattern = MT541_SequenceA_GeneralInformation_98E_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceA_GeneralInformation_99B_Type_Pattern
class MT541_SequenceA_GeneralInformation_99B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceA_GeneralInformation_99B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 68, 1)
    _Documentation = None
MT541_SequenceA_GeneralInformation_99B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceA_GeneralInformation_99B_Type_Pattern._CF_pattern.addPattern(pattern='(:(SETT|TOSE)//[0-9]{3})')
MT541_SequenceA_GeneralInformation_99B_Type_Pattern._InitializeFacetMap(MT541_SequenceA_GeneralInformation_99B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceA_GeneralInformation_99B_Type_Pattern', MT541_SequenceA_GeneralInformation_99B_Type_Pattern)
_module_typeBindings.MT541_SequenceA_GeneralInformation_99B_Type_Pattern = MT541_SequenceA_GeneralInformation_99B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_22F_Type_Pattern
class MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_22F_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_22F_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 81, 1)
    _Documentation = None
MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_22F_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_22F_Type_Pattern._CF_pattern.addPattern(pattern='(:(LINK)/([A-Z0-9]{1,8})?/[A-Z0-9]{4})')
MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_22F_Type_Pattern._InitializeFacetMap(MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_22F_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_22F_Type_Pattern', MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_22F_Type_Pattern)
_module_typeBindings.MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_22F_Type_Pattern = MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_22F_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13A_Type_Pattern
class MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 94, 1)
    _Documentation = None
MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13A_Type_Pattern._CF_pattern.addPattern(pattern='(:(LINK)//[A-Z0-9]{3})')
MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13A_Type_Pattern._InitializeFacetMap(MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13A_Type_Pattern', MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13A_Type_Pattern)
_module_typeBindings.MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13A_Type_Pattern = MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13B_Type_Pattern
class MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 107, 1)
    _Documentation = None
MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13B_Type_Pattern._CF_pattern.addPattern(pattern="(:(LINK)/([A-Z0-9]{1,8})?/[^/]([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,30}[^/])")
MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13B_Type_Pattern._InitializeFacetMap(MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13B_Type_Pattern', MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13B_Type_Pattern)
_module_typeBindings.MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13B_Type_Pattern = MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20C_Type_Pattern
class MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20C_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20C_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 120, 1)
    _Documentation = None
MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20C_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20C_Type_Pattern._CF_pattern.addPattern(pattern="(:(POOL|PREA|PREV|RELA|TRRF|COMM|COLR|CORP|TCTR|CLTR|CLCI|TRCI|PCTI)//[^/]([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,16}[^/])")
MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20C_Type_Pattern._InitializeFacetMap(MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20C_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20C_Type_Pattern', MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20C_Type_Pattern)
_module_typeBindings.MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20C_Type_Pattern = MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20C_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20U_Type_Pattern
class MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20U_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20U_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 133, 1)
    _Documentation = None
MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20U_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20U_Type_Pattern._CF_pattern.addPattern(pattern="(:(TRRF)//([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,52})")
MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20U_Type_Pattern._InitializeFacetMap(MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20U_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20U_Type_Pattern', MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20U_Type_Pattern)
_module_typeBindings.MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20U_Type_Pattern = MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20U_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_36B_Type_Pattern
class MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_36B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_36B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 146, 1)
    _Documentation = None
MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_36B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_36B_Type_Pattern._CF_pattern.addPattern(pattern='((PAIR|TURN)//(AMOR|FAMT|UNIT)/[0-9,(?0-9)]{1,15})')
MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_36B_Type_Pattern._InitializeFacetMap(MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_36B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_36B_Type_Pattern', MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_36B_Type_Pattern)
_module_typeBindings.MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_36B_Type_Pattern = MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_36B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceB_TradeDetails_94B_Type_Pattern
class MT541_SequenceB_TradeDetails_94B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceB_TradeDetails_94B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 159, 1)
    _Documentation = None
MT541_SequenceB_TradeDetails_94B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceB_TradeDetails_94B_Type_Pattern._CF_pattern.addPattern(pattern="(:(TRAD)/([A-Z0-9]{1,8})?/[A-Z0-9]{4}(/[^/]([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,30}[^/])?)")
MT541_SequenceB_TradeDetails_94B_Type_Pattern._InitializeFacetMap(MT541_SequenceB_TradeDetails_94B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceB_TradeDetails_94B_Type_Pattern', MT541_SequenceB_TradeDetails_94B_Type_Pattern)
_module_typeBindings.MT541_SequenceB_TradeDetails_94B_Type_Pattern = MT541_SequenceB_TradeDetails_94B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceB_TradeDetails_94H_Type_Pattern
class MT541_SequenceB_TradeDetails_94H_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceB_TradeDetails_94H_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 172, 1)
    _Documentation = None
MT541_SequenceB_TradeDetails_94H_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceB_TradeDetails_94H_Type_Pattern._CF_pattern.addPattern(pattern='(:(CLEA)//[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)')
MT541_SequenceB_TradeDetails_94H_Type_Pattern._InitializeFacetMap(MT541_SequenceB_TradeDetails_94H_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceB_TradeDetails_94H_Type_Pattern', MT541_SequenceB_TradeDetails_94H_Type_Pattern)
_module_typeBindings.MT541_SequenceB_TradeDetails_94H_Type_Pattern = MT541_SequenceB_TradeDetails_94H_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceB_TradeDetails_94L_Type_Pattern
class MT541_SequenceB_TradeDetails_94L_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceB_TradeDetails_94L_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 185, 1)
    _Documentation = None
MT541_SequenceB_TradeDetails_94L_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceB_TradeDetails_94L_Type_Pattern._CF_pattern.addPattern(pattern='(:(TRAD|CLEA)//[A-Z0-9]{18}[0-9]{2})')
MT541_SequenceB_TradeDetails_94L_Type_Pattern._InitializeFacetMap(MT541_SequenceB_TradeDetails_94L_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceB_TradeDetails_94L_Type_Pattern', MT541_SequenceB_TradeDetails_94L_Type_Pattern)
_module_typeBindings.MT541_SequenceB_TradeDetails_94L_Type_Pattern = MT541_SequenceB_TradeDetails_94L_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceB_TradeDetails_98A_Type_Pattern
class MT541_SequenceB_TradeDetails_98A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceB_TradeDetails_98A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 198, 1)
    _Documentation = None
MT541_SequenceB_TradeDetails_98A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceB_TradeDetails_98A_Type_Pattern._CF_pattern.addPattern(pattern='(:(SETT|TRAD|ADEL)//[0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01]))')
MT541_SequenceB_TradeDetails_98A_Type_Pattern._InitializeFacetMap(MT541_SequenceB_TradeDetails_98A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceB_TradeDetails_98A_Type_Pattern', MT541_SequenceB_TradeDetails_98A_Type_Pattern)
_module_typeBindings.MT541_SequenceB_TradeDetails_98A_Type_Pattern = MT541_SequenceB_TradeDetails_98A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceB_TradeDetails_98B_Type_Pattern
class MT541_SequenceB_TradeDetails_98B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceB_TradeDetails_98B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 211, 1)
    _Documentation = None
MT541_SequenceB_TradeDetails_98B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceB_TradeDetails_98B_Type_Pattern._CF_pattern.addPattern(pattern='(:(SETT|TRAD)/([A-Z0-9]{1,8})?/[A-Z0-9]{4})')
MT541_SequenceB_TradeDetails_98B_Type_Pattern._InitializeFacetMap(MT541_SequenceB_TradeDetails_98B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceB_TradeDetails_98B_Type_Pattern', MT541_SequenceB_TradeDetails_98B_Type_Pattern)
_module_typeBindings.MT541_SequenceB_TradeDetails_98B_Type_Pattern = MT541_SequenceB_TradeDetails_98B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceB_TradeDetails_98C_Type_Pattern
class MT541_SequenceB_TradeDetails_98C_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceB_TradeDetails_98C_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 224, 1)
    _Documentation = None
MT541_SequenceB_TradeDetails_98C_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceB_TradeDetails_98C_Type_Pattern._CF_pattern.addPattern(pattern='(:(SETT|TRAD|ADEL)//[0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])(0[0-9]|[1][0-9]|2[1-3])([0-5][0-9])([0-5][0-9]))')
MT541_SequenceB_TradeDetails_98C_Type_Pattern._InitializeFacetMap(MT541_SequenceB_TradeDetails_98C_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceB_TradeDetails_98C_Type_Pattern', MT541_SequenceB_TradeDetails_98C_Type_Pattern)
_module_typeBindings.MT541_SequenceB_TradeDetails_98C_Type_Pattern = MT541_SequenceB_TradeDetails_98C_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceB_TradeDetails_98E_Type_Pattern
class MT541_SequenceB_TradeDetails_98E_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceB_TradeDetails_98E_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 237, 1)
    _Documentation = None
MT541_SequenceB_TradeDetails_98E_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceB_TradeDetails_98E_Type_Pattern._CF_pattern.addPattern(pattern='(:(TRAD)//[0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])(0[0-9]|[1][0-9]|2[1-3])([0-5][0-9])([0-5][0-9])(,[0-9]{1,3})?(/(N)?(0[0-9]|[1][0-9]|2[1-3])(([0-5][0-9]))?)?)')
MT541_SequenceB_TradeDetails_98E_Type_Pattern._InitializeFacetMap(MT541_SequenceB_TradeDetails_98E_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceB_TradeDetails_98E_Type_Pattern', MT541_SequenceB_TradeDetails_98E_Type_Pattern)
_module_typeBindings.MT541_SequenceB_TradeDetails_98E_Type_Pattern = MT541_SequenceB_TradeDetails_98E_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceB_TradeDetails_90A_Type_Pattern
class MT541_SequenceB_TradeDetails_90A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceB_TradeDetails_90A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 250, 1)
    _Documentation = None
MT541_SequenceB_TradeDetails_90A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceB_TradeDetails_90A_Type_Pattern._CF_pattern.addPattern(pattern='(:(DEAL)//(DISC|PRCT|PREM|YIEL)/(N)?[0-9,(?0-9)]{1,15})')
MT541_SequenceB_TradeDetails_90A_Type_Pattern._InitializeFacetMap(MT541_SequenceB_TradeDetails_90A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceB_TradeDetails_90A_Type_Pattern', MT541_SequenceB_TradeDetails_90A_Type_Pattern)
_module_typeBindings.MT541_SequenceB_TradeDetails_90A_Type_Pattern = MT541_SequenceB_TradeDetails_90A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceB_TradeDetails_90B_Type_Pattern
class MT541_SequenceB_TradeDetails_90B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceB_TradeDetails_90B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 263, 1)
    _Documentation = None
MT541_SequenceB_TradeDetails_90B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceB_TradeDetails_90B_Type_Pattern._CF_pattern.addPattern(pattern='(:(DEAL)//(ACTU|DISC|PREM)/(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})')
MT541_SequenceB_TradeDetails_90B_Type_Pattern._InitializeFacetMap(MT541_SequenceB_TradeDetails_90B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceB_TradeDetails_90B_Type_Pattern', MT541_SequenceB_TradeDetails_90B_Type_Pattern)
_module_typeBindings.MT541_SequenceB_TradeDetails_90B_Type_Pattern = MT541_SequenceB_TradeDetails_90B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceB_TradeDetails_99A_Type_Pattern
class MT541_SequenceB_TradeDetails_99A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceB_TradeDetails_99A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 276, 1)
    _Documentation = None
MT541_SequenceB_TradeDetails_99A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceB_TradeDetails_99A_Type_Pattern._CF_pattern.addPattern(pattern='(:(DAAC)//(N)?[0-9]{3})')
MT541_SequenceB_TradeDetails_99A_Type_Pattern._InitializeFacetMap(MT541_SequenceB_TradeDetails_99A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceB_TradeDetails_99A_Type_Pattern', MT541_SequenceB_TradeDetails_99A_Type_Pattern)
_module_typeBindings.MT541_SequenceB_TradeDetails_99A_Type_Pattern = MT541_SequenceB_TradeDetails_99A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceB_TradeDetails_35B_Type_Pattern
class MT541_SequenceB_TradeDetails_35B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceB_TradeDetails_35B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 289, 1)
    _Documentation = None
MT541_SequenceB_TradeDetails_35B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceB_TradeDetails_35B_Type_Pattern._CF_pattern.addPattern(pattern="((ISIN {1}[A-Z0-9]{12})?(\\n(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})?)")
MT541_SequenceB_TradeDetails_35B_Type_Pattern._InitializeFacetMap(MT541_SequenceB_TradeDetails_35B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceB_TradeDetails_35B_Type_Pattern', MT541_SequenceB_TradeDetails_35B_Type_Pattern)
_module_typeBindings.MT541_SequenceB_TradeDetails_35B_Type_Pattern = MT541_SequenceB_TradeDetails_35B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_94B_Type_Pattern
class MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_94B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_94B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 302, 1)
    _Documentation = None
MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_94B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_94B_Type_Pattern._CF_pattern.addPattern(pattern="(:(PLIS)/([A-Z0-9]{1,8})?/[A-Z0-9]{4}(/[^/]([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,30}[^/])?)")
MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_94B_Type_Pattern._InitializeFacetMap(MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_94B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_94B_Type_Pattern', MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_94B_Type_Pattern)
_module_typeBindings.MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_94B_Type_Pattern = MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_94B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_22F_Type_Pattern
class MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_22F_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_22F_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 315, 1)
    _Documentation = None
MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_22F_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_22F_Type_Pattern._CF_pattern.addPattern(pattern='(:(MICO|FORM|PFRE|PAYS|CFRE)/([A-Z0-9]{1,8})?/[A-Z0-9]{4})')
MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_22F_Type_Pattern._InitializeFacetMap(MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_22F_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_22F_Type_Pattern', MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_22F_Type_Pattern)
_module_typeBindings.MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_22F_Type_Pattern = MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_22F_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_12A_Type_Pattern
class MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_12A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_12A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 328, 1)
    _Documentation = None
MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_12A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_12A_Type_Pattern._CF_pattern.addPattern(pattern="(:(CLAS)/([A-Z0-9]{1,8})?/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,30})")
MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_12A_Type_Pattern._InitializeFacetMap(MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_12A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_12A_Type_Pattern', MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_12A_Type_Pattern)
_module_typeBindings.MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_12A_Type_Pattern = MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_12A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_12B_Type_Pattern
class MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_12B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_12B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 341, 1)
    _Documentation = None
MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_12B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_12B_Type_Pattern._CF_pattern.addPattern(pattern='(:(OPST|OPTI)/([A-Z0-9]{1,8})?/[A-Z0-9]{4})')
MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_12B_Type_Pattern._InitializeFacetMap(MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_12B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_12B_Type_Pattern', MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_12B_Type_Pattern)
_module_typeBindings.MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_12B_Type_Pattern = MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_12B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_12C_Type_Pattern
class MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_12C_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_12C_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 354, 1)
    _Documentation = None
MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_12C_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_12C_Type_Pattern._CF_pattern.addPattern(pattern='(:(CLAS)//[A-Z0-9]{6})')
MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_12C_Type_Pattern._InitializeFacetMap(MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_12C_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_12C_Type_Pattern', MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_12C_Type_Pattern)
_module_typeBindings.MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_12C_Type_Pattern = MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_12C_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_11A_Type_Pattern
class MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_11A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_11A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 367, 1)
    _Documentation = None
MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_11A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_11A_Type_Pattern._CF_pattern.addPattern(pattern='(:(DENO)//(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD))')
MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_11A_Type_Pattern._InitializeFacetMap(MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_11A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_11A_Type_Pattern', MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_11A_Type_Pattern)
_module_typeBindings.MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_11A_Type_Pattern = MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_11A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_98A_Type_Pattern
class MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_98A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_98A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 380, 1)
    _Documentation = None
MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_98A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_98A_Type_Pattern._CF_pattern.addPattern(pattern='(:(COUP|EXPI|FRNR|MATU|ISSU|CALD|PUTT|DDTE|FCOU)//[0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01]))')
MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_98A_Type_Pattern._InitializeFacetMap(MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_98A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_98A_Type_Pattern', MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_98A_Type_Pattern)
_module_typeBindings.MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_98A_Type_Pattern = MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_98A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_92A_Type_Pattern
class MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_92A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_92A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 393, 1)
    _Documentation = None
MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_92A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_92A_Type_Pattern._CF_pattern.addPattern(pattern='(:(PRFC|CUFC|NWFC|INTR|NXRT|INDX|YTMR)//(N)?[0-9,(?0-9)]{1,15})')
MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_92A_Type_Pattern._InitializeFacetMap(MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_92A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_92A_Type_Pattern', MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_92A_Type_Pattern)
_module_typeBindings.MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_92A_Type_Pattern = MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_92A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_13A_Type_Pattern
class MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_13A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_13A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 406, 1)
    _Documentation = None
MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_13A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_13A_Type_Pattern._CF_pattern.addPattern(pattern='(:(COUP)//[A-Z0-9]{3})')
MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_13A_Type_Pattern._InitializeFacetMap(MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_13A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_13A_Type_Pattern', MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_13A_Type_Pattern)
_module_typeBindings.MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_13A_Type_Pattern = MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_13A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_13B_Type_Pattern
class MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_13B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_13B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 419, 1)
    _Documentation = None
MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_13B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_13B_Type_Pattern._CF_pattern.addPattern(pattern="(:(COUP|POOL)/([A-Z0-9]{1,8})?/[^/]([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,30}[^/])")
MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_13B_Type_Pattern._InitializeFacetMap(MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_13B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_13B_Type_Pattern', MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_13B_Type_Pattern)
_module_typeBindings.MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_13B_Type_Pattern = MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_13B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_17B_Type_Pattern
class MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_17B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_17B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 432, 1)
    _Documentation = None
MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_17B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_17B_Type_Pattern._CF_pattern.addPattern(pattern='(:(FRNF|CALL|PUTT)//(N|Y))')
MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_17B_Type_Pattern._InitializeFacetMap(MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_17B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_17B_Type_Pattern', MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_17B_Type_Pattern)
_module_typeBindings.MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_17B_Type_Pattern = MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_17B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_90A_Type_Pattern
class MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_90A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_90A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 445, 1)
    _Documentation = None
MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_90A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_90A_Type_Pattern._CF_pattern.addPattern(pattern='(:(INDC|MRKT|EXER)//(DISC|PRCT|PREM|YIEL)/(N)?[0-9,(?0-9)]{1,15})')
MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_90A_Type_Pattern._InitializeFacetMap(MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_90A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_90A_Type_Pattern', MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_90A_Type_Pattern)
_module_typeBindings.MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_90A_Type_Pattern = MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_90A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_90B_Type_Pattern
class MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_90B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_90B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 458, 1)
    _Documentation = None
MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_90B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_90B_Type_Pattern._CF_pattern.addPattern(pattern='(:(INDC|MRKT|EXER)//(ACTU|DISC|PREM)/(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})')
MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_90B_Type_Pattern._InitializeFacetMap(MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_90B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_90B_Type_Pattern', MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_90B_Type_Pattern)
_module_typeBindings.MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_90B_Type_Pattern = MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_90B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_36B_Type_Pattern
class MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_36B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_36B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 471, 1)
    _Documentation = None
MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_36B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_36B_Type_Pattern._CF_pattern.addPattern(pattern='(:(MINO|SIZE)//(AMOR|FAMT|UNIT)/[0-9,(?0-9)]{1,15})')
MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_36B_Type_Pattern._InitializeFacetMap(MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_36B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_36B_Type_Pattern', MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_36B_Type_Pattern)
_module_typeBindings.MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_36B_Type_Pattern = MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_36B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_35B_Type_Pattern
class MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_35B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_35B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 484, 1)
    _Documentation = None
MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_35B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_35B_Type_Pattern._CF_pattern.addPattern(pattern="((ISIN {1}[A-Z0-9]{12})?(\\n(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})?)")
MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_35B_Type_Pattern._InitializeFacetMap(MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_35B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_35B_Type_Pattern', MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_35B_Type_Pattern)
_module_typeBindings.MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_35B_Type_Pattern = MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_35B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_70E_Type_Pattern
class MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_70E_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_70E_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 497, 1)
    _Documentation = None
MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_70E_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_70E_Type_Pattern._CF_pattern.addPattern(pattern="(:(FIAN)//(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,10})")
MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_70E_Type_Pattern._InitializeFacetMap(MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_70E_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_70E_Type_Pattern', MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_70E_Type_Pattern)
_module_typeBindings.MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_70E_Type_Pattern = MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_70E_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceB_TradeDetails_22F_Type_Pattern
class MT541_SequenceB_TradeDetails_22F_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceB_TradeDetails_22F_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 510, 1)
    _Documentation = None
MT541_SequenceB_TradeDetails_22F_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceB_TradeDetails_22F_Type_Pattern._CF_pattern.addPattern(pattern='(:(PROC|RPOR|PRIR|BORR|TTCO|INCA|TRCA|PRIC)/([A-Z0-9]{1,8})?/[A-Z0-9]{4})')
MT541_SequenceB_TradeDetails_22F_Type_Pattern._InitializeFacetMap(MT541_SequenceB_TradeDetails_22F_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceB_TradeDetails_22F_Type_Pattern', MT541_SequenceB_TradeDetails_22F_Type_Pattern)
_module_typeBindings.MT541_SequenceB_TradeDetails_22F_Type_Pattern = MT541_SequenceB_TradeDetails_22F_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceB_TradeDetails_11A_Type_Pattern
class MT541_SequenceB_TradeDetails_11A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceB_TradeDetails_11A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 523, 1)
    _Documentation = None
MT541_SequenceB_TradeDetails_11A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceB_TradeDetails_11A_Type_Pattern._CF_pattern.addPattern(pattern='(:(FXIS)//(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD))')
MT541_SequenceB_TradeDetails_11A_Type_Pattern._InitializeFacetMap(MT541_SequenceB_TradeDetails_11A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceB_TradeDetails_11A_Type_Pattern', MT541_SequenceB_TradeDetails_11A_Type_Pattern)
_module_typeBindings.MT541_SequenceB_TradeDetails_11A_Type_Pattern = MT541_SequenceB_TradeDetails_11A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceB_TradeDetails_25D_Type_Pattern
class MT541_SequenceB_TradeDetails_25D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceB_TradeDetails_25D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 536, 1)
    _Documentation = None
MT541_SequenceB_TradeDetails_25D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceB_TradeDetails_25D_Type_Pattern._CF_pattern.addPattern(pattern='(:(MTCH|AFFM)/([A-Z0-9]{1,8})?/[A-Z0-9]{4})')
MT541_SequenceB_TradeDetails_25D_Type_Pattern._InitializeFacetMap(MT541_SequenceB_TradeDetails_25D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceB_TradeDetails_25D_Type_Pattern', MT541_SequenceB_TradeDetails_25D_Type_Pattern)
_module_typeBindings.MT541_SequenceB_TradeDetails_25D_Type_Pattern = MT541_SequenceB_TradeDetails_25D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceB_TradeDetails_70E_Type_Pattern
class MT541_SequenceB_TradeDetails_70E_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceB_TradeDetails_70E_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 549, 1)
    _Documentation = None
MT541_SequenceB_TradeDetails_70E_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceB_TradeDetails_70E_Type_Pattern._CF_pattern.addPattern(pattern="(:(FXIN|SPRO)//(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,10})")
MT541_SequenceB_TradeDetails_70E_Type_Pattern._InitializeFacetMap(MT541_SequenceB_TradeDetails_70E_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceB_TradeDetails_70E_Type_Pattern', MT541_SequenceB_TradeDetails_70E_Type_Pattern)
_module_typeBindings.MT541_SequenceB_TradeDetails_70E_Type_Pattern = MT541_SequenceB_TradeDetails_70E_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceC_FinancialInstrumentAccount_36B_Type_Pattern
class MT541_SequenceC_FinancialInstrumentAccount_36B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceC_FinancialInstrumentAccount_36B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 562, 1)
    _Documentation = None
MT541_SequenceC_FinancialInstrumentAccount_36B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceC_FinancialInstrumentAccount_36B_Type_Pattern._CF_pattern.addPattern(pattern='(:(SETT)//(AMOR|FAMT|UNIT)/[0-9,(?0-9)]{1,15})')
MT541_SequenceC_FinancialInstrumentAccount_36B_Type_Pattern._InitializeFacetMap(MT541_SequenceC_FinancialInstrumentAccount_36B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceC_FinancialInstrumentAccount_36B_Type_Pattern', MT541_SequenceC_FinancialInstrumentAccount_36B_Type_Pattern)
_module_typeBindings.MT541_SequenceC_FinancialInstrumentAccount_36B_Type_Pattern = MT541_SequenceC_FinancialInstrumentAccount_36B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceC_FinancialInstrumentAccount_70D_Type_Pattern
class MT541_SequenceC_FinancialInstrumentAccount_70D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceC_FinancialInstrumentAccount_70D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 575, 1)
    _Documentation = None
MT541_SequenceC_FinancialInstrumentAccount_70D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceC_FinancialInstrumentAccount_70D_Type_Pattern._CF_pattern.addPattern(pattern="(:(DENC)//(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,6})")
MT541_SequenceC_FinancialInstrumentAccount_70D_Type_Pattern._InitializeFacetMap(MT541_SequenceC_FinancialInstrumentAccount_70D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceC_FinancialInstrumentAccount_70D_Type_Pattern', MT541_SequenceC_FinancialInstrumentAccount_70D_Type_Pattern)
_module_typeBindings.MT541_SequenceC_FinancialInstrumentAccount_70D_Type_Pattern = MT541_SequenceC_FinancialInstrumentAccount_70D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceC_FinancialInstrumentAccount_13B_Type_Pattern
class MT541_SequenceC_FinancialInstrumentAccount_13B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceC_FinancialInstrumentAccount_13B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 588, 1)
    _Documentation = None
MT541_SequenceC_FinancialInstrumentAccount_13B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceC_FinancialInstrumentAccount_13B_Type_Pattern._CF_pattern.addPattern(pattern="(:(CERT)/([A-Z0-9]{1,8})?/[^/]([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,30}[^/])")
MT541_SequenceC_FinancialInstrumentAccount_13B_Type_Pattern._InitializeFacetMap(MT541_SequenceC_FinancialInstrumentAccount_13B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceC_FinancialInstrumentAccount_13B_Type_Pattern', MT541_SequenceC_FinancialInstrumentAccount_13B_Type_Pattern)
_module_typeBindings.MT541_SequenceC_FinancialInstrumentAccount_13B_Type_Pattern = MT541_SequenceC_FinancialInstrumentAccount_13B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceC_FinancialInstrumentAccount_95L_Type_Pattern
class MT541_SequenceC_FinancialInstrumentAccount_95L_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceC_FinancialInstrumentAccount_95L_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 601, 1)
    _Documentation = None
MT541_SequenceC_FinancialInstrumentAccount_95L_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceC_FinancialInstrumentAccount_95L_Type_Pattern._CF_pattern.addPattern(pattern='(:(ALTE)//[A-Z0-9]{18}[0-9]{2})')
MT541_SequenceC_FinancialInstrumentAccount_95L_Type_Pattern._InitializeFacetMap(MT541_SequenceC_FinancialInstrumentAccount_95L_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceC_FinancialInstrumentAccount_95L_Type_Pattern', MT541_SequenceC_FinancialInstrumentAccount_95L_Type_Pattern)
_module_typeBindings.MT541_SequenceC_FinancialInstrumentAccount_95L_Type_Pattern = MT541_SequenceC_FinancialInstrumentAccount_95L_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceC_FinancialInstrumentAccount_95P_Type_Pattern
class MT541_SequenceC_FinancialInstrumentAccount_95P_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceC_FinancialInstrumentAccount_95P_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 614, 1)
    _Documentation = None
MT541_SequenceC_FinancialInstrumentAccount_95P_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceC_FinancialInstrumentAccount_95P_Type_Pattern._CF_pattern.addPattern(pattern='(:(ACOW)//[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)')
MT541_SequenceC_FinancialInstrumentAccount_95P_Type_Pattern._InitializeFacetMap(MT541_SequenceC_FinancialInstrumentAccount_95P_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceC_FinancialInstrumentAccount_95P_Type_Pattern', MT541_SequenceC_FinancialInstrumentAccount_95P_Type_Pattern)
_module_typeBindings.MT541_SequenceC_FinancialInstrumentAccount_95P_Type_Pattern = MT541_SequenceC_FinancialInstrumentAccount_95P_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceC_FinancialInstrumentAccount_95R_Type_Pattern
class MT541_SequenceC_FinancialInstrumentAccount_95R_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceC_FinancialInstrumentAccount_95R_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 627, 1)
    _Documentation = None
MT541_SequenceC_FinancialInstrumentAccount_95R_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceC_FinancialInstrumentAccount_95R_Type_Pattern._CF_pattern.addPattern(pattern="(:(ACOW)/[A-Z0-9]{1,8}/[^/]([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34}[^/])")
MT541_SequenceC_FinancialInstrumentAccount_95R_Type_Pattern._InitializeFacetMap(MT541_SequenceC_FinancialInstrumentAccount_95R_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceC_FinancialInstrumentAccount_95R_Type_Pattern', MT541_SequenceC_FinancialInstrumentAccount_95R_Type_Pattern)
_module_typeBindings.MT541_SequenceC_FinancialInstrumentAccount_95R_Type_Pattern = MT541_SequenceC_FinancialInstrumentAccount_95R_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceC_FinancialInstrumentAccount_97A_Type_Pattern
class MT541_SequenceC_FinancialInstrumentAccount_97A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceC_FinancialInstrumentAccount_97A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 640, 1)
    _Documentation = None
MT541_SequenceC_FinancialInstrumentAccount_97A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceC_FinancialInstrumentAccount_97A_Type_Pattern._CF_pattern.addPattern(pattern="(:(SAFE|CASH)//([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35})")
MT541_SequenceC_FinancialInstrumentAccount_97A_Type_Pattern._InitializeFacetMap(MT541_SequenceC_FinancialInstrumentAccount_97A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceC_FinancialInstrumentAccount_97A_Type_Pattern', MT541_SequenceC_FinancialInstrumentAccount_97A_Type_Pattern)
_module_typeBindings.MT541_SequenceC_FinancialInstrumentAccount_97A_Type_Pattern = MT541_SequenceC_FinancialInstrumentAccount_97A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceC_FinancialInstrumentAccount_97B_Type_Pattern
class MT541_SequenceC_FinancialInstrumentAccount_97B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceC_FinancialInstrumentAccount_97B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 653, 1)
    _Documentation = None
MT541_SequenceC_FinancialInstrumentAccount_97B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceC_FinancialInstrumentAccount_97B_Type_Pattern._CF_pattern.addPattern(pattern="(:(SAFE)/([A-Z0-9]{1,8})?/[A-Z0-9]{4}/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35})")
MT541_SequenceC_FinancialInstrumentAccount_97B_Type_Pattern._InitializeFacetMap(MT541_SequenceC_FinancialInstrumentAccount_97B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceC_FinancialInstrumentAccount_97B_Type_Pattern', MT541_SequenceC_FinancialInstrumentAccount_97B_Type_Pattern)
_module_typeBindings.MT541_SequenceC_FinancialInstrumentAccount_97B_Type_Pattern = MT541_SequenceC_FinancialInstrumentAccount_97B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceC_FinancialInstrumentAccount_97E_Type_Pattern
class MT541_SequenceC_FinancialInstrumentAccount_97E_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceC_FinancialInstrumentAccount_97E_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 666, 1)
    _Documentation = None
MT541_SequenceC_FinancialInstrumentAccount_97E_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceC_FinancialInstrumentAccount_97E_Type_Pattern._CF_pattern.addPattern(pattern="(:(CASH)//([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})")
MT541_SequenceC_FinancialInstrumentAccount_97E_Type_Pattern._InitializeFacetMap(MT541_SequenceC_FinancialInstrumentAccount_97E_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceC_FinancialInstrumentAccount_97E_Type_Pattern', MT541_SequenceC_FinancialInstrumentAccount_97E_Type_Pattern)
_module_typeBindings.MT541_SequenceC_FinancialInstrumentAccount_97E_Type_Pattern = MT541_SequenceC_FinancialInstrumentAccount_97E_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceC_FinancialInstrumentAccount_94B_Type_Pattern
class MT541_SequenceC_FinancialInstrumentAccount_94B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceC_FinancialInstrumentAccount_94B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 679, 1)
    _Documentation = None
MT541_SequenceC_FinancialInstrumentAccount_94B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceC_FinancialInstrumentAccount_94B_Type_Pattern._CF_pattern.addPattern(pattern="(:(SAFE)/([A-Z0-9]{1,8})?/[A-Z0-9]{4}(/[^/]([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,30}[^/])?)")
MT541_SequenceC_FinancialInstrumentAccount_94B_Type_Pattern._InitializeFacetMap(MT541_SequenceC_FinancialInstrumentAccount_94B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceC_FinancialInstrumentAccount_94B_Type_Pattern', MT541_SequenceC_FinancialInstrumentAccount_94B_Type_Pattern)
_module_typeBindings.MT541_SequenceC_FinancialInstrumentAccount_94B_Type_Pattern = MT541_SequenceC_FinancialInstrumentAccount_94B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceC_FinancialInstrumentAccount_94C_Type_Pattern
class MT541_SequenceC_FinancialInstrumentAccount_94C_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceC_FinancialInstrumentAccount_94C_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 692, 1)
    _Documentation = None
MT541_SequenceC_FinancialInstrumentAccount_94C_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceC_FinancialInstrumentAccount_94C_Type_Pattern._CF_pattern.addPattern(pattern='(:(SAFE)//[A-Z]{2})')
MT541_SequenceC_FinancialInstrumentAccount_94C_Type_Pattern._InitializeFacetMap(MT541_SequenceC_FinancialInstrumentAccount_94C_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceC_FinancialInstrumentAccount_94C_Type_Pattern', MT541_SequenceC_FinancialInstrumentAccount_94C_Type_Pattern)
_module_typeBindings.MT541_SequenceC_FinancialInstrumentAccount_94C_Type_Pattern = MT541_SequenceC_FinancialInstrumentAccount_94C_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceC_FinancialInstrumentAccount_94F_Type_Pattern
class MT541_SequenceC_FinancialInstrumentAccount_94F_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceC_FinancialInstrumentAccount_94F_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 705, 1)
    _Documentation = None
MT541_SequenceC_FinancialInstrumentAccount_94F_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceC_FinancialInstrumentAccount_94F_Type_Pattern._CF_pattern.addPattern(pattern='(:(SAFE)//(CUST|ICSD|NCSD|SHHE)/[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)')
MT541_SequenceC_FinancialInstrumentAccount_94F_Type_Pattern._InitializeFacetMap(MT541_SequenceC_FinancialInstrumentAccount_94F_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceC_FinancialInstrumentAccount_94F_Type_Pattern', MT541_SequenceC_FinancialInstrumentAccount_94F_Type_Pattern)
_module_typeBindings.MT541_SequenceC_FinancialInstrumentAccount_94F_Type_Pattern = MT541_SequenceC_FinancialInstrumentAccount_94F_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceC_FinancialInstrumentAccount_94L_Type_Pattern
class MT541_SequenceC_FinancialInstrumentAccount_94L_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceC_FinancialInstrumentAccount_94L_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 718, 1)
    _Documentation = None
MT541_SequenceC_FinancialInstrumentAccount_94L_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceC_FinancialInstrumentAccount_94L_Type_Pattern._CF_pattern.addPattern(pattern='(:(SAFE)//[A-Z0-9]{18}[0-9]{2})')
MT541_SequenceC_FinancialInstrumentAccount_94L_Type_Pattern._InitializeFacetMap(MT541_SequenceC_FinancialInstrumentAccount_94L_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceC_FinancialInstrumentAccount_94L_Type_Pattern', MT541_SequenceC_FinancialInstrumentAccount_94L_Type_Pattern)
_module_typeBindings.MT541_SequenceC_FinancialInstrumentAccount_94L_Type_Pattern = MT541_SequenceC_FinancialInstrumentAccount_94L_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_13B_Type_Pattern
class MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_13B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_13B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 731, 1)
    _Documentation = None
MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_13B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_13B_Type_Pattern._CF_pattern.addPattern(pattern="(:(LOTS)/([A-Z0-9]{1,8})?/[^/]([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,30}[^/])")
MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_13B_Type_Pattern._InitializeFacetMap(MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_13B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_13B_Type_Pattern', MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_13B_Type_Pattern)
_module_typeBindings.MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_13B_Type_Pattern = MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_13B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_36B_Type_Pattern
class MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_36B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_36B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 744, 1)
    _Documentation = None
MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_36B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_36B_Type_Pattern._CF_pattern.addPattern(pattern='(:(LOTS)//(AMOR|FAMT|UNIT)/[0-9,(?0-9)]{1,15})')
MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_36B_Type_Pattern._InitializeFacetMap(MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_36B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_36B_Type_Pattern', MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_36B_Type_Pattern)
_module_typeBindings.MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_36B_Type_Pattern = MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_36B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_98A_Type_Pattern
class MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_98A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_98A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 757, 1)
    _Documentation = None
MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_98A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_98A_Type_Pattern._CF_pattern.addPattern(pattern='(:(LOTS)//[0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01]))')
MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_98A_Type_Pattern._InitializeFacetMap(MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_98A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_98A_Type_Pattern', MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_98A_Type_Pattern)
_module_typeBindings.MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_98A_Type_Pattern = MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_98A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_98C_Type_Pattern
class MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_98C_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_98C_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 770, 1)
    _Documentation = None
MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_98C_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_98C_Type_Pattern._CF_pattern.addPattern(pattern='(:(LOTS)//[0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])(0[0-9]|[1][0-9]|2[1-3])([0-5][0-9])([0-5][0-9]))')
MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_98C_Type_Pattern._InitializeFacetMap(MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_98C_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_98C_Type_Pattern', MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_98C_Type_Pattern)
_module_typeBindings.MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_98C_Type_Pattern = MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_98C_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_98E_Type_Pattern
class MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_98E_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_98E_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 783, 1)
    _Documentation = None
MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_98E_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_98E_Type_Pattern._CF_pattern.addPattern(pattern='(:(LOTS)//[0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])(0[0-9]|[1][0-9]|2[1-3])([0-5][0-9])([0-5][0-9])(,[0-9]{1,3})?(/(N)?(0[0-9]|[1][0-9]|2[1-3])(([0-5][0-9]))?)?)')
MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_98E_Type_Pattern._InitializeFacetMap(MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_98E_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_98E_Type_Pattern', MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_98E_Type_Pattern)
_module_typeBindings.MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_98E_Type_Pattern = MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_98E_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_90A_Type_Pattern
class MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_90A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_90A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 796, 1)
    _Documentation = None
MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_90A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_90A_Type_Pattern._CF_pattern.addPattern(pattern='(:(LOTS)//(DISC|PRCT|PREM|YIEL)/(N)?[0-9,(?0-9)]{1,15})')
MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_90A_Type_Pattern._InitializeFacetMap(MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_90A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_90A_Type_Pattern', MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_90A_Type_Pattern)
_module_typeBindings.MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_90A_Type_Pattern = MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_90A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_90B_Type_Pattern
class MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_90B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_90B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 809, 1)
    _Documentation = None
MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_90B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_90B_Type_Pattern._CF_pattern.addPattern(pattern='(:(LOTS)//(ACTU|DISC|PREM)/(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})')
MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_90B_Type_Pattern._InitializeFacetMap(MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_90B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_90B_Type_Pattern', MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_90B_Type_Pattern)
_module_typeBindings.MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_90B_Type_Pattern = MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_90B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_22F_Type_Pattern
class MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_22F_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_22F_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 822, 1)
    _Documentation = None
MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_22F_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_22F_Type_Pattern._CF_pattern.addPattern(pattern='(:(PRIC)/([A-Z0-9]{1,8})?/[A-Z0-9]{4})')
MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_22F_Type_Pattern._InitializeFacetMap(MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_22F_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_22F_Type_Pattern', MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_22F_Type_Pattern)
_module_typeBindings.MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_22F_Type_Pattern = MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_22F_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceD_TwoLegTransactionDetails_98A_Type_Pattern
class MT541_SequenceD_TwoLegTransactionDetails_98A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceD_TwoLegTransactionDetails_98A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 835, 1)
    _Documentation = None
MT541_SequenceD_TwoLegTransactionDetails_98A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceD_TwoLegTransactionDetails_98A_Type_Pattern._CF_pattern.addPattern(pattern='(:(TERM|RERA)//[0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01]))')
MT541_SequenceD_TwoLegTransactionDetails_98A_Type_Pattern._InitializeFacetMap(MT541_SequenceD_TwoLegTransactionDetails_98A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceD_TwoLegTransactionDetails_98A_Type_Pattern', MT541_SequenceD_TwoLegTransactionDetails_98A_Type_Pattern)
_module_typeBindings.MT541_SequenceD_TwoLegTransactionDetails_98A_Type_Pattern = MT541_SequenceD_TwoLegTransactionDetails_98A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceD_TwoLegTransactionDetails_98B_Type_Pattern
class MT541_SequenceD_TwoLegTransactionDetails_98B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceD_TwoLegTransactionDetails_98B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 848, 1)
    _Documentation = None
MT541_SequenceD_TwoLegTransactionDetails_98B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceD_TwoLegTransactionDetails_98B_Type_Pattern._CF_pattern.addPattern(pattern='(:(TERM)/([A-Z0-9]{1,8})?/[A-Z0-9]{4})')
MT541_SequenceD_TwoLegTransactionDetails_98B_Type_Pattern._InitializeFacetMap(MT541_SequenceD_TwoLegTransactionDetails_98B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceD_TwoLegTransactionDetails_98B_Type_Pattern', MT541_SequenceD_TwoLegTransactionDetails_98B_Type_Pattern)
_module_typeBindings.MT541_SequenceD_TwoLegTransactionDetails_98B_Type_Pattern = MT541_SequenceD_TwoLegTransactionDetails_98B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceD_TwoLegTransactionDetails_98C_Type_Pattern
class MT541_SequenceD_TwoLegTransactionDetails_98C_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceD_TwoLegTransactionDetails_98C_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 861, 1)
    _Documentation = None
MT541_SequenceD_TwoLegTransactionDetails_98C_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceD_TwoLegTransactionDetails_98C_Type_Pattern._CF_pattern.addPattern(pattern='(:(TERM|RERA)//[0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])(0[0-9]|[1][0-9]|2[1-3])([0-5][0-9])([0-5][0-9]))')
MT541_SequenceD_TwoLegTransactionDetails_98C_Type_Pattern._InitializeFacetMap(MT541_SequenceD_TwoLegTransactionDetails_98C_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceD_TwoLegTransactionDetails_98C_Type_Pattern', MT541_SequenceD_TwoLegTransactionDetails_98C_Type_Pattern)
_module_typeBindings.MT541_SequenceD_TwoLegTransactionDetails_98C_Type_Pattern = MT541_SequenceD_TwoLegTransactionDetails_98C_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceD_TwoLegTransactionDetails_22F_Type_Pattern
class MT541_SequenceD_TwoLegTransactionDetails_22F_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceD_TwoLegTransactionDetails_22F_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 874, 1)
    _Documentation = None
MT541_SequenceD_TwoLegTransactionDetails_22F_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceD_TwoLegTransactionDetails_22F_Type_Pattern._CF_pattern.addPattern(pattern='(:(RERT|MICO|REVA|LEGA|OMAT|INTR)/([A-Z0-9]{1,8})?/[A-Z0-9]{4})')
MT541_SequenceD_TwoLegTransactionDetails_22F_Type_Pattern._InitializeFacetMap(MT541_SequenceD_TwoLegTransactionDetails_22F_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceD_TwoLegTransactionDetails_22F_Type_Pattern', MT541_SequenceD_TwoLegTransactionDetails_22F_Type_Pattern)
_module_typeBindings.MT541_SequenceD_TwoLegTransactionDetails_22F_Type_Pattern = MT541_SequenceD_TwoLegTransactionDetails_22F_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceD_TwoLegTransactionDetails_20C_Type_Pattern
class MT541_SequenceD_TwoLegTransactionDetails_20C_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceD_TwoLegTransactionDetails_20C_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 887, 1)
    _Documentation = None
MT541_SequenceD_TwoLegTransactionDetails_20C_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceD_TwoLegTransactionDetails_20C_Type_Pattern._CF_pattern.addPattern(pattern="(:(SECO|REPO)//[^/]([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,16}[^/])")
MT541_SequenceD_TwoLegTransactionDetails_20C_Type_Pattern._InitializeFacetMap(MT541_SequenceD_TwoLegTransactionDetails_20C_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceD_TwoLegTransactionDetails_20C_Type_Pattern', MT541_SequenceD_TwoLegTransactionDetails_20C_Type_Pattern)
_module_typeBindings.MT541_SequenceD_TwoLegTransactionDetails_20C_Type_Pattern = MT541_SequenceD_TwoLegTransactionDetails_20C_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceD_TwoLegTransactionDetails_92A_Type_Pattern
class MT541_SequenceD_TwoLegTransactionDetails_92A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceD_TwoLegTransactionDetails_92A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 900, 1)
    _Documentation = None
MT541_SequenceD_TwoLegTransactionDetails_92A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceD_TwoLegTransactionDetails_92A_Type_Pattern._CF_pattern.addPattern(pattern='(:(REPO|RSPR|PRIC|SLMG|SHAI)//(N)?[0-9,(?0-9)]{1,15})')
MT541_SequenceD_TwoLegTransactionDetails_92A_Type_Pattern._InitializeFacetMap(MT541_SequenceD_TwoLegTransactionDetails_92A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceD_TwoLegTransactionDetails_92A_Type_Pattern', MT541_SequenceD_TwoLegTransactionDetails_92A_Type_Pattern)
_module_typeBindings.MT541_SequenceD_TwoLegTransactionDetails_92A_Type_Pattern = MT541_SequenceD_TwoLegTransactionDetails_92A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceD_TwoLegTransactionDetails_92C_Type_Pattern
class MT541_SequenceD_TwoLegTransactionDetails_92C_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceD_TwoLegTransactionDetails_92C_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 913, 1)
    _Documentation = None
MT541_SequenceD_TwoLegTransactionDetails_92C_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceD_TwoLegTransactionDetails_92C_Type_Pattern._CF_pattern.addPattern(pattern="(:(VASU|PRIC)/([A-Z0-9]{1,8})?/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,24})")
MT541_SequenceD_TwoLegTransactionDetails_92C_Type_Pattern._InitializeFacetMap(MT541_SequenceD_TwoLegTransactionDetails_92C_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceD_TwoLegTransactionDetails_92C_Type_Pattern', MT541_SequenceD_TwoLegTransactionDetails_92C_Type_Pattern)
_module_typeBindings.MT541_SequenceD_TwoLegTransactionDetails_92C_Type_Pattern = MT541_SequenceD_TwoLegTransactionDetails_92C_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceD_TwoLegTransactionDetails_99B_Type_Pattern
class MT541_SequenceD_TwoLegTransactionDetails_99B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceD_TwoLegTransactionDetails_99B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 926, 1)
    _Documentation = None
MT541_SequenceD_TwoLegTransactionDetails_99B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceD_TwoLegTransactionDetails_99B_Type_Pattern._CF_pattern.addPattern(pattern='(:(CADE|TOCO)//[0-9]{3})')
MT541_SequenceD_TwoLegTransactionDetails_99B_Type_Pattern._InitializeFacetMap(MT541_SequenceD_TwoLegTransactionDetails_99B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceD_TwoLegTransactionDetails_99B_Type_Pattern', MT541_SequenceD_TwoLegTransactionDetails_99B_Type_Pattern)
_module_typeBindings.MT541_SequenceD_TwoLegTransactionDetails_99B_Type_Pattern = MT541_SequenceD_TwoLegTransactionDetails_99B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceD_TwoLegTransactionDetails_19A_Type_Pattern
class MT541_SequenceD_TwoLegTransactionDetails_19A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceD_TwoLegTransactionDetails_19A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 939, 1)
    _Documentation = None
MT541_SequenceD_TwoLegTransactionDetails_19A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceD_TwoLegTransactionDetails_19A_Type_Pattern._CF_pattern.addPattern(pattern='(:(FORF|TRTE|REPP|ACRU|DEAL|TAPC)//(N)?(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})')
MT541_SequenceD_TwoLegTransactionDetails_19A_Type_Pattern._InitializeFacetMap(MT541_SequenceD_TwoLegTransactionDetails_19A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceD_TwoLegTransactionDetails_19A_Type_Pattern', MT541_SequenceD_TwoLegTransactionDetails_19A_Type_Pattern)
_module_typeBindings.MT541_SequenceD_TwoLegTransactionDetails_19A_Type_Pattern = MT541_SequenceD_TwoLegTransactionDetails_19A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceD_TwoLegTransactionDetails_70C_Type_Pattern
class MT541_SequenceD_TwoLegTransactionDetails_70C_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceD_TwoLegTransactionDetails_70C_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 952, 1)
    _Documentation = None
MT541_SequenceD_TwoLegTransactionDetails_70C_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceD_TwoLegTransactionDetails_70C_Type_Pattern._CF_pattern.addPattern(pattern="(:(SECO)//(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT541_SequenceD_TwoLegTransactionDetails_70C_Type_Pattern._InitializeFacetMap(MT541_SequenceD_TwoLegTransactionDetails_70C_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceD_TwoLegTransactionDetails_70C_Type_Pattern', MT541_SequenceD_TwoLegTransactionDetails_70C_Type_Pattern)
_module_typeBindings.MT541_SequenceD_TwoLegTransactionDetails_70C_Type_Pattern = MT541_SequenceD_TwoLegTransactionDetails_70C_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceE_SettlementDetails_22F_Type_Pattern
class MT541_SequenceE_SettlementDetails_22F_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceE_SettlementDetails_22F_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 965, 1)
    _Documentation = None
MT541_SequenceE_SettlementDetails_22F_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceE_SettlementDetails_22F_Type_Pattern._CF_pattern.addPattern(pattern='(:(STCO|SETR|TRCA|STAM|RTGS|REGT|BENE|CASY|DBNM|TCPI|MACL|FXCX|BLOC|REST|SETS|NETT|CCPT|LEOG|COLA|TRAK|REPT|COLE|SSBT|CSBT)/([A-Z0-9]{1,8})?/[A-Z0-9]{4})')
MT541_SequenceE_SettlementDetails_22F_Type_Pattern._InitializeFacetMap(MT541_SequenceE_SettlementDetails_22F_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceE_SettlementDetails_22F_Type_Pattern', MT541_SequenceE_SettlementDetails_22F_Type_Pattern)
_module_typeBindings.MT541_SequenceE_SettlementDetails_22F_Type_Pattern = MT541_SequenceE_SettlementDetails_22F_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95C_Type_Pattern
class MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95C_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95C_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 978, 1)
    _Documentation = None
MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95C_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95C_Type_Pattern._CF_pattern.addPattern(pattern='(:(PSET)//[A-Z]{2})')
MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95C_Type_Pattern._InitializeFacetMap(MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95C_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95C_Type_Pattern', MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95C_Type_Pattern)
_module_typeBindings.MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95C_Type_Pattern = MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95C_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95L_Type_Pattern
class MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95L_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95L_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 991, 1)
    _Documentation = None
MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95L_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95L_Type_Pattern._CF_pattern.addPattern(pattern='(:(ALTE)//[A-Z0-9]{18}[0-9]{2})')
MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95L_Type_Pattern._InitializeFacetMap(MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95L_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95L_Type_Pattern', MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95L_Type_Pattern)
_module_typeBindings.MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95L_Type_Pattern = MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95L_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95P_Type_Pattern
class MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95P_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95P_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1004, 1)
    _Documentation = None
MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95P_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95P_Type_Pattern._CF_pattern.addPattern(pattern='(:(BUYR|DEAG|DECU|DEI1|DEI2|PSET|REAG|RECU|REI1|REI2|SELL)//[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)')
MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95P_Type_Pattern._InitializeFacetMap(MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95P_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95P_Type_Pattern', MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95P_Type_Pattern)
_module_typeBindings.MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95P_Type_Pattern = MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95P_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95Q_Type_Pattern
class MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95Q_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95Q_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1017, 1)
    _Documentation = None
MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95Q_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95Q_Type_Pattern._CF_pattern.addPattern(pattern="(:(BUYR|DEAG|DECU|DEI1|DEI2|PSET|REAG|RECU|REI1|REI2|SELL)//(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95Q_Type_Pattern._InitializeFacetMap(MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95Q_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95Q_Type_Pattern', MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95Q_Type_Pattern)
_module_typeBindings.MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95Q_Type_Pattern = MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95Q_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95R_Type_Pattern
class MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95R_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95R_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1030, 1)
    _Documentation = None
MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95R_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95R_Type_Pattern._CF_pattern.addPattern(pattern="(:(BUYR|DEAG|DECU|DEI1|DEI2|REAG|RECU|REI1|REI2|SELL)/[A-Z0-9]{1,8}/[^/]([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34}[^/])")
MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95R_Type_Pattern._InitializeFacetMap(MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95R_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95R_Type_Pattern', MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95R_Type_Pattern)
_module_typeBindings.MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95R_Type_Pattern = MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95R_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95S_Type_Pattern
class MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95S_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95S_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1043, 1)
    _Documentation = None
MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95S_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95S_Type_Pattern._CF_pattern.addPattern(pattern="(:(ALTE)/([A-Z0-9]{1,8})?/[A-Z0-9]{4}/[A-Z]{2}/[^/]([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,30}[^/])")
MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95S_Type_Pattern._InitializeFacetMap(MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95S_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95S_Type_Pattern', MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95S_Type_Pattern)
_module_typeBindings.MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95S_Type_Pattern = MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95S_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_97A_Type_Pattern
class MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_97A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_97A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1056, 1)
    _Documentation = None
MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_97A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_97A_Type_Pattern._CF_pattern.addPattern(pattern="(:(SAFE)//([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35})")
MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_97A_Type_Pattern._InitializeFacetMap(MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_97A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_97A_Type_Pattern', MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_97A_Type_Pattern)
_module_typeBindings.MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_97A_Type_Pattern = MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_97A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_97B_Type_Pattern
class MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_97B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_97B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1069, 1)
    _Documentation = None
MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_97B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_97B_Type_Pattern._CF_pattern.addPattern(pattern="(:(SAFE)/([A-Z0-9]{1,8})?/[A-Z0-9]{4}/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35})")
MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_97B_Type_Pattern._InitializeFacetMap(MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_97B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_97B_Type_Pattern', MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_97B_Type_Pattern)
_module_typeBindings.MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_97B_Type_Pattern = MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_97B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_98A_Type_Pattern
class MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_98A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_98A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1082, 1)
    _Documentation = None
MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_98A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_98A_Type_Pattern._CF_pattern.addPattern(pattern='(:(PROC)//[0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01]))')
MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_98A_Type_Pattern._InitializeFacetMap(MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_98A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_98A_Type_Pattern', MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_98A_Type_Pattern)
_module_typeBindings.MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_98A_Type_Pattern = MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_98A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_98C_Type_Pattern
class MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_98C_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_98C_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1095, 1)
    _Documentation = None
MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_98C_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_98C_Type_Pattern._CF_pattern.addPattern(pattern='(:(PROC)//[0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])(0[0-9]|[1][0-9]|2[1-3])([0-5][0-9])([0-5][0-9]))')
MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_98C_Type_Pattern._InitializeFacetMap(MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_98C_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_98C_Type_Pattern', MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_98C_Type_Pattern)
_module_typeBindings.MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_98C_Type_Pattern = MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_98C_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_20C_Type_Pattern
class MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_20C_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_20C_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1108, 1)
    _Documentation = None
MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_20C_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_20C_Type_Pattern._CF_pattern.addPattern(pattern="(:(PROC)//[^/]([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,16}[^/])")
MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_20C_Type_Pattern._InitializeFacetMap(MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_20C_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_20C_Type_Pattern', MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_20C_Type_Pattern)
_module_typeBindings.MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_20C_Type_Pattern = MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_20C_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_70C_Type_Pattern
class MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_70C_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_70C_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1121, 1)
    _Documentation = None
MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_70C_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_70C_Type_Pattern._CF_pattern.addPattern(pattern="(:(PACO)//(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_70C_Type_Pattern._InitializeFacetMap(MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_70C_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_70C_Type_Pattern', MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_70C_Type_Pattern)
_module_typeBindings.MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_70C_Type_Pattern = MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_70C_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_70D_Type_Pattern
class MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_70D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_70D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1134, 1)
    _Documentation = None
MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_70D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_70D_Type_Pattern._CF_pattern.addPattern(pattern="(:(REGI)//(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,6})")
MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_70D_Type_Pattern._InitializeFacetMap(MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_70D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_70D_Type_Pattern', MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_70D_Type_Pattern)
_module_typeBindings.MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_70D_Type_Pattern = MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_70D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_70E_Type_Pattern
class MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_70E_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_70E_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1147, 1)
    _Documentation = None
MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_70E_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_70E_Type_Pattern._CF_pattern.addPattern(pattern="(:(DECL)//(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,10})")
MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_70E_Type_Pattern._InitializeFacetMap(MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_70E_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_70E_Type_Pattern', MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_70E_Type_Pattern)
_module_typeBindings.MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_70E_Type_Pattern = MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_70E_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95L_Type_Pattern
class MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95L_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95L_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1160, 1)
    _Documentation = None
MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95L_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95L_Type_Pattern._CF_pattern.addPattern(pattern='(:(ALTE)//[A-Z0-9]{18}[0-9]{2})')
MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95L_Type_Pattern._InitializeFacetMap(MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95L_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95L_Type_Pattern', MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95L_Type_Pattern)
_module_typeBindings.MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95L_Type_Pattern = MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95L_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95P_Type_Pattern
class MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95P_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95P_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1173, 1)
    _Documentation = None
MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95P_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95P_Type_Pattern._CF_pattern.addPattern(pattern='(:(ACCW|BENM|DEBT|INTM|PAYE)//[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)')
MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95P_Type_Pattern._InitializeFacetMap(MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95P_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95P_Type_Pattern', MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95P_Type_Pattern)
_module_typeBindings.MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95P_Type_Pattern = MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95P_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95Q_Type_Pattern
class MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95Q_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95Q_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1186, 1)
    _Documentation = None
MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95Q_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95Q_Type_Pattern._CF_pattern.addPattern(pattern="(:(ACCW|BENM|DEBT|INTM|PAYE)//(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95Q_Type_Pattern._InitializeFacetMap(MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95Q_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95Q_Type_Pattern', MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95Q_Type_Pattern)
_module_typeBindings.MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95Q_Type_Pattern = MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95Q_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95R_Type_Pattern
class MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95R_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95R_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1199, 1)
    _Documentation = None
MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95R_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95R_Type_Pattern._CF_pattern.addPattern(pattern="(:(ACCW|BENM|DEBT|INTM|PAYE)/[A-Z0-9]{1,8}/[^/]([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34}[^/])")
MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95R_Type_Pattern._InitializeFacetMap(MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95R_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95R_Type_Pattern', MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95R_Type_Pattern)
_module_typeBindings.MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95R_Type_Pattern = MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95R_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95S_Type_Pattern
class MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95S_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95S_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1212, 1)
    _Documentation = None
MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95S_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95S_Type_Pattern._CF_pattern.addPattern(pattern="(:(ALTE)/([A-Z0-9]{1,8})?/[A-Z0-9]{4}/[A-Z]{2}/[^/]([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,30}[^/])")
MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95S_Type_Pattern._InitializeFacetMap(MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95S_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95S_Type_Pattern', MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95S_Type_Pattern)
_module_typeBindings.MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95S_Type_Pattern = MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95S_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_97A_Type_Pattern
class MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_97A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_97A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1225, 1)
    _Documentation = None
MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_97A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_97A_Type_Pattern._CF_pattern.addPattern(pattern="(:(CASH|CHAR|COMM|TAXE)//([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35})")
MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_97A_Type_Pattern._InitializeFacetMap(MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_97A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_97A_Type_Pattern', MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_97A_Type_Pattern)
_module_typeBindings.MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_97A_Type_Pattern = MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_97A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_97E_Type_Pattern
class MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_97E_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_97E_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1238, 1)
    _Documentation = None
MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_97E_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_97E_Type_Pattern._CF_pattern.addPattern(pattern="(:(CASH|CHAR|COMM|TAXE)//([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})")
MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_97E_Type_Pattern._InitializeFacetMap(MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_97E_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_97E_Type_Pattern', MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_97E_Type_Pattern)
_module_typeBindings.MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_97E_Type_Pattern = MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_97E_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_70C_Type_Pattern
class MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_70C_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_70C_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1251, 1)
    _Documentation = None
MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_70C_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_70C_Type_Pattern._CF_pattern.addPattern(pattern="(:(PACO)//(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_70C_Type_Pattern._InitializeFacetMap(MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_70C_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_70C_Type_Pattern', MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_70C_Type_Pattern)
_module_typeBindings.MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_70C_Type_Pattern = MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_70C_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_70E_Type_Pattern
class MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_70E_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_70E_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1264, 1)
    _Documentation = None
MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_70E_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_70E_Type_Pattern._CF_pattern.addPattern(pattern="(:(DECL)//(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,10})")
MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_70E_Type_Pattern._InitializeFacetMap(MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_70E_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_70E_Type_Pattern', MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_70E_Type_Pattern)
_module_typeBindings.MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_70E_Type_Pattern = MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_70E_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_17B_Type_Pattern
class MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_17B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_17B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1277, 1)
    _Documentation = None
MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_17B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_17B_Type_Pattern._CF_pattern.addPattern(pattern='(:(ACRU|STAM|EXEC)//(N|Y))')
MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_17B_Type_Pattern._InitializeFacetMap(MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_17B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_17B_Type_Pattern', MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_17B_Type_Pattern)
_module_typeBindings.MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_17B_Type_Pattern = MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_17B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_19A_Type_Pattern
class MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_19A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_19A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1290, 1)
    _Documentation = None
MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_19A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_19A_Type_Pattern._CF_pattern.addPattern(pattern='(:(ACRU|CHAR|COUN|DEAL|EXEC|ISDI|LADT|LEVY|LOCL|LOCO|MARG|OTHR|REGF|SETT|SHIP|SPCN|STAM|STEX|TRAN|TRAX|VATA|WITH|ANTO|COAX|ACCA|RSCH|RESU|OCMT)//(N)?(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})')
MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_19A_Type_Pattern._InitializeFacetMap(MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_19A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_19A_Type_Pattern', MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_19A_Type_Pattern)
_module_typeBindings.MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_19A_Type_Pattern = MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_19A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_98A_Type_Pattern
class MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_98A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_98A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1303, 1)
    _Documentation = None
MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_98A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_98A_Type_Pattern._CF_pattern.addPattern(pattern='(:(VALU)//[0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01]))')
MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_98A_Type_Pattern._InitializeFacetMap(MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_98A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_98A_Type_Pattern', MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_98A_Type_Pattern)
_module_typeBindings.MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_98A_Type_Pattern = MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_98A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_98C_Type_Pattern
class MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_98C_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_98C_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1316, 1)
    _Documentation = None
MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_98C_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_98C_Type_Pattern._CF_pattern.addPattern(pattern='(:(VALU)//[0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])(0[0-9]|[1][0-9]|2[1-3])([0-5][0-9])([0-5][0-9]))')
MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_98C_Type_Pattern._InitializeFacetMap(MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_98C_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_98C_Type_Pattern', MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_98C_Type_Pattern)
_module_typeBindings.MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_98C_Type_Pattern = MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_98C_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_92B_Type_Pattern
class MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_92B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_92B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1329, 1)
    _Documentation = None
MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_92B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_92B_Type_Pattern._CF_pattern.addPattern(pattern='(:(EXCH)//(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)/(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)/[0-9,(?0-9)]{1,15})')
MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_92B_Type_Pattern._InitializeFacetMap(MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_92B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_92B_Type_Pattern', MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_92B_Type_Pattern)
_module_typeBindings.MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_92B_Type_Pattern = MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_92B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceF_OtherParties_95C_Type_Pattern
class MT541_SequenceF_OtherParties_95C_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceF_OtherParties_95C_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1342, 1)
    _Documentation = None
MT541_SequenceF_OtherParties_95C_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceF_OtherParties_95C_Type_Pattern._CF_pattern.addPattern(pattern='(:(INVE)//[A-Z]{2})')
MT541_SequenceF_OtherParties_95C_Type_Pattern._InitializeFacetMap(MT541_SequenceF_OtherParties_95C_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceF_OtherParties_95C_Type_Pattern', MT541_SequenceF_OtherParties_95C_Type_Pattern)
_module_typeBindings.MT541_SequenceF_OtherParties_95C_Type_Pattern = MT541_SequenceF_OtherParties_95C_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceF_OtherParties_95L_Type_Pattern
class MT541_SequenceF_OtherParties_95L_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceF_OtherParties_95L_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1355, 1)
    _Documentation = None
MT541_SequenceF_OtherParties_95L_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceF_OtherParties_95L_Type_Pattern._CF_pattern.addPattern(pattern='(:(ALTE)//[A-Z0-9]{18}[0-9]{2})')
MT541_SequenceF_OtherParties_95L_Type_Pattern._InitializeFacetMap(MT541_SequenceF_OtherParties_95L_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceF_OtherParties_95L_Type_Pattern', MT541_SequenceF_OtherParties_95L_Type_Pattern)
_module_typeBindings.MT541_SequenceF_OtherParties_95L_Type_Pattern = MT541_SequenceF_OtherParties_95L_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceF_OtherParties_95P_Type_Pattern
class MT541_SequenceF_OtherParties_95P_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceF_OtherParties_95P_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1368, 1)
    _Documentation = None
MT541_SequenceF_OtherParties_95P_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceF_OtherParties_95P_Type_Pattern._CF_pattern.addPattern(pattern='(:(EXCH|MEOR|MERE|TRRE|INVE|VEND|TRAG|BRKR)//[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)')
MT541_SequenceF_OtherParties_95P_Type_Pattern._InitializeFacetMap(MT541_SequenceF_OtherParties_95P_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceF_OtherParties_95P_Type_Pattern', MT541_SequenceF_OtherParties_95P_Type_Pattern)
_module_typeBindings.MT541_SequenceF_OtherParties_95P_Type_Pattern = MT541_SequenceF_OtherParties_95P_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceF_OtherParties_95Q_Type_Pattern
class MT541_SequenceF_OtherParties_95Q_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceF_OtherParties_95Q_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1381, 1)
    _Documentation = None
MT541_SequenceF_OtherParties_95Q_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceF_OtherParties_95Q_Type_Pattern._CF_pattern.addPattern(pattern="(:(EXCH|MEOR|MERE|TRRE|INVE|VEND|TRAG|BRKR)//(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT541_SequenceF_OtherParties_95Q_Type_Pattern._InitializeFacetMap(MT541_SequenceF_OtherParties_95Q_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceF_OtherParties_95Q_Type_Pattern', MT541_SequenceF_OtherParties_95Q_Type_Pattern)
_module_typeBindings.MT541_SequenceF_OtherParties_95Q_Type_Pattern = MT541_SequenceF_OtherParties_95Q_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceF_OtherParties_95R_Type_Pattern
class MT541_SequenceF_OtherParties_95R_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceF_OtherParties_95R_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1394, 1)
    _Documentation = None
MT541_SequenceF_OtherParties_95R_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceF_OtherParties_95R_Type_Pattern._CF_pattern.addPattern(pattern="(:(EXCH|MEOR|MERE|TRRE|INVE|VEND|TRAG|BRKR)/[A-Z0-9]{1,8}/[^/]([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34}[^/])")
MT541_SequenceF_OtherParties_95R_Type_Pattern._InitializeFacetMap(MT541_SequenceF_OtherParties_95R_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceF_OtherParties_95R_Type_Pattern', MT541_SequenceF_OtherParties_95R_Type_Pattern)
_module_typeBindings.MT541_SequenceF_OtherParties_95R_Type_Pattern = MT541_SequenceF_OtherParties_95R_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceF_OtherParties_95S_Type_Pattern
class MT541_SequenceF_OtherParties_95S_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceF_OtherParties_95S_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1407, 1)
    _Documentation = None
MT541_SequenceF_OtherParties_95S_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceF_OtherParties_95S_Type_Pattern._CF_pattern.addPattern(pattern="(:(ALTE)/([A-Z0-9]{1,8})?/[A-Z0-9]{4}/[A-Z]{2}/[^/]([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,30}[^/])")
MT541_SequenceF_OtherParties_95S_Type_Pattern._InitializeFacetMap(MT541_SequenceF_OtherParties_95S_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceF_OtherParties_95S_Type_Pattern', MT541_SequenceF_OtherParties_95S_Type_Pattern)
_module_typeBindings.MT541_SequenceF_OtherParties_95S_Type_Pattern = MT541_SequenceF_OtherParties_95S_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceF_OtherParties_97A_Type_Pattern
class MT541_SequenceF_OtherParties_97A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceF_OtherParties_97A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1420, 1)
    _Documentation = None
MT541_SequenceF_OtherParties_97A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceF_OtherParties_97A_Type_Pattern._CF_pattern.addPattern(pattern="(:(SAFE)//([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35})")
MT541_SequenceF_OtherParties_97A_Type_Pattern._InitializeFacetMap(MT541_SequenceF_OtherParties_97A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceF_OtherParties_97A_Type_Pattern', MT541_SequenceF_OtherParties_97A_Type_Pattern)
_module_typeBindings.MT541_SequenceF_OtherParties_97A_Type_Pattern = MT541_SequenceF_OtherParties_97A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceF_OtherParties_70C_Type_Pattern
class MT541_SequenceF_OtherParties_70C_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceF_OtherParties_70C_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1433, 1)
    _Documentation = None
MT541_SequenceF_OtherParties_70C_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceF_OtherParties_70C_Type_Pattern._CF_pattern.addPattern(pattern="(:(PACO)//(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT541_SequenceF_OtherParties_70C_Type_Pattern._InitializeFacetMap(MT541_SequenceF_OtherParties_70C_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceF_OtherParties_70C_Type_Pattern', MT541_SequenceF_OtherParties_70C_Type_Pattern)
_module_typeBindings.MT541_SequenceF_OtherParties_70C_Type_Pattern = MT541_SequenceF_OtherParties_70C_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceF_OtherParties_70D_Type_Pattern
class MT541_SequenceF_OtherParties_70D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceF_OtherParties_70D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1446, 1)
    _Documentation = None
MT541_SequenceF_OtherParties_70D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceF_OtherParties_70D_Type_Pattern._CF_pattern.addPattern(pattern="(:(REGI)//(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,6})")
MT541_SequenceF_OtherParties_70D_Type_Pattern._InitializeFacetMap(MT541_SequenceF_OtherParties_70D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceF_OtherParties_70D_Type_Pattern', MT541_SequenceF_OtherParties_70D_Type_Pattern)
_module_typeBindings.MT541_SequenceF_OtherParties_70D_Type_Pattern = MT541_SequenceF_OtherParties_70D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceF_OtherParties_70E_Type_Pattern
class MT541_SequenceF_OtherParties_70E_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceF_OtherParties_70E_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1459, 1)
    _Documentation = None
MT541_SequenceF_OtherParties_70E_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceF_OtherParties_70E_Type_Pattern._CF_pattern.addPattern(pattern="(:(DECL)//(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,10})")
MT541_SequenceF_OtherParties_70E_Type_Pattern._InitializeFacetMap(MT541_SequenceF_OtherParties_70E_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceF_OtherParties_70E_Type_Pattern', MT541_SequenceF_OtherParties_70E_Type_Pattern)
_module_typeBindings.MT541_SequenceF_OtherParties_70E_Type_Pattern = MT541_SequenceF_OtherParties_70E_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT541_SequenceF_OtherParties_20C_Type_Pattern
class MT541_SequenceF_OtherParties_20C_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceF_OtherParties_20C_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1472, 1)
    _Documentation = None
MT541_SequenceF_OtherParties_20C_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT541_SequenceF_OtherParties_20C_Type_Pattern._CF_pattern.addPattern(pattern="(:(PROC)//[^/]([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,16}[^/])")
MT541_SequenceF_OtherParties_20C_Type_Pattern._InitializeFacetMap(MT541_SequenceF_OtherParties_20C_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceF_OtherParties_20C_Type_Pattern', MT541_SequenceF_OtherParties_20C_Type_Pattern)
_module_typeBindings.MT541_SequenceF_OtherParties_20C_Type_Pattern = MT541_SequenceF_OtherParties_20C_Type_Pattern

# Complex type {http://www.w3schools.com}MT541_SequenceA_GeneralInformation with content type ELEMENT_ONLY
class MT541_SequenceA_GeneralInformation (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceA_GeneralInformation with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceA_GeneralInformation')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1485, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}SendersMessageReference uses Python identifier SendersMessageReference
    __SendersMessageReference = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SendersMessageReference'), 'SendersMessageReference', '__httpwww_w3schools_com_MT541_SequenceA_GeneralInformation_httpwww_w3schools_comSendersMessageReference', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1487, 3), )

    
    SendersMessageReference = property(__SendersMessageReference.value, __SendersMessageReference.set, None, None)

    
    # Element {http://www.w3schools.com}FunctionOfMessage uses Python identifier FunctionOfMessage
    __FunctionOfMessage = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'FunctionOfMessage'), 'FunctionOfMessage', '__httpwww_w3schools_com_MT541_SequenceA_GeneralInformation_httpwww_w3schools_comFunctionOfMessage', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1488, 3), )

    
    FunctionOfMessage = property(__FunctionOfMessage.value, __FunctionOfMessage.set, None, None)

    
    # Element {http://www.w3schools.com}PreparationDateTime_A uses Python identifier PreparationDateTime_A
    __PreparationDateTime_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PreparationDateTime_A'), 'PreparationDateTime_A', '__httpwww_w3schools_com_MT541_SequenceA_GeneralInformation_httpwww_w3schools_comPreparationDateTime_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1490, 4), )

    
    PreparationDateTime_A = property(__PreparationDateTime_A.value, __PreparationDateTime_A.set, None, None)

    
    # Element {http://www.w3schools.com}PreparationDateTime_C uses Python identifier PreparationDateTime_C
    __PreparationDateTime_C = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PreparationDateTime_C'), 'PreparationDateTime_C', '__httpwww_w3schools_com_MT541_SequenceA_GeneralInformation_httpwww_w3schools_comPreparationDateTime_C', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1491, 4), )

    
    PreparationDateTime_C = property(__PreparationDateTime_C.value, __PreparationDateTime_C.set, None, None)

    
    # Element {http://www.w3schools.com}PreparationDateTime_E uses Python identifier PreparationDateTime_E
    __PreparationDateTime_E = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PreparationDateTime_E'), 'PreparationDateTime_E', '__httpwww_w3schools_com_MT541_SequenceA_GeneralInformation_httpwww_w3schools_comPreparationDateTime_E', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1492, 4), )

    
    PreparationDateTime_E = property(__PreparationDateTime_E.value, __PreparationDateTime_E.set, None, None)

    
    # Element {http://www.w3schools.com}NumberCount uses Python identifier NumberCount
    __NumberCount = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'NumberCount'), 'NumberCount', '__httpwww_w3schools_com_MT541_SequenceA_GeneralInformation_httpwww_w3schools_comNumberCount', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1494, 3), )

    
    NumberCount = property(__NumberCount.value, __NumberCount.set, None, None)

    
    # Element {http://www.w3schools.com}SubSequenceA1_Linkages uses Python identifier SubSequenceA1_Linkages
    __SubSequenceA1_Linkages = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SubSequenceA1_Linkages'), 'SubSequenceA1_Linkages', '__httpwww_w3schools_com_MT541_SequenceA_GeneralInformation_httpwww_w3schools_comSubSequenceA1_Linkages', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1495, 3), )

    
    SubSequenceA1_Linkages = property(__SubSequenceA1_Linkages.value, __SubSequenceA1_Linkages.set, None, None)

    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceA_GeneralInformation_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='16R')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1497, 2)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1497, 2)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceA_GeneralInformation_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1498, 2)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1498, 2)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    
    # Attribute formatTag uses Python identifier formatTag
    __formatTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'formatTag'), 'formatTag', '__httpwww_w3schools_com_MT541_SequenceA_GeneralInformation_formatTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='GENL')
    __formatTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1499, 2)
    __formatTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1499, 2)
    
    formatTag = property(__formatTag.value, __formatTag.set, None, None)

    _ElementMap.update({
        __SendersMessageReference.name() : __SendersMessageReference,
        __FunctionOfMessage.name() : __FunctionOfMessage,
        __PreparationDateTime_A.name() : __PreparationDateTime_A,
        __PreparationDateTime_C.name() : __PreparationDateTime_C,
        __PreparationDateTime_E.name() : __PreparationDateTime_E,
        __NumberCount.name() : __NumberCount,
        __SubSequenceA1_Linkages.name() : __SubSequenceA1_Linkages
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory,
        __formatTag.name() : __formatTag
    })
_module_typeBindings.MT541_SequenceA_GeneralInformation = MT541_SequenceA_GeneralInformation
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceA_GeneralInformation', MT541_SequenceA_GeneralInformation)


# Complex type {http://www.w3schools.com}MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages with content type ELEMENT_ONLY
class MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1501, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}LinkageTypeIndicator uses Python identifier LinkageTypeIndicator
    __LinkageTypeIndicator = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'LinkageTypeIndicator'), 'LinkageTypeIndicator', '__httpwww_w3schools_com_MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_httpwww_w3schools_comLinkageTypeIndicator', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1503, 3), )

    
    LinkageTypeIndicator = property(__LinkageTypeIndicator.value, __LinkageTypeIndicator.set, None, None)

    
    # Element {http://www.w3schools.com}LinkedMessage_A uses Python identifier LinkedMessage_A
    __LinkedMessage_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'LinkedMessage_A'), 'LinkedMessage_A', '__httpwww_w3schools_com_MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_httpwww_w3schools_comLinkedMessage_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1505, 4), )

    
    LinkedMessage_A = property(__LinkedMessage_A.value, __LinkedMessage_A.set, None, None)

    
    # Element {http://www.w3schools.com}LinkedMessage_B uses Python identifier LinkedMessage_B
    __LinkedMessage_B = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'LinkedMessage_B'), 'LinkedMessage_B', '__httpwww_w3schools_com_MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_httpwww_w3schools_comLinkedMessage_B', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1506, 4), )

    
    LinkedMessage_B = property(__LinkedMessage_B.value, __LinkedMessage_B.set, None, None)

    
    # Element {http://www.w3schools.com}Reference_C uses Python identifier Reference_C
    __Reference_C = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Reference_C'), 'Reference_C', '__httpwww_w3schools_com_MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_httpwww_w3schools_comReference_C', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1509, 4), )

    
    Reference_C = property(__Reference_C.value, __Reference_C.set, None, None)

    
    # Element {http://www.w3schools.com}Reference_U uses Python identifier Reference_U
    __Reference_U = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Reference_U'), 'Reference_U', '__httpwww_w3schools_com_MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_httpwww_w3schools_comReference_U', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1510, 4), )

    
    Reference_U = property(__Reference_U.value, __Reference_U.set, None, None)

    
    # Element {http://www.w3schools.com}QuantityOfFinancialInstrument uses Python identifier QuantityOfFinancialInstrument
    __QuantityOfFinancialInstrument = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'QuantityOfFinancialInstrument'), 'QuantityOfFinancialInstrument', '__httpwww_w3schools_com_MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_httpwww_w3schools_comQuantityOfFinancialInstrument', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1512, 3), )

    
    QuantityOfFinancialInstrument = property(__QuantityOfFinancialInstrument.value, __QuantityOfFinancialInstrument.set, None, None)

    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='16R')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1514, 2)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1514, 2)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1515, 2)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1515, 2)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    
    # Attribute formatTag uses Python identifier formatTag
    __formatTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'formatTag'), 'formatTag', '__httpwww_w3schools_com_MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_formatTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='LINK')
    __formatTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1516, 2)
    __formatTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1516, 2)
    
    formatTag = property(__formatTag.value, __formatTag.set, None, None)

    _ElementMap.update({
        __LinkageTypeIndicator.name() : __LinkageTypeIndicator,
        __LinkedMessage_A.name() : __LinkedMessage_A,
        __LinkedMessage_B.name() : __LinkedMessage_B,
        __Reference_C.name() : __Reference_C,
        __Reference_U.name() : __Reference_U,
        __QuantityOfFinancialInstrument.name() : __QuantityOfFinancialInstrument
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory,
        __formatTag.name() : __formatTag
    })
_module_typeBindings.MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages = MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages', MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages)


# Complex type {http://www.w3schools.com}MT541_SequenceB_TradeDetails with content type ELEMENT_ONLY
class MT541_SequenceB_TradeDetails (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceB_TradeDetails with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceB_TradeDetails')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1518, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}Place_B uses Python identifier Place_B
    __Place_B = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Place_B'), 'Place_B', '__httpwww_w3schools_com_MT541_SequenceB_TradeDetails_httpwww_w3schools_comPlace_B', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1521, 4), )

    
    Place_B = property(__Place_B.value, __Place_B.set, None, None)

    
    # Element {http://www.w3schools.com}Place_H uses Python identifier Place_H
    __Place_H = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Place_H'), 'Place_H', '__httpwww_w3schools_com_MT541_SequenceB_TradeDetails_httpwww_w3schools_comPlace_H', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1522, 4), )

    
    Place_H = property(__Place_H.value, __Place_H.set, None, None)

    
    # Element {http://www.w3schools.com}Place_L uses Python identifier Place_L
    __Place_L = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Place_L'), 'Place_L', '__httpwww_w3schools_com_MT541_SequenceB_TradeDetails_httpwww_w3schools_comPlace_L', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1523, 4), )

    
    Place_L = property(__Place_L.value, __Place_L.set, None, None)

    
    # Element {http://www.w3schools.com}DateTime_A uses Python identifier DateTime_A
    __DateTime_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'DateTime_A'), 'DateTime_A', '__httpwww_w3schools_com_MT541_SequenceB_TradeDetails_httpwww_w3schools_comDateTime_A', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1526, 4), )

    
    DateTime_A = property(__DateTime_A.value, __DateTime_A.set, None, None)

    
    # Element {http://www.w3schools.com}DateTime_B uses Python identifier DateTime_B
    __DateTime_B = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'DateTime_B'), 'DateTime_B', '__httpwww_w3schools_com_MT541_SequenceB_TradeDetails_httpwww_w3schools_comDateTime_B', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1527, 4), )

    
    DateTime_B = property(__DateTime_B.value, __DateTime_B.set, None, None)

    
    # Element {http://www.w3schools.com}DateTime_C uses Python identifier DateTime_C
    __DateTime_C = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'DateTime_C'), 'DateTime_C', '__httpwww_w3schools_com_MT541_SequenceB_TradeDetails_httpwww_w3schools_comDateTime_C', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1528, 4), )

    
    DateTime_C = property(__DateTime_C.value, __DateTime_C.set, None, None)

    
    # Element {http://www.w3schools.com}DateTime_E uses Python identifier DateTime_E
    __DateTime_E = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'DateTime_E'), 'DateTime_E', '__httpwww_w3schools_com_MT541_SequenceB_TradeDetails_httpwww_w3schools_comDateTime_E', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1529, 4), )

    
    DateTime_E = property(__DateTime_E.value, __DateTime_E.set, None, None)

    
    # Element {http://www.w3schools.com}DealPrice_A uses Python identifier DealPrice_A
    __DealPrice_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'DealPrice_A'), 'DealPrice_A', '__httpwww_w3schools_com_MT541_SequenceB_TradeDetails_httpwww_w3schools_comDealPrice_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1532, 4), )

    
    DealPrice_A = property(__DealPrice_A.value, __DealPrice_A.set, None, None)

    
    # Element {http://www.w3schools.com}DealPrice_B uses Python identifier DealPrice_B
    __DealPrice_B = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'DealPrice_B'), 'DealPrice_B', '__httpwww_w3schools_com_MT541_SequenceB_TradeDetails_httpwww_w3schools_comDealPrice_B', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1533, 4), )

    
    DealPrice_B = property(__DealPrice_B.value, __DealPrice_B.set, None, None)

    
    # Element {http://www.w3schools.com}NumberOfDaysAccrued uses Python identifier NumberOfDaysAccrued
    __NumberOfDaysAccrued = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'NumberOfDaysAccrued'), 'NumberOfDaysAccrued', '__httpwww_w3schools_com_MT541_SequenceB_TradeDetails_httpwww_w3schools_comNumberOfDaysAccrued', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1535, 3), )

    
    NumberOfDaysAccrued = property(__NumberOfDaysAccrued.value, __NumberOfDaysAccrued.set, None, None)

    
    # Element {http://www.w3schools.com}IdentificationOfFinancialInstrument uses Python identifier IdentificationOfFinancialInstrument
    __IdentificationOfFinancialInstrument = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'IdentificationOfFinancialInstrument'), 'IdentificationOfFinancialInstrument', '__httpwww_w3schools_com_MT541_SequenceB_TradeDetails_httpwww_w3schools_comIdentificationOfFinancialInstrument', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1536, 3), )

    
    IdentificationOfFinancialInstrument = property(__IdentificationOfFinancialInstrument.value, __IdentificationOfFinancialInstrument.set, None, None)

    
    # Element {http://www.w3schools.com}SubSequenceB1_FinancialInstrumentAttributes uses Python identifier SubSequenceB1_FinancialInstrumentAttributes
    __SubSequenceB1_FinancialInstrumentAttributes = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SubSequenceB1_FinancialInstrumentAttributes'), 'SubSequenceB1_FinancialInstrumentAttributes', '__httpwww_w3schools_com_MT541_SequenceB_TradeDetails_httpwww_w3schools_comSubSequenceB1_FinancialInstrumentAttributes', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1537, 3), )

    
    SubSequenceB1_FinancialInstrumentAttributes = property(__SubSequenceB1_FinancialInstrumentAttributes.value, __SubSequenceB1_FinancialInstrumentAttributes.set, None, None)

    
    # Element {http://www.w3schools.com}Indicator uses Python identifier Indicator
    __Indicator = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Indicator'), 'Indicator', '__httpwww_w3schools_com_MT541_SequenceB_TradeDetails_httpwww_w3schools_comIndicator', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1538, 3), )

    
    Indicator = property(__Indicator.value, __Indicator.set, None, None)

    
    # Element {http://www.w3schools.com}CurrencyToSell uses Python identifier CurrencyToSell
    __CurrencyToSell = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'CurrencyToSell'), 'CurrencyToSell', '__httpwww_w3schools_com_MT541_SequenceB_TradeDetails_httpwww_w3schools_comCurrencyToSell', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1539, 3), )

    
    CurrencyToSell = property(__CurrencyToSell.value, __CurrencyToSell.set, None, None)

    
    # Element {http://www.w3schools.com}Status uses Python identifier Status
    __Status = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Status'), 'Status', '__httpwww_w3schools_com_MT541_SequenceB_TradeDetails_httpwww_w3schools_comStatus', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1540, 3), )

    
    Status = property(__Status.value, __Status.set, None, None)

    
    # Element {http://www.w3schools.com}Narrative uses Python identifier Narrative
    __Narrative = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Narrative'), 'Narrative', '__httpwww_w3schools_com_MT541_SequenceB_TradeDetails_httpwww_w3schools_comNarrative', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1541, 3), )

    
    Narrative = property(__Narrative.value, __Narrative.set, None, None)

    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceB_TradeDetails_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='16R')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1543, 2)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1543, 2)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceB_TradeDetails_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1544, 2)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1544, 2)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    
    # Attribute formatTag uses Python identifier formatTag
    __formatTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'formatTag'), 'formatTag', '__httpwww_w3schools_com_MT541_SequenceB_TradeDetails_formatTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='TRADDET')
    __formatTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1545, 2)
    __formatTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1545, 2)
    
    formatTag = property(__formatTag.value, __formatTag.set, None, None)

    _ElementMap.update({
        __Place_B.name() : __Place_B,
        __Place_H.name() : __Place_H,
        __Place_L.name() : __Place_L,
        __DateTime_A.name() : __DateTime_A,
        __DateTime_B.name() : __DateTime_B,
        __DateTime_C.name() : __DateTime_C,
        __DateTime_E.name() : __DateTime_E,
        __DealPrice_A.name() : __DealPrice_A,
        __DealPrice_B.name() : __DealPrice_B,
        __NumberOfDaysAccrued.name() : __NumberOfDaysAccrued,
        __IdentificationOfFinancialInstrument.name() : __IdentificationOfFinancialInstrument,
        __SubSequenceB1_FinancialInstrumentAttributes.name() : __SubSequenceB1_FinancialInstrumentAttributes,
        __Indicator.name() : __Indicator,
        __CurrencyToSell.name() : __CurrencyToSell,
        __Status.name() : __Status,
        __Narrative.name() : __Narrative
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory,
        __formatTag.name() : __formatTag
    })
_module_typeBindings.MT541_SequenceB_TradeDetails = MT541_SequenceB_TradeDetails
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceB_TradeDetails', MT541_SequenceB_TradeDetails)


# Complex type {http://www.w3schools.com}MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes with content type ELEMENT_ONLY
class MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1547, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}PlaceOfListing uses Python identifier PlaceOfListing
    __PlaceOfListing = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PlaceOfListing'), 'PlaceOfListing', '__httpwww_w3schools_com_MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_httpwww_w3schools_comPlaceOfListing', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1549, 3), )

    
    PlaceOfListing = property(__PlaceOfListing.value, __PlaceOfListing.set, None, None)

    
    # Element {http://www.w3schools.com}Indicator uses Python identifier Indicator
    __Indicator = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Indicator'), 'Indicator', '__httpwww_w3schools_com_MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_httpwww_w3schools_comIndicator', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1550, 3), )

    
    Indicator = property(__Indicator.value, __Indicator.set, None, None)

    
    # Element {http://www.w3schools.com}TypeOfFinancialInstrument_A uses Python identifier TypeOfFinancialInstrument_A
    __TypeOfFinancialInstrument_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'TypeOfFinancialInstrument_A'), 'TypeOfFinancialInstrument_A', '__httpwww_w3schools_com_MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_httpwww_w3schools_comTypeOfFinancialInstrument_A', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1552, 4), )

    
    TypeOfFinancialInstrument_A = property(__TypeOfFinancialInstrument_A.value, __TypeOfFinancialInstrument_A.set, None, None)

    
    # Element {http://www.w3schools.com}TypeOfFinancialInstrument_B uses Python identifier TypeOfFinancialInstrument_B
    __TypeOfFinancialInstrument_B = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'TypeOfFinancialInstrument_B'), 'TypeOfFinancialInstrument_B', '__httpwww_w3schools_com_MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_httpwww_w3schools_comTypeOfFinancialInstrument_B', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1553, 4), )

    
    TypeOfFinancialInstrument_B = property(__TypeOfFinancialInstrument_B.value, __TypeOfFinancialInstrument_B.set, None, None)

    
    # Element {http://www.w3schools.com}TypeOfFinancialInstrument_C uses Python identifier TypeOfFinancialInstrument_C
    __TypeOfFinancialInstrument_C = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'TypeOfFinancialInstrument_C'), 'TypeOfFinancialInstrument_C', '__httpwww_w3schools_com_MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_httpwww_w3schools_comTypeOfFinancialInstrument_C', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1554, 4), )

    
    TypeOfFinancialInstrument_C = property(__TypeOfFinancialInstrument_C.value, __TypeOfFinancialInstrument_C.set, None, None)

    
    # Element {http://www.w3schools.com}CurrencyOfDenomination uses Python identifier CurrencyOfDenomination
    __CurrencyOfDenomination = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'CurrencyOfDenomination'), 'CurrencyOfDenomination', '__httpwww_w3schools_com_MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_httpwww_w3schools_comCurrencyOfDenomination', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1556, 3), )

    
    CurrencyOfDenomination = property(__CurrencyOfDenomination.value, __CurrencyOfDenomination.set, None, None)

    
    # Element {http://www.w3schools.com}Date uses Python identifier Date
    __Date = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Date'), 'Date', '__httpwww_w3schools_com_MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_httpwww_w3schools_comDate', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1557, 3), )

    
    Date = property(__Date.value, __Date.set, None, None)

    
    # Element {http://www.w3schools.com}Rate uses Python identifier Rate
    __Rate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Rate'), 'Rate', '__httpwww_w3schools_com_MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_httpwww_w3schools_comRate', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1558, 3), )

    
    Rate = property(__Rate.value, __Rate.set, None, None)

    
    # Element {http://www.w3schools.com}NumberIdentification_A uses Python identifier NumberIdentification_A
    __NumberIdentification_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'NumberIdentification_A'), 'NumberIdentification_A', '__httpwww_w3schools_com_MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_httpwww_w3schools_comNumberIdentification_A', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1560, 4), )

    
    NumberIdentification_A = property(__NumberIdentification_A.value, __NumberIdentification_A.set, None, None)

    
    # Element {http://www.w3schools.com}NumberIdentification_B uses Python identifier NumberIdentification_B
    __NumberIdentification_B = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'NumberIdentification_B'), 'NumberIdentification_B', '__httpwww_w3schools_com_MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_httpwww_w3schools_comNumberIdentification_B', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1561, 4), )

    
    NumberIdentification_B = property(__NumberIdentification_B.value, __NumberIdentification_B.set, None, None)

    
    # Element {http://www.w3schools.com}Flag uses Python identifier Flag
    __Flag = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Flag'), 'Flag', '__httpwww_w3schools_com_MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_httpwww_w3schools_comFlag', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1563, 3), )

    
    Flag = property(__Flag.value, __Flag.set, None, None)

    
    # Element {http://www.w3schools.com}Price_A uses Python identifier Price_A
    __Price_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Price_A'), 'Price_A', '__httpwww_w3schools_com_MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_httpwww_w3schools_comPrice_A', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1565, 4), )

    
    Price_A = property(__Price_A.value, __Price_A.set, None, None)

    
    # Element {http://www.w3schools.com}Price_B uses Python identifier Price_B
    __Price_B = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Price_B'), 'Price_B', '__httpwww_w3schools_com_MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_httpwww_w3schools_comPrice_B', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1566, 4), )

    
    Price_B = property(__Price_B.value, __Price_B.set, None, None)

    
    # Element {http://www.w3schools.com}QuantityOfFinancialInstrument uses Python identifier QuantityOfFinancialInstrument
    __QuantityOfFinancialInstrument = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'QuantityOfFinancialInstrument'), 'QuantityOfFinancialInstrument', '__httpwww_w3schools_com_MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_httpwww_w3schools_comQuantityOfFinancialInstrument', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1568, 3), )

    
    QuantityOfFinancialInstrument = property(__QuantityOfFinancialInstrument.value, __QuantityOfFinancialInstrument.set, None, None)

    
    # Element {http://www.w3schools.com}IdentificationOfFinancialInstrument uses Python identifier IdentificationOfFinancialInstrument
    __IdentificationOfFinancialInstrument = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'IdentificationOfFinancialInstrument'), 'IdentificationOfFinancialInstrument', '__httpwww_w3schools_com_MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_httpwww_w3schools_comIdentificationOfFinancialInstrument', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1569, 3), )

    
    IdentificationOfFinancialInstrument = property(__IdentificationOfFinancialInstrument.value, __IdentificationOfFinancialInstrument.set, None, None)

    
    # Element {http://www.w3schools.com}FinancialInstrumentAttributeNarrative uses Python identifier FinancialInstrumentAttributeNarrative
    __FinancialInstrumentAttributeNarrative = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'FinancialInstrumentAttributeNarrative'), 'FinancialInstrumentAttributeNarrative', '__httpwww_w3schools_com_MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_httpwww_w3schools_comFinancialInstrumentAttributeNarrative', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1570, 3), )

    
    FinancialInstrumentAttributeNarrative = property(__FinancialInstrumentAttributeNarrative.value, __FinancialInstrumentAttributeNarrative.set, None, None)

    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='16R')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1572, 2)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1572, 2)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1573, 2)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1573, 2)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    
    # Attribute formatTag uses Python identifier formatTag
    __formatTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'formatTag'), 'formatTag', '__httpwww_w3schools_com_MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_formatTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='FIA')
    __formatTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1574, 2)
    __formatTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1574, 2)
    
    formatTag = property(__formatTag.value, __formatTag.set, None, None)

    _ElementMap.update({
        __PlaceOfListing.name() : __PlaceOfListing,
        __Indicator.name() : __Indicator,
        __TypeOfFinancialInstrument_A.name() : __TypeOfFinancialInstrument_A,
        __TypeOfFinancialInstrument_B.name() : __TypeOfFinancialInstrument_B,
        __TypeOfFinancialInstrument_C.name() : __TypeOfFinancialInstrument_C,
        __CurrencyOfDenomination.name() : __CurrencyOfDenomination,
        __Date.name() : __Date,
        __Rate.name() : __Rate,
        __NumberIdentification_A.name() : __NumberIdentification_A,
        __NumberIdentification_B.name() : __NumberIdentification_B,
        __Flag.name() : __Flag,
        __Price_A.name() : __Price_A,
        __Price_B.name() : __Price_B,
        __QuantityOfFinancialInstrument.name() : __QuantityOfFinancialInstrument,
        __IdentificationOfFinancialInstrument.name() : __IdentificationOfFinancialInstrument,
        __FinancialInstrumentAttributeNarrative.name() : __FinancialInstrumentAttributeNarrative
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory,
        __formatTag.name() : __formatTag
    })
_module_typeBindings.MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes = MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes', MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes)


# Complex type {http://www.w3schools.com}MT541_SequenceC_FinancialInstrumentAccount with content type ELEMENT_ONLY
class MT541_SequenceC_FinancialInstrumentAccount (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceC_FinancialInstrumentAccount with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceC_FinancialInstrumentAccount')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1576, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}QuantityOfFinancialInstrumentToBeSettled uses Python identifier QuantityOfFinancialInstrumentToBeSettled
    __QuantityOfFinancialInstrumentToBeSettled = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'QuantityOfFinancialInstrumentToBeSettled'), 'QuantityOfFinancialInstrumentToBeSettled', '__httpwww_w3schools_com_MT541_SequenceC_FinancialInstrumentAccount_httpwww_w3schools_comQuantityOfFinancialInstrumentToBeSettled', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1578, 3), )

    
    QuantityOfFinancialInstrumentToBeSettled = property(__QuantityOfFinancialInstrumentToBeSettled.value, __QuantityOfFinancialInstrumentToBeSettled.set, None, None)

    
    # Element {http://www.w3schools.com}DenominationChoice uses Python identifier DenominationChoice
    __DenominationChoice = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'DenominationChoice'), 'DenominationChoice', '__httpwww_w3schools_com_MT541_SequenceC_FinancialInstrumentAccount_httpwww_w3schools_comDenominationChoice', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1579, 3), )

    
    DenominationChoice = property(__DenominationChoice.value, __DenominationChoice.set, None, None)

    
    # Element {http://www.w3schools.com}CertificateNumber uses Python identifier CertificateNumber
    __CertificateNumber = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'CertificateNumber'), 'CertificateNumber', '__httpwww_w3schools_com_MT541_SequenceC_FinancialInstrumentAccount_httpwww_w3schools_comCertificateNumber', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1580, 3), )

    
    CertificateNumber = property(__CertificateNumber.value, __CertificateNumber.set, None, None)

    
    # Element {http://www.w3schools.com}Party_L uses Python identifier Party_L
    __Party_L = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Party_L'), 'Party_L', '__httpwww_w3schools_com_MT541_SequenceC_FinancialInstrumentAccount_httpwww_w3schools_comParty_L', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1582, 4), )

    
    Party_L = property(__Party_L.value, __Party_L.set, None, None)

    
    # Element {http://www.w3schools.com}Party_P uses Python identifier Party_P
    __Party_P = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Party_P'), 'Party_P', '__httpwww_w3schools_com_MT541_SequenceC_FinancialInstrumentAccount_httpwww_w3schools_comParty_P', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1583, 4), )

    
    Party_P = property(__Party_P.value, __Party_P.set, None, None)

    
    # Element {http://www.w3schools.com}Party_R uses Python identifier Party_R
    __Party_R = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Party_R'), 'Party_R', '__httpwww_w3schools_com_MT541_SequenceC_FinancialInstrumentAccount_httpwww_w3schools_comParty_R', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1584, 4), )

    
    Party_R = property(__Party_R.value, __Party_R.set, None, None)

    
    # Element {http://www.w3schools.com}Account_A uses Python identifier Account_A
    __Account_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Account_A'), 'Account_A', '__httpwww_w3schools_com_MT541_SequenceC_FinancialInstrumentAccount_httpwww_w3schools_comAccount_A', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1587, 4), )

    
    Account_A = property(__Account_A.value, __Account_A.set, None, None)

    
    # Element {http://www.w3schools.com}Account_B uses Python identifier Account_B
    __Account_B = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Account_B'), 'Account_B', '__httpwww_w3schools_com_MT541_SequenceC_FinancialInstrumentAccount_httpwww_w3schools_comAccount_B', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1588, 4), )

    
    Account_B = property(__Account_B.value, __Account_B.set, None, None)

    
    # Element {http://www.w3schools.com}Account_E uses Python identifier Account_E
    __Account_E = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Account_E'), 'Account_E', '__httpwww_w3schools_com_MT541_SequenceC_FinancialInstrumentAccount_httpwww_w3schools_comAccount_E', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1589, 4), )

    
    Account_E = property(__Account_E.value, __Account_E.set, None, None)

    
    # Element {http://www.w3schools.com}PlaceOfSafekeeping_B uses Python identifier PlaceOfSafekeeping_B
    __PlaceOfSafekeeping_B = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PlaceOfSafekeeping_B'), 'PlaceOfSafekeeping_B', '__httpwww_w3schools_com_MT541_SequenceC_FinancialInstrumentAccount_httpwww_w3schools_comPlaceOfSafekeeping_B', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1592, 4), )

    
    PlaceOfSafekeeping_B = property(__PlaceOfSafekeeping_B.value, __PlaceOfSafekeeping_B.set, None, None)

    
    # Element {http://www.w3schools.com}PlaceOfSafekeeping_C uses Python identifier PlaceOfSafekeeping_C
    __PlaceOfSafekeeping_C = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PlaceOfSafekeeping_C'), 'PlaceOfSafekeeping_C', '__httpwww_w3schools_com_MT541_SequenceC_FinancialInstrumentAccount_httpwww_w3schools_comPlaceOfSafekeeping_C', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1593, 4), )

    
    PlaceOfSafekeeping_C = property(__PlaceOfSafekeeping_C.value, __PlaceOfSafekeeping_C.set, None, None)

    
    # Element {http://www.w3schools.com}PlaceOfSafekeeping_F uses Python identifier PlaceOfSafekeeping_F
    __PlaceOfSafekeeping_F = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PlaceOfSafekeeping_F'), 'PlaceOfSafekeeping_F', '__httpwww_w3schools_com_MT541_SequenceC_FinancialInstrumentAccount_httpwww_w3schools_comPlaceOfSafekeeping_F', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1594, 4), )

    
    PlaceOfSafekeeping_F = property(__PlaceOfSafekeeping_F.value, __PlaceOfSafekeeping_F.set, None, None)

    
    # Element {http://www.w3schools.com}PlaceOfSafekeeping_L uses Python identifier PlaceOfSafekeeping_L
    __PlaceOfSafekeeping_L = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PlaceOfSafekeeping_L'), 'PlaceOfSafekeeping_L', '__httpwww_w3schools_com_MT541_SequenceC_FinancialInstrumentAccount_httpwww_w3schools_comPlaceOfSafekeeping_L', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1595, 4), )

    
    PlaceOfSafekeeping_L = property(__PlaceOfSafekeeping_L.value, __PlaceOfSafekeeping_L.set, None, None)

    
    # Element {http://www.w3schools.com}SubSequenceC1_QuantityBreakdown uses Python identifier SubSequenceC1_QuantityBreakdown
    __SubSequenceC1_QuantityBreakdown = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SubSequenceC1_QuantityBreakdown'), 'SubSequenceC1_QuantityBreakdown', '__httpwww_w3schools_com_MT541_SequenceC_FinancialInstrumentAccount_httpwww_w3schools_comSubSequenceC1_QuantityBreakdown', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1597, 3), )

    
    SubSequenceC1_QuantityBreakdown = property(__SubSequenceC1_QuantityBreakdown.value, __SubSequenceC1_QuantityBreakdown.set, None, None)

    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceC_FinancialInstrumentAccount_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='16R')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1599, 2)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1599, 2)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceC_FinancialInstrumentAccount_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1600, 2)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1600, 2)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    
    # Attribute formatTag uses Python identifier formatTag
    __formatTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'formatTag'), 'formatTag', '__httpwww_w3schools_com_MT541_SequenceC_FinancialInstrumentAccount_formatTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='FIAC')
    __formatTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1601, 2)
    __formatTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1601, 2)
    
    formatTag = property(__formatTag.value, __formatTag.set, None, None)

    _ElementMap.update({
        __QuantityOfFinancialInstrumentToBeSettled.name() : __QuantityOfFinancialInstrumentToBeSettled,
        __DenominationChoice.name() : __DenominationChoice,
        __CertificateNumber.name() : __CertificateNumber,
        __Party_L.name() : __Party_L,
        __Party_P.name() : __Party_P,
        __Party_R.name() : __Party_R,
        __Account_A.name() : __Account_A,
        __Account_B.name() : __Account_B,
        __Account_E.name() : __Account_E,
        __PlaceOfSafekeeping_B.name() : __PlaceOfSafekeeping_B,
        __PlaceOfSafekeeping_C.name() : __PlaceOfSafekeeping_C,
        __PlaceOfSafekeeping_F.name() : __PlaceOfSafekeeping_F,
        __PlaceOfSafekeeping_L.name() : __PlaceOfSafekeeping_L,
        __SubSequenceC1_QuantityBreakdown.name() : __SubSequenceC1_QuantityBreakdown
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory,
        __formatTag.name() : __formatTag
    })
_module_typeBindings.MT541_SequenceC_FinancialInstrumentAccount = MT541_SequenceC_FinancialInstrumentAccount
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceC_FinancialInstrumentAccount', MT541_SequenceC_FinancialInstrumentAccount)


# Complex type {http://www.w3schools.com}MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown with content type ELEMENT_ONLY
class MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1603, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}LotNumber uses Python identifier LotNumber
    __LotNumber = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'LotNumber'), 'LotNumber', '__httpwww_w3schools_com_MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_httpwww_w3schools_comLotNumber', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1605, 3), )

    
    LotNumber = property(__LotNumber.value, __LotNumber.set, None, None)

    
    # Element {http://www.w3schools.com}QuantityOfFinancialInstrumentInTheLot uses Python identifier QuantityOfFinancialInstrumentInTheLot
    __QuantityOfFinancialInstrumentInTheLot = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'QuantityOfFinancialInstrumentInTheLot'), 'QuantityOfFinancialInstrumentInTheLot', '__httpwww_w3schools_com_MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_httpwww_w3schools_comQuantityOfFinancialInstrumentInTheLot', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1606, 3), )

    
    QuantityOfFinancialInstrumentInTheLot = property(__QuantityOfFinancialInstrumentInTheLot.value, __QuantityOfFinancialInstrumentInTheLot.set, None, None)

    
    # Element {http://www.w3schools.com}LotDateTime_A uses Python identifier LotDateTime_A
    __LotDateTime_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'LotDateTime_A'), 'LotDateTime_A', '__httpwww_w3schools_com_MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_httpwww_w3schools_comLotDateTime_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1608, 4), )

    
    LotDateTime_A = property(__LotDateTime_A.value, __LotDateTime_A.set, None, None)

    
    # Element {http://www.w3schools.com}LotDateTime_C uses Python identifier LotDateTime_C
    __LotDateTime_C = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'LotDateTime_C'), 'LotDateTime_C', '__httpwww_w3schools_com_MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_httpwww_w3schools_comLotDateTime_C', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1609, 4), )

    
    LotDateTime_C = property(__LotDateTime_C.value, __LotDateTime_C.set, None, None)

    
    # Element {http://www.w3schools.com}LotDateTime_E uses Python identifier LotDateTime_E
    __LotDateTime_E = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'LotDateTime_E'), 'LotDateTime_E', '__httpwww_w3schools_com_MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_httpwww_w3schools_comLotDateTime_E', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1610, 4), )

    
    LotDateTime_E = property(__LotDateTime_E.value, __LotDateTime_E.set, None, None)

    
    # Element {http://www.w3schools.com}BookLotPrice_A uses Python identifier BookLotPrice_A
    __BookLotPrice_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'BookLotPrice_A'), 'BookLotPrice_A', '__httpwww_w3schools_com_MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_httpwww_w3schools_comBookLotPrice_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1613, 4), )

    
    BookLotPrice_A = property(__BookLotPrice_A.value, __BookLotPrice_A.set, None, None)

    
    # Element {http://www.w3schools.com}BookLotPrice_B uses Python identifier BookLotPrice_B
    __BookLotPrice_B = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'BookLotPrice_B'), 'BookLotPrice_B', '__httpwww_w3schools_com_MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_httpwww_w3schools_comBookLotPrice_B', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1614, 4), )

    
    BookLotPrice_B = property(__BookLotPrice_B.value, __BookLotPrice_B.set, None, None)

    
    # Element {http://www.w3schools.com}TypeOfPriceIndicator uses Python identifier TypeOfPriceIndicator
    __TypeOfPriceIndicator = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'TypeOfPriceIndicator'), 'TypeOfPriceIndicator', '__httpwww_w3schools_com_MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_httpwww_w3schools_comTypeOfPriceIndicator', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1616, 3), )

    
    TypeOfPriceIndicator = property(__TypeOfPriceIndicator.value, __TypeOfPriceIndicator.set, None, None)

    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='16R')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1618, 2)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1618, 2)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1619, 2)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1619, 2)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    
    # Attribute formatTag uses Python identifier formatTag
    __formatTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'formatTag'), 'formatTag', '__httpwww_w3schools_com_MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_formatTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='BREAK')
    __formatTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1620, 2)
    __formatTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1620, 2)
    
    formatTag = property(__formatTag.value, __formatTag.set, None, None)

    _ElementMap.update({
        __LotNumber.name() : __LotNumber,
        __QuantityOfFinancialInstrumentInTheLot.name() : __QuantityOfFinancialInstrumentInTheLot,
        __LotDateTime_A.name() : __LotDateTime_A,
        __LotDateTime_C.name() : __LotDateTime_C,
        __LotDateTime_E.name() : __LotDateTime_E,
        __BookLotPrice_A.name() : __BookLotPrice_A,
        __BookLotPrice_B.name() : __BookLotPrice_B,
        __TypeOfPriceIndicator.name() : __TypeOfPriceIndicator
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory,
        __formatTag.name() : __formatTag
    })
_module_typeBindings.MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown = MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown', MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown)


# Complex type {http://www.w3schools.com}MT541_SequenceD_TwoLegTransactionDetails with content type ELEMENT_ONLY
class MT541_SequenceD_TwoLegTransactionDetails (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceD_TwoLegTransactionDetails with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceD_TwoLegTransactionDetails')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1622, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}DateTime_A uses Python identifier DateTime_A
    __DateTime_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'DateTime_A'), 'DateTime_A', '__httpwww_w3schools_com_MT541_SequenceD_TwoLegTransactionDetails_httpwww_w3schools_comDateTime_A', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1625, 4), )

    
    DateTime_A = property(__DateTime_A.value, __DateTime_A.set, None, None)

    
    # Element {http://www.w3schools.com}DateTime_B uses Python identifier DateTime_B
    __DateTime_B = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'DateTime_B'), 'DateTime_B', '__httpwww_w3schools_com_MT541_SequenceD_TwoLegTransactionDetails_httpwww_w3schools_comDateTime_B', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1626, 4), )

    
    DateTime_B = property(__DateTime_B.value, __DateTime_B.set, None, None)

    
    # Element {http://www.w3schools.com}DateTime_C uses Python identifier DateTime_C
    __DateTime_C = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'DateTime_C'), 'DateTime_C', '__httpwww_w3schools_com_MT541_SequenceD_TwoLegTransactionDetails_httpwww_w3schools_comDateTime_C', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1627, 4), )

    
    DateTime_C = property(__DateTime_C.value, __DateTime_C.set, None, None)

    
    # Element {http://www.w3schools.com}Indicator uses Python identifier Indicator
    __Indicator = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Indicator'), 'Indicator', '__httpwww_w3schools_com_MT541_SequenceD_TwoLegTransactionDetails_httpwww_w3schools_comIndicator', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1629, 3), )

    
    Indicator = property(__Indicator.value, __Indicator.set, None, None)

    
    # Element {http://www.w3schools.com}Reference uses Python identifier Reference
    __Reference = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Reference'), 'Reference', '__httpwww_w3schools_com_MT541_SequenceD_TwoLegTransactionDetails_httpwww_w3schools_comReference', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1630, 3), )

    
    Reference = property(__Reference.value, __Reference.set, None, None)

    
    # Element {http://www.w3schools.com}Rate_A uses Python identifier Rate_A
    __Rate_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Rate_A'), 'Rate_A', '__httpwww_w3schools_com_MT541_SequenceD_TwoLegTransactionDetails_httpwww_w3schools_comRate_A', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1632, 4), )

    
    Rate_A = property(__Rate_A.value, __Rate_A.set, None, None)

    
    # Element {http://www.w3schools.com}Rate_C uses Python identifier Rate_C
    __Rate_C = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Rate_C'), 'Rate_C', '__httpwww_w3schools_com_MT541_SequenceD_TwoLegTransactionDetails_httpwww_w3schools_comRate_C', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1633, 4), )

    
    Rate_C = property(__Rate_C.value, __Rate_C.set, None, None)

    
    # Element {http://www.w3schools.com}NumberCount uses Python identifier NumberCount
    __NumberCount = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'NumberCount'), 'NumberCount', '__httpwww_w3schools_com_MT541_SequenceD_TwoLegTransactionDetails_httpwww_w3schools_comNumberCount', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1635, 3), )

    
    NumberCount = property(__NumberCount.value, __NumberCount.set, None, None)

    
    # Element {http://www.w3schools.com}Amount uses Python identifier Amount
    __Amount = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Amount'), 'Amount', '__httpwww_w3schools_com_MT541_SequenceD_TwoLegTransactionDetails_httpwww_w3schools_comAmount', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1636, 3), )

    
    Amount = property(__Amount.value, __Amount.set, None, None)

    
    # Element {http://www.w3schools.com}SecondLegNarrative uses Python identifier SecondLegNarrative
    __SecondLegNarrative = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SecondLegNarrative'), 'SecondLegNarrative', '__httpwww_w3schools_com_MT541_SequenceD_TwoLegTransactionDetails_httpwww_w3schools_comSecondLegNarrative', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1637, 3), )

    
    SecondLegNarrative = property(__SecondLegNarrative.value, __SecondLegNarrative.set, None, None)

    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceD_TwoLegTransactionDetails_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='16R')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1639, 2)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1639, 2)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceD_TwoLegTransactionDetails_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1640, 2)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1640, 2)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    
    # Attribute formatTag uses Python identifier formatTag
    __formatTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'formatTag'), 'formatTag', '__httpwww_w3schools_com_MT541_SequenceD_TwoLegTransactionDetails_formatTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='REPO')
    __formatTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1641, 2)
    __formatTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1641, 2)
    
    formatTag = property(__formatTag.value, __formatTag.set, None, None)

    _ElementMap.update({
        __DateTime_A.name() : __DateTime_A,
        __DateTime_B.name() : __DateTime_B,
        __DateTime_C.name() : __DateTime_C,
        __Indicator.name() : __Indicator,
        __Reference.name() : __Reference,
        __Rate_A.name() : __Rate_A,
        __Rate_C.name() : __Rate_C,
        __NumberCount.name() : __NumberCount,
        __Amount.name() : __Amount,
        __SecondLegNarrative.name() : __SecondLegNarrative
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory,
        __formatTag.name() : __formatTag
    })
_module_typeBindings.MT541_SequenceD_TwoLegTransactionDetails = MT541_SequenceD_TwoLegTransactionDetails
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceD_TwoLegTransactionDetails', MT541_SequenceD_TwoLegTransactionDetails)


# Complex type {http://www.w3schools.com}MT541_SequenceE_SettlementDetails with content type ELEMENT_ONLY
class MT541_SequenceE_SettlementDetails (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceE_SettlementDetails with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceE_SettlementDetails')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1643, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}Indicator uses Python identifier Indicator
    __Indicator = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Indicator'), 'Indicator', '__httpwww_w3schools_com_MT541_SequenceE_SettlementDetails_httpwww_w3schools_comIndicator', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1645, 3), )

    
    Indicator = property(__Indicator.value, __Indicator.set, None, None)

    
    # Element {http://www.w3schools.com}SubSequenceE1_SettlementParties uses Python identifier SubSequenceE1_SettlementParties
    __SubSequenceE1_SettlementParties = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SubSequenceE1_SettlementParties'), 'SubSequenceE1_SettlementParties', '__httpwww_w3schools_com_MT541_SequenceE_SettlementDetails_httpwww_w3schools_comSubSequenceE1_SettlementParties', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1646, 3), )

    
    SubSequenceE1_SettlementParties = property(__SubSequenceE1_SettlementParties.value, __SubSequenceE1_SettlementParties.set, None, None)

    
    # Element {http://www.w3schools.com}SubSequenceE2_CashParties uses Python identifier SubSequenceE2_CashParties
    __SubSequenceE2_CashParties = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SubSequenceE2_CashParties'), 'SubSequenceE2_CashParties', '__httpwww_w3schools_com_MT541_SequenceE_SettlementDetails_httpwww_w3schools_comSubSequenceE2_CashParties', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1647, 3), )

    
    SubSequenceE2_CashParties = property(__SubSequenceE2_CashParties.value, __SubSequenceE2_CashParties.set, None, None)

    
    # Element {http://www.w3schools.com}SubSequenceE3_Amounts uses Python identifier SubSequenceE3_Amounts
    __SubSequenceE3_Amounts = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SubSequenceE3_Amounts'), 'SubSequenceE3_Amounts', '__httpwww_w3schools_com_MT541_SequenceE_SettlementDetails_httpwww_w3schools_comSubSequenceE3_Amounts', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1648, 3), )

    
    SubSequenceE3_Amounts = property(__SubSequenceE3_Amounts.value, __SubSequenceE3_Amounts.set, None, None)

    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceE_SettlementDetails_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='16R')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1650, 2)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1650, 2)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceE_SettlementDetails_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1651, 2)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1651, 2)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    
    # Attribute formatTag uses Python identifier formatTag
    __formatTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'formatTag'), 'formatTag', '__httpwww_w3schools_com_MT541_SequenceE_SettlementDetails_formatTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='SETDET')
    __formatTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1652, 2)
    __formatTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1652, 2)
    
    formatTag = property(__formatTag.value, __formatTag.set, None, None)

    _ElementMap.update({
        __Indicator.name() : __Indicator,
        __SubSequenceE1_SettlementParties.name() : __SubSequenceE1_SettlementParties,
        __SubSequenceE2_CashParties.name() : __SubSequenceE2_CashParties,
        __SubSequenceE3_Amounts.name() : __SubSequenceE3_Amounts
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory,
        __formatTag.name() : __formatTag
    })
_module_typeBindings.MT541_SequenceE_SettlementDetails = MT541_SequenceE_SettlementDetails
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceE_SettlementDetails', MT541_SequenceE_SettlementDetails)


# Complex type {http://www.w3schools.com}MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties with content type ELEMENT_ONLY
class MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1654, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}PARTY_C uses Python identifier PARTY_C
    __PARTY_C = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PARTY_C'), 'PARTY_C', '__httpwww_w3schools_com_MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_httpwww_w3schools_comPARTY_C', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1657, 4), )

    
    PARTY_C = property(__PARTY_C.value, __PARTY_C.set, None, None)

    
    # Element {http://www.w3schools.com}PARTY_L uses Python identifier PARTY_L
    __PARTY_L = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PARTY_L'), 'PARTY_L', '__httpwww_w3schools_com_MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_httpwww_w3schools_comPARTY_L', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1658, 4), )

    
    PARTY_L = property(__PARTY_L.value, __PARTY_L.set, None, None)

    
    # Element {http://www.w3schools.com}PARTY_P uses Python identifier PARTY_P
    __PARTY_P = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PARTY_P'), 'PARTY_P', '__httpwww_w3schools_com_MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_httpwww_w3schools_comPARTY_P', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1659, 4), )

    
    PARTY_P = property(__PARTY_P.value, __PARTY_P.set, None, None)

    
    # Element {http://www.w3schools.com}PARTY_Q uses Python identifier PARTY_Q
    __PARTY_Q = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PARTY_Q'), 'PARTY_Q', '__httpwww_w3schools_com_MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_httpwww_w3schools_comPARTY_Q', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1660, 4), )

    
    PARTY_Q = property(__PARTY_Q.value, __PARTY_Q.set, None, None)

    
    # Element {http://www.w3schools.com}PARTY_R uses Python identifier PARTY_R
    __PARTY_R = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PARTY_R'), 'PARTY_R', '__httpwww_w3schools_com_MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_httpwww_w3schools_comPARTY_R', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1661, 4), )

    
    PARTY_R = property(__PARTY_R.value, __PARTY_R.set, None, None)

    
    # Element {http://www.w3schools.com}PARTY_S uses Python identifier PARTY_S
    __PARTY_S = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PARTY_S'), 'PARTY_S', '__httpwww_w3schools_com_MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_httpwww_w3schools_comPARTY_S', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1662, 4), )

    
    PARTY_S = property(__PARTY_S.value, __PARTY_S.set, None, None)

    
    # Element {http://www.w3schools.com}SafekeepingAccount_A uses Python identifier SafekeepingAccount_A
    __SafekeepingAccount_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SafekeepingAccount_A'), 'SafekeepingAccount_A', '__httpwww_w3schools_com_MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_httpwww_w3schools_comSafekeepingAccount_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1665, 4), )

    
    SafekeepingAccount_A = property(__SafekeepingAccount_A.value, __SafekeepingAccount_A.set, None, None)

    
    # Element {http://www.w3schools.com}SafekeepingAccount_B uses Python identifier SafekeepingAccount_B
    __SafekeepingAccount_B = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SafekeepingAccount_B'), 'SafekeepingAccount_B', '__httpwww_w3schools_com_MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_httpwww_w3schools_comSafekeepingAccount_B', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1666, 4), )

    
    SafekeepingAccount_B = property(__SafekeepingAccount_B.value, __SafekeepingAccount_B.set, None, None)

    
    # Element {http://www.w3schools.com}ProcessingDateTime_A uses Python identifier ProcessingDateTime_A
    __ProcessingDateTime_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ProcessingDateTime_A'), 'ProcessingDateTime_A', '__httpwww_w3schools_com_MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_httpwww_w3schools_comProcessingDateTime_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1669, 4), )

    
    ProcessingDateTime_A = property(__ProcessingDateTime_A.value, __ProcessingDateTime_A.set, None, None)

    
    # Element {http://www.w3schools.com}ProcessingDateTime_C uses Python identifier ProcessingDateTime_C
    __ProcessingDateTime_C = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ProcessingDateTime_C'), 'ProcessingDateTime_C', '__httpwww_w3schools_com_MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_httpwww_w3schools_comProcessingDateTime_C', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1670, 4), )

    
    ProcessingDateTime_C = property(__ProcessingDateTime_C.value, __ProcessingDateTime_C.set, None, None)

    
    # Element {http://www.w3schools.com}ProcessingReference uses Python identifier ProcessingReference
    __ProcessingReference = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ProcessingReference'), 'ProcessingReference', '__httpwww_w3schools_com_MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_httpwww_w3schools_comProcessingReference', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1672, 3), )

    
    ProcessingReference = property(__ProcessingReference.value, __ProcessingReference.set, None, None)

    
    # Element {http://www.w3schools.com}Narrative_C uses Python identifier Narrative_C
    __Narrative_C = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Narrative_C'), 'Narrative_C', '__httpwww_w3schools_com_MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_httpwww_w3schools_comNarrative_C', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1674, 4), )

    
    Narrative_C = property(__Narrative_C.value, __Narrative_C.set, None, None)

    
    # Element {http://www.w3schools.com}Narrative_D uses Python identifier Narrative_D
    __Narrative_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Narrative_D'), 'Narrative_D', '__httpwww_w3schools_com_MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_httpwww_w3schools_comNarrative_D', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1675, 4), )

    
    Narrative_D = property(__Narrative_D.value, __Narrative_D.set, None, None)

    
    # Element {http://www.w3schools.com}Narrative_E uses Python identifier Narrative_E
    __Narrative_E = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Narrative_E'), 'Narrative_E', '__httpwww_w3schools_com_MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_httpwww_w3schools_comNarrative_E', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1676, 4), )

    
    Narrative_E = property(__Narrative_E.value, __Narrative_E.set, None, None)

    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='16R')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1679, 2)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1679, 2)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1680, 2)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1680, 2)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    
    # Attribute formatTag uses Python identifier formatTag
    __formatTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'formatTag'), 'formatTag', '__httpwww_w3schools_com_MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_formatTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='SETPRTY')
    __formatTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1681, 2)
    __formatTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1681, 2)
    
    formatTag = property(__formatTag.value, __formatTag.set, None, None)

    _ElementMap.update({
        __PARTY_C.name() : __PARTY_C,
        __PARTY_L.name() : __PARTY_L,
        __PARTY_P.name() : __PARTY_P,
        __PARTY_Q.name() : __PARTY_Q,
        __PARTY_R.name() : __PARTY_R,
        __PARTY_S.name() : __PARTY_S,
        __SafekeepingAccount_A.name() : __SafekeepingAccount_A,
        __SafekeepingAccount_B.name() : __SafekeepingAccount_B,
        __ProcessingDateTime_A.name() : __ProcessingDateTime_A,
        __ProcessingDateTime_C.name() : __ProcessingDateTime_C,
        __ProcessingReference.name() : __ProcessingReference,
        __Narrative_C.name() : __Narrative_C,
        __Narrative_D.name() : __Narrative_D,
        __Narrative_E.name() : __Narrative_E
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory,
        __formatTag.name() : __formatTag
    })
_module_typeBindings.MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties = MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties', MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties)


# Complex type {http://www.w3schools.com}MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties with content type ELEMENT_ONLY
class MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1683, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}PARTY_L uses Python identifier PARTY_L
    __PARTY_L = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PARTY_L'), 'PARTY_L', '__httpwww_w3schools_com_MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_httpwww_w3schools_comPARTY_L', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1686, 4), )

    
    PARTY_L = property(__PARTY_L.value, __PARTY_L.set, None, None)

    
    # Element {http://www.w3schools.com}PARTY_P uses Python identifier PARTY_P
    __PARTY_P = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PARTY_P'), 'PARTY_P', '__httpwww_w3schools_com_MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_httpwww_w3schools_comPARTY_P', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1687, 4), )

    
    PARTY_P = property(__PARTY_P.value, __PARTY_P.set, None, None)

    
    # Element {http://www.w3schools.com}PARTY_Q uses Python identifier PARTY_Q
    __PARTY_Q = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PARTY_Q'), 'PARTY_Q', '__httpwww_w3schools_com_MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_httpwww_w3schools_comPARTY_Q', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1688, 4), )

    
    PARTY_Q = property(__PARTY_Q.value, __PARTY_Q.set, None, None)

    
    # Element {http://www.w3schools.com}PARTY_R uses Python identifier PARTY_R
    __PARTY_R = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PARTY_R'), 'PARTY_R', '__httpwww_w3schools_com_MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_httpwww_w3schools_comPARTY_R', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1689, 4), )

    
    PARTY_R = property(__PARTY_R.value, __PARTY_R.set, None, None)

    
    # Element {http://www.w3schools.com}PARTY_S uses Python identifier PARTY_S
    __PARTY_S = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PARTY_S'), 'PARTY_S', '__httpwww_w3schools_com_MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_httpwww_w3schools_comPARTY_S', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1690, 4), )

    
    PARTY_S = property(__PARTY_S.value, __PARTY_S.set, None, None)

    
    # Element {http://www.w3schools.com}Account_A uses Python identifier Account_A
    __Account_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Account_A'), 'Account_A', '__httpwww_w3schools_com_MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_httpwww_w3schools_comAccount_A', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1693, 4), )

    
    Account_A = property(__Account_A.value, __Account_A.set, None, None)

    
    # Element {http://www.w3schools.com}Account_E uses Python identifier Account_E
    __Account_E = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Account_E'), 'Account_E', '__httpwww_w3schools_com_MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_httpwww_w3schools_comAccount_E', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1694, 4), )

    
    Account_E = property(__Account_E.value, __Account_E.set, None, None)

    
    # Element {http://www.w3schools.com}Narrative_C uses Python identifier Narrative_C
    __Narrative_C = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Narrative_C'), 'Narrative_C', '__httpwww_w3schools_com_MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_httpwww_w3schools_comNarrative_C', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1697, 4), )

    
    Narrative_C = property(__Narrative_C.value, __Narrative_C.set, None, None)

    
    # Element {http://www.w3schools.com}Narrative_E uses Python identifier Narrative_E
    __Narrative_E = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Narrative_E'), 'Narrative_E', '__httpwww_w3schools_com_MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_httpwww_w3schools_comNarrative_E', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1698, 4), )

    
    Narrative_E = property(__Narrative_E.value, __Narrative_E.set, None, None)

    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='16R')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1701, 2)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1701, 2)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1702, 2)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1702, 2)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    
    # Attribute formatTag uses Python identifier formatTag
    __formatTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'formatTag'), 'formatTag', '__httpwww_w3schools_com_MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_formatTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='CSHPRTY')
    __formatTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1703, 2)
    __formatTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1703, 2)
    
    formatTag = property(__formatTag.value, __formatTag.set, None, None)

    _ElementMap.update({
        __PARTY_L.name() : __PARTY_L,
        __PARTY_P.name() : __PARTY_P,
        __PARTY_Q.name() : __PARTY_Q,
        __PARTY_R.name() : __PARTY_R,
        __PARTY_S.name() : __PARTY_S,
        __Account_A.name() : __Account_A,
        __Account_E.name() : __Account_E,
        __Narrative_C.name() : __Narrative_C,
        __Narrative_E.name() : __Narrative_E
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory,
        __formatTag.name() : __formatTag
    })
_module_typeBindings.MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties = MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties', MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties)


# Complex type {http://www.w3schools.com}MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts with content type ELEMENT_ONLY
class MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1705, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}Flag uses Python identifier Flag
    __Flag = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Flag'), 'Flag', '__httpwww_w3schools_com_MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_httpwww_w3schools_comFlag', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1707, 3), )

    
    Flag = property(__Flag.value, __Flag.set, None, None)

    
    # Element {http://www.w3schools.com}Amount uses Python identifier Amount
    __Amount = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Amount'), 'Amount', '__httpwww_w3schools_com_MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_httpwww_w3schools_comAmount', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1708, 3), )

    
    Amount = property(__Amount.value, __Amount.set, None, None)

    
    # Element {http://www.w3schools.com}ValueDateTime_A uses Python identifier ValueDateTime_A
    __ValueDateTime_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ValueDateTime_A'), 'ValueDateTime_A', '__httpwww_w3schools_com_MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_httpwww_w3schools_comValueDateTime_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1710, 4), )

    
    ValueDateTime_A = property(__ValueDateTime_A.value, __ValueDateTime_A.set, None, None)

    
    # Element {http://www.w3schools.com}ValueDateTime_C uses Python identifier ValueDateTime_C
    __ValueDateTime_C = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ValueDateTime_C'), 'ValueDateTime_C', '__httpwww_w3schools_com_MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_httpwww_w3schools_comValueDateTime_C', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1711, 4), )

    
    ValueDateTime_C = property(__ValueDateTime_C.value, __ValueDateTime_C.set, None, None)

    
    # Element {http://www.w3schools.com}ExchangeRate uses Python identifier ExchangeRate
    __ExchangeRate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ExchangeRate'), 'ExchangeRate', '__httpwww_w3schools_com_MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_httpwww_w3schools_comExchangeRate', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1713, 3), )

    
    ExchangeRate = property(__ExchangeRate.value, __ExchangeRate.set, None, None)

    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='16R')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1715, 2)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1715, 2)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1716, 2)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1716, 2)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    
    # Attribute formatTag uses Python identifier formatTag
    __formatTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'formatTag'), 'formatTag', '__httpwww_w3schools_com_MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_formatTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='AMT')
    __formatTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1717, 2)
    __formatTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1717, 2)
    
    formatTag = property(__formatTag.value, __formatTag.set, None, None)

    _ElementMap.update({
        __Flag.name() : __Flag,
        __Amount.name() : __Amount,
        __ValueDateTime_A.name() : __ValueDateTime_A,
        __ValueDateTime_C.name() : __ValueDateTime_C,
        __ExchangeRate.name() : __ExchangeRate
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory,
        __formatTag.name() : __formatTag
    })
_module_typeBindings.MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts = MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts', MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts)


# Complex type {http://www.w3schools.com}MT541_SequenceF_OtherParties with content type ELEMENT_ONLY
class MT541_SequenceF_OtherParties (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceF_OtherParties with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceF_OtherParties')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1719, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}PARTY_C uses Python identifier PARTY_C
    __PARTY_C = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PARTY_C'), 'PARTY_C', '__httpwww_w3schools_com_MT541_SequenceF_OtherParties_httpwww_w3schools_comPARTY_C', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1722, 4), )

    
    PARTY_C = property(__PARTY_C.value, __PARTY_C.set, None, None)

    
    # Element {http://www.w3schools.com}PARTY_L uses Python identifier PARTY_L
    __PARTY_L = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PARTY_L'), 'PARTY_L', '__httpwww_w3schools_com_MT541_SequenceF_OtherParties_httpwww_w3schools_comPARTY_L', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1723, 4), )

    
    PARTY_L = property(__PARTY_L.value, __PARTY_L.set, None, None)

    
    # Element {http://www.w3schools.com}PARTY_P uses Python identifier PARTY_P
    __PARTY_P = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PARTY_P'), 'PARTY_P', '__httpwww_w3schools_com_MT541_SequenceF_OtherParties_httpwww_w3schools_comPARTY_P', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1724, 4), )

    
    PARTY_P = property(__PARTY_P.value, __PARTY_P.set, None, None)

    
    # Element {http://www.w3schools.com}PARTY_Q uses Python identifier PARTY_Q
    __PARTY_Q = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PARTY_Q'), 'PARTY_Q', '__httpwww_w3schools_com_MT541_SequenceF_OtherParties_httpwww_w3schools_comPARTY_Q', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1725, 4), )

    
    PARTY_Q = property(__PARTY_Q.value, __PARTY_Q.set, None, None)

    
    # Element {http://www.w3schools.com}PARTY_R uses Python identifier PARTY_R
    __PARTY_R = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PARTY_R'), 'PARTY_R', '__httpwww_w3schools_com_MT541_SequenceF_OtherParties_httpwww_w3schools_comPARTY_R', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1726, 4), )

    
    PARTY_R = property(__PARTY_R.value, __PARTY_R.set, None, None)

    
    # Element {http://www.w3schools.com}PARTY_S uses Python identifier PARTY_S
    __PARTY_S = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PARTY_S'), 'PARTY_S', '__httpwww_w3schools_com_MT541_SequenceF_OtherParties_httpwww_w3schools_comPARTY_S', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1727, 4), )

    
    PARTY_S = property(__PARTY_S.value, __PARTY_S.set, None, None)

    
    # Element {http://www.w3schools.com}SafekeepingAccount uses Python identifier SafekeepingAccount
    __SafekeepingAccount = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SafekeepingAccount'), 'SafekeepingAccount', '__httpwww_w3schools_com_MT541_SequenceF_OtherParties_httpwww_w3schools_comSafekeepingAccount', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1729, 3), )

    
    SafekeepingAccount = property(__SafekeepingAccount.value, __SafekeepingAccount.set, None, None)

    
    # Element {http://www.w3schools.com}Narrative_C uses Python identifier Narrative_C
    __Narrative_C = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Narrative_C'), 'Narrative_C', '__httpwww_w3schools_com_MT541_SequenceF_OtherParties_httpwww_w3schools_comNarrative_C', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1731, 4), )

    
    Narrative_C = property(__Narrative_C.value, __Narrative_C.set, None, None)

    
    # Element {http://www.w3schools.com}Narrative_D uses Python identifier Narrative_D
    __Narrative_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Narrative_D'), 'Narrative_D', '__httpwww_w3schools_com_MT541_SequenceF_OtherParties_httpwww_w3schools_comNarrative_D', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1732, 4), )

    
    Narrative_D = property(__Narrative_D.value, __Narrative_D.set, None, None)

    
    # Element {http://www.w3schools.com}Narrative_E uses Python identifier Narrative_E
    __Narrative_E = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Narrative_E'), 'Narrative_E', '__httpwww_w3schools_com_MT541_SequenceF_OtherParties_httpwww_w3schools_comNarrative_E', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1733, 4), )

    
    Narrative_E = property(__Narrative_E.value, __Narrative_E.set, None, None)

    
    # Element {http://www.w3schools.com}ProcessingReference uses Python identifier ProcessingReference
    __ProcessingReference = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ProcessingReference'), 'ProcessingReference', '__httpwww_w3schools_com_MT541_SequenceF_OtherParties_httpwww_w3schools_comProcessingReference', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1735, 3), )

    
    ProcessingReference = property(__ProcessingReference.value, __ProcessingReference.set, None, None)

    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceF_OtherParties_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='16R')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1737, 2)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1737, 2)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceF_OtherParties_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1738, 2)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1738, 2)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    
    # Attribute formatTag uses Python identifier formatTag
    __formatTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'formatTag'), 'formatTag', '__httpwww_w3schools_com_MT541_SequenceF_OtherParties_formatTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='OTHRPRTY')
    __formatTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1739, 2)
    __formatTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1739, 2)
    
    formatTag = property(__formatTag.value, __formatTag.set, None, None)

    _ElementMap.update({
        __PARTY_C.name() : __PARTY_C,
        __PARTY_L.name() : __PARTY_L,
        __PARTY_P.name() : __PARTY_P,
        __PARTY_Q.name() : __PARTY_Q,
        __PARTY_R.name() : __PARTY_R,
        __PARTY_S.name() : __PARTY_S,
        __SafekeepingAccount.name() : __SafekeepingAccount,
        __Narrative_C.name() : __Narrative_C,
        __Narrative_D.name() : __Narrative_D,
        __Narrative_E.name() : __Narrative_E,
        __ProcessingReference.name() : __ProcessingReference
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory,
        __formatTag.name() : __formatTag
    })
_module_typeBindings.MT541_SequenceF_OtherParties = MT541_SequenceF_OtherParties
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceF_OtherParties', MT541_SequenceF_OtherParties)


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1742, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}SequenceA_GeneralInformation uses Python identifier SequenceA_GeneralInformation
    __SequenceA_GeneralInformation = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SequenceA_GeneralInformation'), 'SequenceA_GeneralInformation', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comSequenceA_GeneralInformation', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1744, 4), )

    
    SequenceA_GeneralInformation = property(__SequenceA_GeneralInformation.value, __SequenceA_GeneralInformation.set, None, None)

    
    # Element {http://www.w3schools.com}SequenceB_TradeDetails uses Python identifier SequenceB_TradeDetails
    __SequenceB_TradeDetails = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SequenceB_TradeDetails'), 'SequenceB_TradeDetails', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comSequenceB_TradeDetails', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1745, 4), )

    
    SequenceB_TradeDetails = property(__SequenceB_TradeDetails.value, __SequenceB_TradeDetails.set, None, None)

    
    # Element {http://www.w3schools.com}SequenceC_FinancialInstrumentAccount uses Python identifier SequenceC_FinancialInstrumentAccount
    __SequenceC_FinancialInstrumentAccount = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SequenceC_FinancialInstrumentAccount'), 'SequenceC_FinancialInstrumentAccount', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comSequenceC_FinancialInstrumentAccount', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1746, 4), )

    
    SequenceC_FinancialInstrumentAccount = property(__SequenceC_FinancialInstrumentAccount.value, __SequenceC_FinancialInstrumentAccount.set, None, None)

    
    # Element {http://www.w3schools.com}SequenceD_TwoLegTransactionDetails uses Python identifier SequenceD_TwoLegTransactionDetails
    __SequenceD_TwoLegTransactionDetails = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SequenceD_TwoLegTransactionDetails'), 'SequenceD_TwoLegTransactionDetails', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comSequenceD_TwoLegTransactionDetails', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1747, 4), )

    
    SequenceD_TwoLegTransactionDetails = property(__SequenceD_TwoLegTransactionDetails.value, __SequenceD_TwoLegTransactionDetails.set, None, None)

    
    # Element {http://www.w3schools.com}SequenceE_SettlementDetails uses Python identifier SequenceE_SettlementDetails
    __SequenceE_SettlementDetails = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SequenceE_SettlementDetails'), 'SequenceE_SettlementDetails', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comSequenceE_SettlementDetails', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1748, 4), )

    
    SequenceE_SettlementDetails = property(__SequenceE_SettlementDetails.value, __SequenceE_SettlementDetails.set, None, None)

    
    # Element {http://www.w3schools.com}SequenceF_OtherParties uses Python identifier SequenceF_OtherParties
    __SequenceF_OtherParties = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SequenceF_OtherParties'), 'SequenceF_OtherParties', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comSequenceF_OtherParties', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1749, 4), )

    
    SequenceF_OtherParties = property(__SequenceF_OtherParties.value, __SequenceF_OtherParties.set, None, None)

    _ElementMap.update({
        __SequenceA_GeneralInformation.name() : __SequenceA_GeneralInformation,
        __SequenceB_TradeDetails.name() : __SequenceB_TradeDetails,
        __SequenceC_FinancialInstrumentAccount.name() : __SequenceC_FinancialInstrumentAccount,
        __SequenceD_TwoLegTransactionDetails.name() : __SequenceD_TwoLegTransactionDetails,
        __SequenceE_SettlementDetails.name() : __SequenceE_SettlementDetails,
        __SequenceF_OtherParties.name() : __SequenceF_OtherParties
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON = CTD_ANON


# Complex type {http://www.w3schools.com}MT541_SequenceA_GeneralInformation_20C_Type with content type SIMPLE
class MT541_SequenceA_GeneralInformation_20C_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceA_GeneralInformation_20C_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceA_GeneralInformation_20C_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceA_GeneralInformation_20C_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 8, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceA_GeneralInformation_20C_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceA_GeneralInformation_20C_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='20C')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 11, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 11, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceA_GeneralInformation_20C_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 12, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 12, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceA_GeneralInformation_20C_Type = MT541_SequenceA_GeneralInformation_20C_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceA_GeneralInformation_20C_Type', MT541_SequenceA_GeneralInformation_20C_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceA_GeneralInformation_23G_Type with content type SIMPLE
class MT541_SequenceA_GeneralInformation_23G_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceA_GeneralInformation_23G_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceA_GeneralInformation_23G_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceA_GeneralInformation_23G_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 21, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceA_GeneralInformation_23G_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceA_GeneralInformation_23G_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='23G')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 24, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 24, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceA_GeneralInformation_23G_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 25, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 25, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceA_GeneralInformation_23G_Type = MT541_SequenceA_GeneralInformation_23G_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceA_GeneralInformation_23G_Type', MT541_SequenceA_GeneralInformation_23G_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceA_GeneralInformation_98A_Type with content type SIMPLE
class MT541_SequenceA_GeneralInformation_98A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceA_GeneralInformation_98A_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceA_GeneralInformation_98A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceA_GeneralInformation_98A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 34, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceA_GeneralInformation_98A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceA_GeneralInformation_98A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='98A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 37, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 37, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceA_GeneralInformation_98A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 38, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 38, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceA_GeneralInformation_98A_Type = MT541_SequenceA_GeneralInformation_98A_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceA_GeneralInformation_98A_Type', MT541_SequenceA_GeneralInformation_98A_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceA_GeneralInformation_98C_Type with content type SIMPLE
class MT541_SequenceA_GeneralInformation_98C_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceA_GeneralInformation_98C_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceA_GeneralInformation_98C_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceA_GeneralInformation_98C_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 47, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceA_GeneralInformation_98C_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceA_GeneralInformation_98C_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='98C')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 50, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 50, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceA_GeneralInformation_98C_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 51, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 51, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceA_GeneralInformation_98C_Type = MT541_SequenceA_GeneralInformation_98C_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceA_GeneralInformation_98C_Type', MT541_SequenceA_GeneralInformation_98C_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceA_GeneralInformation_98E_Type with content type SIMPLE
class MT541_SequenceA_GeneralInformation_98E_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceA_GeneralInformation_98E_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceA_GeneralInformation_98E_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceA_GeneralInformation_98E_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 60, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceA_GeneralInformation_98E_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceA_GeneralInformation_98E_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='98E')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 63, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 63, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceA_GeneralInformation_98E_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 64, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 64, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceA_GeneralInformation_98E_Type = MT541_SequenceA_GeneralInformation_98E_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceA_GeneralInformation_98E_Type', MT541_SequenceA_GeneralInformation_98E_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceA_GeneralInformation_99B_Type with content type SIMPLE
class MT541_SequenceA_GeneralInformation_99B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceA_GeneralInformation_99B_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceA_GeneralInformation_99B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceA_GeneralInformation_99B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 73, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceA_GeneralInformation_99B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceA_GeneralInformation_99B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='99B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 76, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 76, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceA_GeneralInformation_99B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 77, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 77, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceA_GeneralInformation_99B_Type = MT541_SequenceA_GeneralInformation_99B_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceA_GeneralInformation_99B_Type', MT541_SequenceA_GeneralInformation_99B_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_22F_Type with content type SIMPLE
class MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_22F_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_22F_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_22F_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_22F_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 86, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_22F_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_22F_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='22F')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 89, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 89, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_22F_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 90, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 90, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_22F_Type = MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_22F_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_22F_Type', MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_22F_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13A_Type with content type SIMPLE
class MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13A_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 99, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='13A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 102, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 102, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 103, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 103, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13A_Type = MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13A_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13A_Type', MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13A_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13B_Type with content type SIMPLE
class MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13B_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 112, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='13B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 115, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 115, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 116, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 116, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13B_Type = MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13B_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13B_Type', MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13B_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20C_Type with content type SIMPLE
class MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20C_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20C_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20C_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20C_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 125, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20C_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20C_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='20C')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 128, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 128, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20C_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 129, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 129, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20C_Type = MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20C_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20C_Type', MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20C_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20U_Type with content type SIMPLE
class MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20U_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20U_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20U_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20U_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 138, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20U_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20U_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='20U')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 141, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 141, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20U_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 142, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 142, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20U_Type = MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20U_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20U_Type', MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20U_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_36B_Type with content type SIMPLE
class MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_36B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_36B_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_36B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_36B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 151, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_36B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_36B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='36B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 154, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 154, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_36B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 155, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 155, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_36B_Type = MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_36B_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_36B_Type', MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_36B_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceB_TradeDetails_94B_Type with content type SIMPLE
class MT541_SequenceB_TradeDetails_94B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceB_TradeDetails_94B_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceB_TradeDetails_94B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceB_TradeDetails_94B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 164, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceB_TradeDetails_94B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceB_TradeDetails_94B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='94B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 167, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 167, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceB_TradeDetails_94B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 168, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 168, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceB_TradeDetails_94B_Type = MT541_SequenceB_TradeDetails_94B_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceB_TradeDetails_94B_Type', MT541_SequenceB_TradeDetails_94B_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceB_TradeDetails_94H_Type with content type SIMPLE
class MT541_SequenceB_TradeDetails_94H_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceB_TradeDetails_94H_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceB_TradeDetails_94H_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceB_TradeDetails_94H_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 177, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceB_TradeDetails_94H_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceB_TradeDetails_94H_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='94H')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 180, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 180, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceB_TradeDetails_94H_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 181, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 181, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceB_TradeDetails_94H_Type = MT541_SequenceB_TradeDetails_94H_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceB_TradeDetails_94H_Type', MT541_SequenceB_TradeDetails_94H_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceB_TradeDetails_94L_Type with content type SIMPLE
class MT541_SequenceB_TradeDetails_94L_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceB_TradeDetails_94L_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceB_TradeDetails_94L_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceB_TradeDetails_94L_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 190, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceB_TradeDetails_94L_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceB_TradeDetails_94L_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='94L')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 193, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 193, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceB_TradeDetails_94L_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 194, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 194, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceB_TradeDetails_94L_Type = MT541_SequenceB_TradeDetails_94L_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceB_TradeDetails_94L_Type', MT541_SequenceB_TradeDetails_94L_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceB_TradeDetails_98A_Type with content type SIMPLE
class MT541_SequenceB_TradeDetails_98A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceB_TradeDetails_98A_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceB_TradeDetails_98A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceB_TradeDetails_98A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 203, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceB_TradeDetails_98A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceB_TradeDetails_98A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='98A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 206, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 206, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceB_TradeDetails_98A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 207, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 207, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceB_TradeDetails_98A_Type = MT541_SequenceB_TradeDetails_98A_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceB_TradeDetails_98A_Type', MT541_SequenceB_TradeDetails_98A_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceB_TradeDetails_98B_Type with content type SIMPLE
class MT541_SequenceB_TradeDetails_98B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceB_TradeDetails_98B_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceB_TradeDetails_98B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceB_TradeDetails_98B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 216, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceB_TradeDetails_98B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceB_TradeDetails_98B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='98B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 219, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 219, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceB_TradeDetails_98B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 220, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 220, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceB_TradeDetails_98B_Type = MT541_SequenceB_TradeDetails_98B_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceB_TradeDetails_98B_Type', MT541_SequenceB_TradeDetails_98B_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceB_TradeDetails_98C_Type with content type SIMPLE
class MT541_SequenceB_TradeDetails_98C_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceB_TradeDetails_98C_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceB_TradeDetails_98C_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceB_TradeDetails_98C_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 229, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceB_TradeDetails_98C_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceB_TradeDetails_98C_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='98C')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 232, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 232, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceB_TradeDetails_98C_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 233, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 233, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceB_TradeDetails_98C_Type = MT541_SequenceB_TradeDetails_98C_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceB_TradeDetails_98C_Type', MT541_SequenceB_TradeDetails_98C_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceB_TradeDetails_98E_Type with content type SIMPLE
class MT541_SequenceB_TradeDetails_98E_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceB_TradeDetails_98E_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceB_TradeDetails_98E_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceB_TradeDetails_98E_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 242, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceB_TradeDetails_98E_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceB_TradeDetails_98E_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='98E')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 245, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 245, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceB_TradeDetails_98E_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 246, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 246, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceB_TradeDetails_98E_Type = MT541_SequenceB_TradeDetails_98E_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceB_TradeDetails_98E_Type', MT541_SequenceB_TradeDetails_98E_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceB_TradeDetails_90A_Type with content type SIMPLE
class MT541_SequenceB_TradeDetails_90A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceB_TradeDetails_90A_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceB_TradeDetails_90A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceB_TradeDetails_90A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 255, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceB_TradeDetails_90A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceB_TradeDetails_90A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='90A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 258, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 258, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceB_TradeDetails_90A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 259, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 259, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceB_TradeDetails_90A_Type = MT541_SequenceB_TradeDetails_90A_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceB_TradeDetails_90A_Type', MT541_SequenceB_TradeDetails_90A_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceB_TradeDetails_90B_Type with content type SIMPLE
class MT541_SequenceB_TradeDetails_90B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceB_TradeDetails_90B_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceB_TradeDetails_90B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceB_TradeDetails_90B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 268, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceB_TradeDetails_90B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceB_TradeDetails_90B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='90B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 271, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 271, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceB_TradeDetails_90B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 272, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 272, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceB_TradeDetails_90B_Type = MT541_SequenceB_TradeDetails_90B_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceB_TradeDetails_90B_Type', MT541_SequenceB_TradeDetails_90B_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceB_TradeDetails_99A_Type with content type SIMPLE
class MT541_SequenceB_TradeDetails_99A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceB_TradeDetails_99A_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceB_TradeDetails_99A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceB_TradeDetails_99A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 281, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceB_TradeDetails_99A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceB_TradeDetails_99A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='99A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 284, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 284, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceB_TradeDetails_99A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 285, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 285, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceB_TradeDetails_99A_Type = MT541_SequenceB_TradeDetails_99A_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceB_TradeDetails_99A_Type', MT541_SequenceB_TradeDetails_99A_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceB_TradeDetails_35B_Type with content type SIMPLE
class MT541_SequenceB_TradeDetails_35B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceB_TradeDetails_35B_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceB_TradeDetails_35B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceB_TradeDetails_35B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 294, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceB_TradeDetails_35B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceB_TradeDetails_35B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='35B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 297, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 297, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceB_TradeDetails_35B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 298, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 298, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceB_TradeDetails_35B_Type = MT541_SequenceB_TradeDetails_35B_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceB_TradeDetails_35B_Type', MT541_SequenceB_TradeDetails_35B_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_94B_Type with content type SIMPLE
class MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_94B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_94B_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_94B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_94B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 307, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_94B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_94B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='94B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 310, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 310, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_94B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 311, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 311, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_94B_Type = MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_94B_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_94B_Type', MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_94B_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_22F_Type with content type SIMPLE
class MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_22F_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_22F_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_22F_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_22F_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 320, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_22F_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_22F_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='22F')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 323, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 323, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_22F_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 324, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 324, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_22F_Type = MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_22F_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_22F_Type', MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_22F_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_12A_Type with content type SIMPLE
class MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_12A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_12A_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_12A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_12A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 333, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_12A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_12A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='12A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 336, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 336, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_12A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 337, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 337, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_12A_Type = MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_12A_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_12A_Type', MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_12A_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_12B_Type with content type SIMPLE
class MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_12B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_12B_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_12B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_12B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 346, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_12B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_12B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='12B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 349, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 349, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_12B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 350, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 350, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_12B_Type = MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_12B_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_12B_Type', MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_12B_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_12C_Type with content type SIMPLE
class MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_12C_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_12C_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_12C_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_12C_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 359, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_12C_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_12C_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='12C')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 362, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 362, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_12C_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 363, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 363, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_12C_Type = MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_12C_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_12C_Type', MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_12C_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_11A_Type with content type SIMPLE
class MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_11A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_11A_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_11A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_11A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 372, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_11A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_11A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='11A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 375, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 375, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_11A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 376, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 376, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_11A_Type = MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_11A_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_11A_Type', MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_11A_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_98A_Type with content type SIMPLE
class MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_98A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_98A_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_98A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_98A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 385, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_98A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_98A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='98A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 388, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 388, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_98A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 389, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 389, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_98A_Type = MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_98A_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_98A_Type', MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_98A_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_92A_Type with content type SIMPLE
class MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_92A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_92A_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_92A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_92A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 398, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_92A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_92A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='92A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 401, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 401, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_92A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 402, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 402, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_92A_Type = MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_92A_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_92A_Type', MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_92A_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_13A_Type with content type SIMPLE
class MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_13A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_13A_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_13A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_13A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 411, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_13A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_13A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='13A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 414, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 414, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_13A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 415, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 415, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_13A_Type = MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_13A_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_13A_Type', MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_13A_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_13B_Type with content type SIMPLE
class MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_13B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_13B_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_13B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_13B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 424, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_13B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_13B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='13B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 427, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 427, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_13B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 428, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 428, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_13B_Type = MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_13B_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_13B_Type', MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_13B_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_17B_Type with content type SIMPLE
class MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_17B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_17B_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_17B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_17B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 437, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_17B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_17B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='17B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 440, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 440, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_17B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 441, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 441, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_17B_Type = MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_17B_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_17B_Type', MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_17B_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_90A_Type with content type SIMPLE
class MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_90A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_90A_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_90A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_90A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 450, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_90A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_90A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='90A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 453, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 453, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_90A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 454, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 454, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_90A_Type = MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_90A_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_90A_Type', MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_90A_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_90B_Type with content type SIMPLE
class MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_90B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_90B_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_90B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_90B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 463, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_90B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_90B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='90B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 466, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 466, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_90B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 467, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 467, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_90B_Type = MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_90B_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_90B_Type', MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_90B_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_36B_Type with content type SIMPLE
class MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_36B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_36B_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_36B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_36B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 476, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_36B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_36B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='36B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 479, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 479, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_36B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 480, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 480, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_36B_Type = MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_36B_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_36B_Type', MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_36B_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_35B_Type with content type SIMPLE
class MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_35B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_35B_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_35B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_35B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 489, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_35B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_35B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='35B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 492, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 492, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_35B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 493, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 493, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_35B_Type = MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_35B_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_35B_Type', MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_35B_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_70E_Type with content type SIMPLE
class MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_70E_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_70E_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_70E_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_70E_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 502, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_70E_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_70E_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='70E')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 505, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 505, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_70E_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 506, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 506, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_70E_Type = MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_70E_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_70E_Type', MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_70E_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceB_TradeDetails_22F_Type with content type SIMPLE
class MT541_SequenceB_TradeDetails_22F_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceB_TradeDetails_22F_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceB_TradeDetails_22F_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceB_TradeDetails_22F_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 515, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceB_TradeDetails_22F_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceB_TradeDetails_22F_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='22F')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 518, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 518, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceB_TradeDetails_22F_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 519, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 519, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceB_TradeDetails_22F_Type = MT541_SequenceB_TradeDetails_22F_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceB_TradeDetails_22F_Type', MT541_SequenceB_TradeDetails_22F_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceB_TradeDetails_11A_Type with content type SIMPLE
class MT541_SequenceB_TradeDetails_11A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceB_TradeDetails_11A_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceB_TradeDetails_11A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceB_TradeDetails_11A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 528, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceB_TradeDetails_11A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceB_TradeDetails_11A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='11A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 531, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 531, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceB_TradeDetails_11A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 532, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 532, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceB_TradeDetails_11A_Type = MT541_SequenceB_TradeDetails_11A_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceB_TradeDetails_11A_Type', MT541_SequenceB_TradeDetails_11A_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceB_TradeDetails_25D_Type with content type SIMPLE
class MT541_SequenceB_TradeDetails_25D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceB_TradeDetails_25D_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceB_TradeDetails_25D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceB_TradeDetails_25D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 541, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceB_TradeDetails_25D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceB_TradeDetails_25D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='25D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 544, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 544, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceB_TradeDetails_25D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 545, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 545, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceB_TradeDetails_25D_Type = MT541_SequenceB_TradeDetails_25D_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceB_TradeDetails_25D_Type', MT541_SequenceB_TradeDetails_25D_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceB_TradeDetails_70E_Type with content type SIMPLE
class MT541_SequenceB_TradeDetails_70E_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceB_TradeDetails_70E_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceB_TradeDetails_70E_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceB_TradeDetails_70E_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 554, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceB_TradeDetails_70E_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceB_TradeDetails_70E_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='70E')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 557, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 557, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceB_TradeDetails_70E_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 558, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 558, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceB_TradeDetails_70E_Type = MT541_SequenceB_TradeDetails_70E_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceB_TradeDetails_70E_Type', MT541_SequenceB_TradeDetails_70E_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceC_FinancialInstrumentAccount_36B_Type with content type SIMPLE
class MT541_SequenceC_FinancialInstrumentAccount_36B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceC_FinancialInstrumentAccount_36B_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceC_FinancialInstrumentAccount_36B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceC_FinancialInstrumentAccount_36B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 567, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceC_FinancialInstrumentAccount_36B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceC_FinancialInstrumentAccount_36B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='36B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 570, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 570, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceC_FinancialInstrumentAccount_36B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 571, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 571, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceC_FinancialInstrumentAccount_36B_Type = MT541_SequenceC_FinancialInstrumentAccount_36B_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceC_FinancialInstrumentAccount_36B_Type', MT541_SequenceC_FinancialInstrumentAccount_36B_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceC_FinancialInstrumentAccount_70D_Type with content type SIMPLE
class MT541_SequenceC_FinancialInstrumentAccount_70D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceC_FinancialInstrumentAccount_70D_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceC_FinancialInstrumentAccount_70D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceC_FinancialInstrumentAccount_70D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 580, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceC_FinancialInstrumentAccount_70D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceC_FinancialInstrumentAccount_70D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='70D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 583, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 583, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceC_FinancialInstrumentAccount_70D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 584, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 584, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceC_FinancialInstrumentAccount_70D_Type = MT541_SequenceC_FinancialInstrumentAccount_70D_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceC_FinancialInstrumentAccount_70D_Type', MT541_SequenceC_FinancialInstrumentAccount_70D_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceC_FinancialInstrumentAccount_13B_Type with content type SIMPLE
class MT541_SequenceC_FinancialInstrumentAccount_13B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceC_FinancialInstrumentAccount_13B_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceC_FinancialInstrumentAccount_13B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceC_FinancialInstrumentAccount_13B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 593, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceC_FinancialInstrumentAccount_13B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceC_FinancialInstrumentAccount_13B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='13B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 596, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 596, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceC_FinancialInstrumentAccount_13B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 597, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 597, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceC_FinancialInstrumentAccount_13B_Type = MT541_SequenceC_FinancialInstrumentAccount_13B_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceC_FinancialInstrumentAccount_13B_Type', MT541_SequenceC_FinancialInstrumentAccount_13B_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceC_FinancialInstrumentAccount_95L_Type with content type SIMPLE
class MT541_SequenceC_FinancialInstrumentAccount_95L_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceC_FinancialInstrumentAccount_95L_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceC_FinancialInstrumentAccount_95L_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceC_FinancialInstrumentAccount_95L_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 606, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceC_FinancialInstrumentAccount_95L_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceC_FinancialInstrumentAccount_95L_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='95L')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 609, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 609, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceC_FinancialInstrumentAccount_95L_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 610, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 610, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceC_FinancialInstrumentAccount_95L_Type = MT541_SequenceC_FinancialInstrumentAccount_95L_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceC_FinancialInstrumentAccount_95L_Type', MT541_SequenceC_FinancialInstrumentAccount_95L_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceC_FinancialInstrumentAccount_95P_Type with content type SIMPLE
class MT541_SequenceC_FinancialInstrumentAccount_95P_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceC_FinancialInstrumentAccount_95P_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceC_FinancialInstrumentAccount_95P_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceC_FinancialInstrumentAccount_95P_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 619, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceC_FinancialInstrumentAccount_95P_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceC_FinancialInstrumentAccount_95P_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='95P')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 622, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 622, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceC_FinancialInstrumentAccount_95P_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 623, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 623, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceC_FinancialInstrumentAccount_95P_Type = MT541_SequenceC_FinancialInstrumentAccount_95P_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceC_FinancialInstrumentAccount_95P_Type', MT541_SequenceC_FinancialInstrumentAccount_95P_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceC_FinancialInstrumentAccount_95R_Type with content type SIMPLE
class MT541_SequenceC_FinancialInstrumentAccount_95R_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceC_FinancialInstrumentAccount_95R_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceC_FinancialInstrumentAccount_95R_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceC_FinancialInstrumentAccount_95R_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 632, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceC_FinancialInstrumentAccount_95R_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceC_FinancialInstrumentAccount_95R_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='95R')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 635, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 635, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceC_FinancialInstrumentAccount_95R_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 636, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 636, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceC_FinancialInstrumentAccount_95R_Type = MT541_SequenceC_FinancialInstrumentAccount_95R_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceC_FinancialInstrumentAccount_95R_Type', MT541_SequenceC_FinancialInstrumentAccount_95R_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceC_FinancialInstrumentAccount_97A_Type with content type SIMPLE
class MT541_SequenceC_FinancialInstrumentAccount_97A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceC_FinancialInstrumentAccount_97A_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceC_FinancialInstrumentAccount_97A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceC_FinancialInstrumentAccount_97A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 645, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceC_FinancialInstrumentAccount_97A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceC_FinancialInstrumentAccount_97A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='97A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 648, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 648, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceC_FinancialInstrumentAccount_97A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 649, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 649, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceC_FinancialInstrumentAccount_97A_Type = MT541_SequenceC_FinancialInstrumentAccount_97A_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceC_FinancialInstrumentAccount_97A_Type', MT541_SequenceC_FinancialInstrumentAccount_97A_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceC_FinancialInstrumentAccount_97B_Type with content type SIMPLE
class MT541_SequenceC_FinancialInstrumentAccount_97B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceC_FinancialInstrumentAccount_97B_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceC_FinancialInstrumentAccount_97B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceC_FinancialInstrumentAccount_97B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 658, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceC_FinancialInstrumentAccount_97B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceC_FinancialInstrumentAccount_97B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='97B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 661, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 661, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceC_FinancialInstrumentAccount_97B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 662, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 662, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceC_FinancialInstrumentAccount_97B_Type = MT541_SequenceC_FinancialInstrumentAccount_97B_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceC_FinancialInstrumentAccount_97B_Type', MT541_SequenceC_FinancialInstrumentAccount_97B_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceC_FinancialInstrumentAccount_97E_Type with content type SIMPLE
class MT541_SequenceC_FinancialInstrumentAccount_97E_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceC_FinancialInstrumentAccount_97E_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceC_FinancialInstrumentAccount_97E_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceC_FinancialInstrumentAccount_97E_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 671, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceC_FinancialInstrumentAccount_97E_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceC_FinancialInstrumentAccount_97E_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='97E')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 674, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 674, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceC_FinancialInstrumentAccount_97E_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 675, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 675, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceC_FinancialInstrumentAccount_97E_Type = MT541_SequenceC_FinancialInstrumentAccount_97E_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceC_FinancialInstrumentAccount_97E_Type', MT541_SequenceC_FinancialInstrumentAccount_97E_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceC_FinancialInstrumentAccount_94B_Type with content type SIMPLE
class MT541_SequenceC_FinancialInstrumentAccount_94B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceC_FinancialInstrumentAccount_94B_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceC_FinancialInstrumentAccount_94B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceC_FinancialInstrumentAccount_94B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 684, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceC_FinancialInstrumentAccount_94B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceC_FinancialInstrumentAccount_94B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='94B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 687, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 687, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceC_FinancialInstrumentAccount_94B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 688, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 688, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceC_FinancialInstrumentAccount_94B_Type = MT541_SequenceC_FinancialInstrumentAccount_94B_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceC_FinancialInstrumentAccount_94B_Type', MT541_SequenceC_FinancialInstrumentAccount_94B_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceC_FinancialInstrumentAccount_94C_Type with content type SIMPLE
class MT541_SequenceC_FinancialInstrumentAccount_94C_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceC_FinancialInstrumentAccount_94C_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceC_FinancialInstrumentAccount_94C_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceC_FinancialInstrumentAccount_94C_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 697, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceC_FinancialInstrumentAccount_94C_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceC_FinancialInstrumentAccount_94C_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='94C')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 700, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 700, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceC_FinancialInstrumentAccount_94C_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 701, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 701, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceC_FinancialInstrumentAccount_94C_Type = MT541_SequenceC_FinancialInstrumentAccount_94C_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceC_FinancialInstrumentAccount_94C_Type', MT541_SequenceC_FinancialInstrumentAccount_94C_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceC_FinancialInstrumentAccount_94F_Type with content type SIMPLE
class MT541_SequenceC_FinancialInstrumentAccount_94F_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceC_FinancialInstrumentAccount_94F_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceC_FinancialInstrumentAccount_94F_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceC_FinancialInstrumentAccount_94F_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 710, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceC_FinancialInstrumentAccount_94F_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceC_FinancialInstrumentAccount_94F_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='94F')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 713, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 713, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceC_FinancialInstrumentAccount_94F_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 714, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 714, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceC_FinancialInstrumentAccount_94F_Type = MT541_SequenceC_FinancialInstrumentAccount_94F_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceC_FinancialInstrumentAccount_94F_Type', MT541_SequenceC_FinancialInstrumentAccount_94F_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceC_FinancialInstrumentAccount_94L_Type with content type SIMPLE
class MT541_SequenceC_FinancialInstrumentAccount_94L_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceC_FinancialInstrumentAccount_94L_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceC_FinancialInstrumentAccount_94L_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceC_FinancialInstrumentAccount_94L_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 723, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceC_FinancialInstrumentAccount_94L_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceC_FinancialInstrumentAccount_94L_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='94L')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 726, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 726, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceC_FinancialInstrumentAccount_94L_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 727, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 727, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceC_FinancialInstrumentAccount_94L_Type = MT541_SequenceC_FinancialInstrumentAccount_94L_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceC_FinancialInstrumentAccount_94L_Type', MT541_SequenceC_FinancialInstrumentAccount_94L_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_13B_Type with content type SIMPLE
class MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_13B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_13B_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_13B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_13B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 736, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_13B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_13B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='13B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 739, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 739, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_13B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 740, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 740, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_13B_Type = MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_13B_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_13B_Type', MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_13B_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_36B_Type with content type SIMPLE
class MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_36B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_36B_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_36B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_36B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 749, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_36B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_36B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='36B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 752, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 752, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_36B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 753, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 753, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_36B_Type = MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_36B_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_36B_Type', MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_36B_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_98A_Type with content type SIMPLE
class MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_98A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_98A_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_98A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_98A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 762, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_98A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_98A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='98A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 765, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 765, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_98A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 766, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 766, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_98A_Type = MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_98A_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_98A_Type', MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_98A_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_98C_Type with content type SIMPLE
class MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_98C_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_98C_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_98C_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_98C_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 775, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_98C_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_98C_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='98C')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 778, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 778, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_98C_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 779, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 779, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_98C_Type = MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_98C_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_98C_Type', MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_98C_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_98E_Type with content type SIMPLE
class MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_98E_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_98E_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_98E_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_98E_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 788, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_98E_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_98E_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='98E')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 791, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 791, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_98E_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 792, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 792, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_98E_Type = MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_98E_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_98E_Type', MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_98E_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_90A_Type with content type SIMPLE
class MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_90A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_90A_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_90A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_90A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 801, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_90A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_90A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='90A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 804, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 804, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_90A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 805, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 805, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_90A_Type = MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_90A_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_90A_Type', MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_90A_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_90B_Type with content type SIMPLE
class MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_90B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_90B_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_90B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_90B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 814, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_90B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_90B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='90B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 817, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 817, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_90B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 818, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 818, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_90B_Type = MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_90B_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_90B_Type', MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_90B_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_22F_Type with content type SIMPLE
class MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_22F_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_22F_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_22F_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_22F_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 827, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_22F_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_22F_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='22F')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 830, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 830, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_22F_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 831, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 831, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_22F_Type = MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_22F_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_22F_Type', MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_22F_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceD_TwoLegTransactionDetails_98A_Type with content type SIMPLE
class MT541_SequenceD_TwoLegTransactionDetails_98A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceD_TwoLegTransactionDetails_98A_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceD_TwoLegTransactionDetails_98A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceD_TwoLegTransactionDetails_98A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 840, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceD_TwoLegTransactionDetails_98A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceD_TwoLegTransactionDetails_98A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='98A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 843, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 843, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceD_TwoLegTransactionDetails_98A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 844, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 844, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceD_TwoLegTransactionDetails_98A_Type = MT541_SequenceD_TwoLegTransactionDetails_98A_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceD_TwoLegTransactionDetails_98A_Type', MT541_SequenceD_TwoLegTransactionDetails_98A_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceD_TwoLegTransactionDetails_98B_Type with content type SIMPLE
class MT541_SequenceD_TwoLegTransactionDetails_98B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceD_TwoLegTransactionDetails_98B_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceD_TwoLegTransactionDetails_98B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceD_TwoLegTransactionDetails_98B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 853, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceD_TwoLegTransactionDetails_98B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceD_TwoLegTransactionDetails_98B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='98B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 856, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 856, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceD_TwoLegTransactionDetails_98B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 857, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 857, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceD_TwoLegTransactionDetails_98B_Type = MT541_SequenceD_TwoLegTransactionDetails_98B_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceD_TwoLegTransactionDetails_98B_Type', MT541_SequenceD_TwoLegTransactionDetails_98B_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceD_TwoLegTransactionDetails_98C_Type with content type SIMPLE
class MT541_SequenceD_TwoLegTransactionDetails_98C_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceD_TwoLegTransactionDetails_98C_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceD_TwoLegTransactionDetails_98C_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceD_TwoLegTransactionDetails_98C_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 866, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceD_TwoLegTransactionDetails_98C_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceD_TwoLegTransactionDetails_98C_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='98C')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 869, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 869, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceD_TwoLegTransactionDetails_98C_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 870, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 870, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceD_TwoLegTransactionDetails_98C_Type = MT541_SequenceD_TwoLegTransactionDetails_98C_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceD_TwoLegTransactionDetails_98C_Type', MT541_SequenceD_TwoLegTransactionDetails_98C_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceD_TwoLegTransactionDetails_22F_Type with content type SIMPLE
class MT541_SequenceD_TwoLegTransactionDetails_22F_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceD_TwoLegTransactionDetails_22F_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceD_TwoLegTransactionDetails_22F_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceD_TwoLegTransactionDetails_22F_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 879, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceD_TwoLegTransactionDetails_22F_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceD_TwoLegTransactionDetails_22F_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='22F')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 882, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 882, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceD_TwoLegTransactionDetails_22F_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 883, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 883, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceD_TwoLegTransactionDetails_22F_Type = MT541_SequenceD_TwoLegTransactionDetails_22F_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceD_TwoLegTransactionDetails_22F_Type', MT541_SequenceD_TwoLegTransactionDetails_22F_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceD_TwoLegTransactionDetails_20C_Type with content type SIMPLE
class MT541_SequenceD_TwoLegTransactionDetails_20C_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceD_TwoLegTransactionDetails_20C_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceD_TwoLegTransactionDetails_20C_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceD_TwoLegTransactionDetails_20C_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 892, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceD_TwoLegTransactionDetails_20C_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceD_TwoLegTransactionDetails_20C_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='20C')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 895, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 895, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceD_TwoLegTransactionDetails_20C_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 896, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 896, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceD_TwoLegTransactionDetails_20C_Type = MT541_SequenceD_TwoLegTransactionDetails_20C_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceD_TwoLegTransactionDetails_20C_Type', MT541_SequenceD_TwoLegTransactionDetails_20C_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceD_TwoLegTransactionDetails_92A_Type with content type SIMPLE
class MT541_SequenceD_TwoLegTransactionDetails_92A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceD_TwoLegTransactionDetails_92A_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceD_TwoLegTransactionDetails_92A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceD_TwoLegTransactionDetails_92A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 905, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceD_TwoLegTransactionDetails_92A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceD_TwoLegTransactionDetails_92A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='92A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 908, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 908, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceD_TwoLegTransactionDetails_92A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 909, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 909, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceD_TwoLegTransactionDetails_92A_Type = MT541_SequenceD_TwoLegTransactionDetails_92A_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceD_TwoLegTransactionDetails_92A_Type', MT541_SequenceD_TwoLegTransactionDetails_92A_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceD_TwoLegTransactionDetails_92C_Type with content type SIMPLE
class MT541_SequenceD_TwoLegTransactionDetails_92C_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceD_TwoLegTransactionDetails_92C_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceD_TwoLegTransactionDetails_92C_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceD_TwoLegTransactionDetails_92C_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 918, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceD_TwoLegTransactionDetails_92C_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceD_TwoLegTransactionDetails_92C_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='92C')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 921, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 921, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceD_TwoLegTransactionDetails_92C_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 922, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 922, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceD_TwoLegTransactionDetails_92C_Type = MT541_SequenceD_TwoLegTransactionDetails_92C_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceD_TwoLegTransactionDetails_92C_Type', MT541_SequenceD_TwoLegTransactionDetails_92C_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceD_TwoLegTransactionDetails_99B_Type with content type SIMPLE
class MT541_SequenceD_TwoLegTransactionDetails_99B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceD_TwoLegTransactionDetails_99B_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceD_TwoLegTransactionDetails_99B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceD_TwoLegTransactionDetails_99B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 931, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceD_TwoLegTransactionDetails_99B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceD_TwoLegTransactionDetails_99B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='99B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 934, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 934, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceD_TwoLegTransactionDetails_99B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 935, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 935, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceD_TwoLegTransactionDetails_99B_Type = MT541_SequenceD_TwoLegTransactionDetails_99B_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceD_TwoLegTransactionDetails_99B_Type', MT541_SequenceD_TwoLegTransactionDetails_99B_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceD_TwoLegTransactionDetails_19A_Type with content type SIMPLE
class MT541_SequenceD_TwoLegTransactionDetails_19A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceD_TwoLegTransactionDetails_19A_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceD_TwoLegTransactionDetails_19A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceD_TwoLegTransactionDetails_19A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 944, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceD_TwoLegTransactionDetails_19A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceD_TwoLegTransactionDetails_19A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='19A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 947, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 947, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceD_TwoLegTransactionDetails_19A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 948, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 948, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceD_TwoLegTransactionDetails_19A_Type = MT541_SequenceD_TwoLegTransactionDetails_19A_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceD_TwoLegTransactionDetails_19A_Type', MT541_SequenceD_TwoLegTransactionDetails_19A_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceD_TwoLegTransactionDetails_70C_Type with content type SIMPLE
class MT541_SequenceD_TwoLegTransactionDetails_70C_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceD_TwoLegTransactionDetails_70C_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceD_TwoLegTransactionDetails_70C_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceD_TwoLegTransactionDetails_70C_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 957, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceD_TwoLegTransactionDetails_70C_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceD_TwoLegTransactionDetails_70C_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='70C')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 960, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 960, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceD_TwoLegTransactionDetails_70C_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 961, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 961, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceD_TwoLegTransactionDetails_70C_Type = MT541_SequenceD_TwoLegTransactionDetails_70C_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceD_TwoLegTransactionDetails_70C_Type', MT541_SequenceD_TwoLegTransactionDetails_70C_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceE_SettlementDetails_22F_Type with content type SIMPLE
class MT541_SequenceE_SettlementDetails_22F_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceE_SettlementDetails_22F_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceE_SettlementDetails_22F_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceE_SettlementDetails_22F_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 970, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceE_SettlementDetails_22F_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceE_SettlementDetails_22F_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='22F')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 973, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 973, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceE_SettlementDetails_22F_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 974, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 974, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceE_SettlementDetails_22F_Type = MT541_SequenceE_SettlementDetails_22F_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceE_SettlementDetails_22F_Type', MT541_SequenceE_SettlementDetails_22F_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95C_Type with content type SIMPLE
class MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95C_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95C_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95C_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95C_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 983, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95C_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95C_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='95C')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 986, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 986, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95C_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 987, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 987, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95C_Type = MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95C_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95C_Type', MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95C_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95L_Type with content type SIMPLE
class MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95L_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95L_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95L_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95L_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 996, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95L_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95L_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='95L')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 999, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 999, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95L_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1000, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1000, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95L_Type = MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95L_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95L_Type', MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95L_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95P_Type with content type SIMPLE
class MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95P_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95P_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95P_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95P_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1009, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95P_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95P_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='95P')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1012, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1012, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95P_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1013, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1013, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95P_Type = MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95P_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95P_Type', MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95P_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95Q_Type with content type SIMPLE
class MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95Q_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95Q_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95Q_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95Q_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1022, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95Q_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95Q_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='95Q')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1025, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1025, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95Q_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1026, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1026, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95Q_Type = MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95Q_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95Q_Type', MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95Q_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95R_Type with content type SIMPLE
class MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95R_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95R_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95R_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95R_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1035, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95R_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95R_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='95R')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1038, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1038, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95R_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1039, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1039, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95R_Type = MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95R_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95R_Type', MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95R_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95S_Type with content type SIMPLE
class MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95S_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95S_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95S_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95S_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1048, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95S_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95S_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='95S')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1051, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1051, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95S_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1052, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1052, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95S_Type = MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95S_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95S_Type', MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95S_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_97A_Type with content type SIMPLE
class MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_97A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_97A_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_97A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_97A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1061, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_97A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_97A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='97A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1064, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1064, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_97A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1065, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1065, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_97A_Type = MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_97A_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_97A_Type', MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_97A_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_97B_Type with content type SIMPLE
class MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_97B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_97B_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_97B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_97B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1074, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_97B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_97B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='97B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1077, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1077, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_97B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1078, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1078, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_97B_Type = MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_97B_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_97B_Type', MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_97B_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_98A_Type with content type SIMPLE
class MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_98A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_98A_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_98A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_98A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1087, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_98A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_98A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='98A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1090, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1090, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_98A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1091, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1091, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_98A_Type = MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_98A_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_98A_Type', MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_98A_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_98C_Type with content type SIMPLE
class MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_98C_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_98C_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_98C_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_98C_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1100, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_98C_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_98C_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='98C')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1103, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1103, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_98C_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1104, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1104, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_98C_Type = MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_98C_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_98C_Type', MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_98C_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_20C_Type with content type SIMPLE
class MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_20C_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_20C_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_20C_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_20C_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1113, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_20C_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_20C_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='20C')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1116, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1116, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_20C_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1117, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1117, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_20C_Type = MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_20C_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_20C_Type', MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_20C_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_70C_Type with content type SIMPLE
class MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_70C_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_70C_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_70C_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_70C_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1126, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_70C_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_70C_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='70C')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1129, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1129, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_70C_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1130, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1130, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_70C_Type = MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_70C_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_70C_Type', MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_70C_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_70D_Type with content type SIMPLE
class MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_70D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_70D_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_70D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_70D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1139, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_70D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_70D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='70D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1142, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1142, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_70D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1143, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1143, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_70D_Type = MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_70D_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_70D_Type', MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_70D_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_70E_Type with content type SIMPLE
class MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_70E_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_70E_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_70E_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_70E_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1152, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_70E_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_70E_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='70E')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1155, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1155, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_70E_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1156, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1156, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_70E_Type = MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_70E_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_70E_Type', MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_70E_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95L_Type with content type SIMPLE
class MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95L_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95L_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95L_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95L_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1165, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95L_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95L_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='95L')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1168, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1168, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95L_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1169, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1169, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95L_Type = MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95L_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95L_Type', MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95L_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95P_Type with content type SIMPLE
class MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95P_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95P_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95P_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95P_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1178, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95P_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95P_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='95P')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1181, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1181, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95P_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1182, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1182, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95P_Type = MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95P_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95P_Type', MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95P_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95Q_Type with content type SIMPLE
class MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95Q_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95Q_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95Q_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95Q_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1191, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95Q_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95Q_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='95Q')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1194, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1194, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95Q_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1195, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1195, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95Q_Type = MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95Q_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95Q_Type', MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95Q_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95R_Type with content type SIMPLE
class MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95R_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95R_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95R_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95R_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1204, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95R_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95R_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='95R')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1207, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1207, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95R_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1208, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1208, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95R_Type = MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95R_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95R_Type', MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95R_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95S_Type with content type SIMPLE
class MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95S_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95S_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95S_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95S_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1217, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95S_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95S_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='95S')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1220, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1220, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95S_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1221, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1221, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95S_Type = MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95S_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95S_Type', MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95S_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_97A_Type with content type SIMPLE
class MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_97A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_97A_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_97A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_97A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1230, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_97A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_97A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='97A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1233, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1233, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_97A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1234, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1234, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_97A_Type = MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_97A_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_97A_Type', MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_97A_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_97E_Type with content type SIMPLE
class MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_97E_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_97E_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_97E_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_97E_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1243, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_97E_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_97E_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='97E')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1246, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1246, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_97E_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1247, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1247, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_97E_Type = MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_97E_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_97E_Type', MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_97E_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_70C_Type with content type SIMPLE
class MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_70C_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_70C_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_70C_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_70C_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1256, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_70C_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_70C_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='70C')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1259, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1259, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_70C_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1260, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1260, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_70C_Type = MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_70C_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_70C_Type', MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_70C_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_70E_Type with content type SIMPLE
class MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_70E_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_70E_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_70E_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_70E_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1269, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_70E_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_70E_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='70E')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1272, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1272, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_70E_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1273, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1273, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_70E_Type = MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_70E_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_70E_Type', MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_70E_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_17B_Type with content type SIMPLE
class MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_17B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_17B_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_17B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_17B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1282, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_17B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_17B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='17B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1285, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1285, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_17B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1286, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1286, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_17B_Type = MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_17B_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_17B_Type', MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_17B_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_19A_Type with content type SIMPLE
class MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_19A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_19A_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_19A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_19A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1295, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_19A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_19A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='19A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1298, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1298, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_19A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1299, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1299, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_19A_Type = MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_19A_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_19A_Type', MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_19A_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_98A_Type with content type SIMPLE
class MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_98A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_98A_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_98A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_98A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1308, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_98A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_98A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='98A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1311, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1311, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_98A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1312, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1312, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_98A_Type = MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_98A_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_98A_Type', MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_98A_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_98C_Type with content type SIMPLE
class MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_98C_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_98C_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_98C_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_98C_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1321, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_98C_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_98C_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='98C')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1324, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1324, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_98C_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1325, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1325, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_98C_Type = MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_98C_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_98C_Type', MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_98C_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_92B_Type with content type SIMPLE
class MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_92B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_92B_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_92B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_92B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1334, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_92B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_92B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='92B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1337, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1337, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_92B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1338, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1338, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_92B_Type = MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_92B_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_92B_Type', MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_92B_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceF_OtherParties_95C_Type with content type SIMPLE
class MT541_SequenceF_OtherParties_95C_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceF_OtherParties_95C_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceF_OtherParties_95C_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceF_OtherParties_95C_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1347, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceF_OtherParties_95C_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceF_OtherParties_95C_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='95C')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1350, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1350, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceF_OtherParties_95C_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1351, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1351, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceF_OtherParties_95C_Type = MT541_SequenceF_OtherParties_95C_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceF_OtherParties_95C_Type', MT541_SequenceF_OtherParties_95C_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceF_OtherParties_95L_Type with content type SIMPLE
class MT541_SequenceF_OtherParties_95L_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceF_OtherParties_95L_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceF_OtherParties_95L_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceF_OtherParties_95L_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1360, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceF_OtherParties_95L_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceF_OtherParties_95L_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='95L')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1363, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1363, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceF_OtherParties_95L_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1364, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1364, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceF_OtherParties_95L_Type = MT541_SequenceF_OtherParties_95L_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceF_OtherParties_95L_Type', MT541_SequenceF_OtherParties_95L_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceF_OtherParties_95P_Type with content type SIMPLE
class MT541_SequenceF_OtherParties_95P_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceF_OtherParties_95P_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceF_OtherParties_95P_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceF_OtherParties_95P_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1373, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceF_OtherParties_95P_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceF_OtherParties_95P_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='95P')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1376, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1376, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceF_OtherParties_95P_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1377, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1377, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceF_OtherParties_95P_Type = MT541_SequenceF_OtherParties_95P_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceF_OtherParties_95P_Type', MT541_SequenceF_OtherParties_95P_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceF_OtherParties_95Q_Type with content type SIMPLE
class MT541_SequenceF_OtherParties_95Q_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceF_OtherParties_95Q_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceF_OtherParties_95Q_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceF_OtherParties_95Q_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1386, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceF_OtherParties_95Q_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceF_OtherParties_95Q_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='95Q')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1389, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1389, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceF_OtherParties_95Q_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1390, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1390, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceF_OtherParties_95Q_Type = MT541_SequenceF_OtherParties_95Q_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceF_OtherParties_95Q_Type', MT541_SequenceF_OtherParties_95Q_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceF_OtherParties_95R_Type with content type SIMPLE
class MT541_SequenceF_OtherParties_95R_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceF_OtherParties_95R_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceF_OtherParties_95R_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceF_OtherParties_95R_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1399, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceF_OtherParties_95R_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceF_OtherParties_95R_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='95R')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1402, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1402, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceF_OtherParties_95R_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1403, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1403, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceF_OtherParties_95R_Type = MT541_SequenceF_OtherParties_95R_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceF_OtherParties_95R_Type', MT541_SequenceF_OtherParties_95R_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceF_OtherParties_95S_Type with content type SIMPLE
class MT541_SequenceF_OtherParties_95S_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceF_OtherParties_95S_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceF_OtherParties_95S_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceF_OtherParties_95S_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1412, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceF_OtherParties_95S_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceF_OtherParties_95S_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='95S')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1415, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1415, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceF_OtherParties_95S_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1416, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1416, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceF_OtherParties_95S_Type = MT541_SequenceF_OtherParties_95S_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceF_OtherParties_95S_Type', MT541_SequenceF_OtherParties_95S_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceF_OtherParties_97A_Type with content type SIMPLE
class MT541_SequenceF_OtherParties_97A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceF_OtherParties_97A_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceF_OtherParties_97A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceF_OtherParties_97A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1425, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceF_OtherParties_97A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceF_OtherParties_97A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='97A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1428, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1428, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceF_OtherParties_97A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1429, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1429, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceF_OtherParties_97A_Type = MT541_SequenceF_OtherParties_97A_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceF_OtherParties_97A_Type', MT541_SequenceF_OtherParties_97A_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceF_OtherParties_70C_Type with content type SIMPLE
class MT541_SequenceF_OtherParties_70C_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceF_OtherParties_70C_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceF_OtherParties_70C_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceF_OtherParties_70C_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1438, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceF_OtherParties_70C_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceF_OtherParties_70C_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='70C')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1441, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1441, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceF_OtherParties_70C_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1442, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1442, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceF_OtherParties_70C_Type = MT541_SequenceF_OtherParties_70C_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceF_OtherParties_70C_Type', MT541_SequenceF_OtherParties_70C_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceF_OtherParties_70D_Type with content type SIMPLE
class MT541_SequenceF_OtherParties_70D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceF_OtherParties_70D_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceF_OtherParties_70D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceF_OtherParties_70D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1451, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceF_OtherParties_70D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceF_OtherParties_70D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='70D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1454, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1454, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceF_OtherParties_70D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1455, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1455, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceF_OtherParties_70D_Type = MT541_SequenceF_OtherParties_70D_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceF_OtherParties_70D_Type', MT541_SequenceF_OtherParties_70D_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceF_OtherParties_70E_Type with content type SIMPLE
class MT541_SequenceF_OtherParties_70E_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceF_OtherParties_70E_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceF_OtherParties_70E_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceF_OtherParties_70E_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1464, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceF_OtherParties_70E_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceF_OtherParties_70E_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='70E')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1467, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1467, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceF_OtherParties_70E_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1468, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1468, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceF_OtherParties_70E_Type = MT541_SequenceF_OtherParties_70E_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceF_OtherParties_70E_Type', MT541_SequenceF_OtherParties_70E_Type)


# Complex type {http://www.w3schools.com}MT541_SequenceF_OtherParties_20C_Type with content type SIMPLE
class MT541_SequenceF_OtherParties_20C_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT541_SequenceF_OtherParties_20C_Type with content type SIMPLE"""
    _TypeDefinition = MT541_SequenceF_OtherParties_20C_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT541_SequenceF_OtherParties_20C_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1477, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT541_SequenceF_OtherParties_20C_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT541_SequenceF_OtherParties_20C_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='20C')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1480, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1480, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT541_SequenceF_OtherParties_20C_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1481, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1481, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT541_SequenceF_OtherParties_20C_Type = MT541_SequenceF_OtherParties_20C_Type
Namespace.addCategoryObject('typeBinding', 'MT541_SequenceF_OtherParties_20C_Type', MT541_SequenceF_OtherParties_20C_Type)


MT541 = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'MT541'), CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1741, 1))
Namespace.addCategoryObject('elementBinding', MT541.name().localName(), MT541)



MT541_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SendersMessageReference'), MT541_SequenceA_GeneralInformation_20C_Type, scope=MT541_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1487, 3)))

MT541_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'FunctionOfMessage'), MT541_SequenceA_GeneralInformation_23G_Type, scope=MT541_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1488, 3)))

MT541_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PreparationDateTime_A'), MT541_SequenceA_GeneralInformation_98A_Type, scope=MT541_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1490, 4)))

MT541_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PreparationDateTime_C'), MT541_SequenceA_GeneralInformation_98C_Type, scope=MT541_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1491, 4)))

MT541_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PreparationDateTime_E'), MT541_SequenceA_GeneralInformation_98E_Type, scope=MT541_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1492, 4)))

MT541_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'NumberCount'), MT541_SequenceA_GeneralInformation_99B_Type, scope=MT541_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1494, 3)))

MT541_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SubSequenceA1_Linkages'), MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages, scope=MT541_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1495, 3)))

def _BuildAutomaton ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1489, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1490, 4))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1491, 4))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1492, 4))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1494, 3))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1495, 3))
    counters.add(cc_5)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SendersMessageReference')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1487, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'FunctionOfMessage')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1488, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PreparationDateTime_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1490, 4))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PreparationDateTime_C')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1491, 4))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PreparationDateTime_E')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1492, 4))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'NumberCount')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1494, 3))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_5, False))
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SubSequenceA1_Linkages')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1495, 3))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
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
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_4, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_4, False) ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_5, True) ]))
    st_6._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
MT541_SequenceA_GeneralInformation._Automaton = _BuildAutomaton()




MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'LinkageTypeIndicator'), MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_22F_Type, scope=MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1503, 3)))

MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'LinkedMessage_A'), MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13A_Type, scope=MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1505, 4)))

MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'LinkedMessage_B'), MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13B_Type, scope=MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1506, 4)))

MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Reference_C'), MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20C_Type, scope=MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1509, 4)))

MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Reference_U'), MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20U_Type, scope=MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1510, 4)))

MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'QuantityOfFinancialInstrument'), MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages_36B_Type, scope=MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1512, 3)))

def _BuildAutomaton_ ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_
    del _BuildAutomaton_
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1503, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1504, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1505, 4))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1506, 4))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1508, 3))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1509, 4))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1510, 4))
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1512, 3))
    counters.add(cc_7)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'LinkageTypeIndicator')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1503, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'LinkedMessage_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1505, 4))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'LinkedMessage_B')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1506, 4))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    final_update.add(fac.UpdateInstruction(cc_5, False))
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Reference_C')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1509, 4))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    final_update.add(fac.UpdateInstruction(cc_6, False))
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Reference_U')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1510, 4))
    st_4 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_7, False))
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'QuantityOfFinancialInstrument')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1512, 3))
    st_5 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
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
        fac.UpdateInstruction(cc_1, False),
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, False),
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_5, [
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
        fac.UpdateInstruction(cc_1, False),
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, False),
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_1, False),
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
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_6, False) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_7, True) ]))
    st_5._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
MT541_SequenceA_GeneralInformation_SubSequenceA1_Linkages._Automaton = _BuildAutomaton_()




MT541_SequenceB_TradeDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Place_B'), MT541_SequenceB_TradeDetails_94B_Type, scope=MT541_SequenceB_TradeDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1521, 4)))

MT541_SequenceB_TradeDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Place_H'), MT541_SequenceB_TradeDetails_94H_Type, scope=MT541_SequenceB_TradeDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1522, 4)))

MT541_SequenceB_TradeDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Place_L'), MT541_SequenceB_TradeDetails_94L_Type, scope=MT541_SequenceB_TradeDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1523, 4)))

MT541_SequenceB_TradeDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DateTime_A'), MT541_SequenceB_TradeDetails_98A_Type, scope=MT541_SequenceB_TradeDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1526, 4)))

MT541_SequenceB_TradeDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DateTime_B'), MT541_SequenceB_TradeDetails_98B_Type, scope=MT541_SequenceB_TradeDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1527, 4)))

MT541_SequenceB_TradeDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DateTime_C'), MT541_SequenceB_TradeDetails_98C_Type, scope=MT541_SequenceB_TradeDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1528, 4)))

MT541_SequenceB_TradeDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DateTime_E'), MT541_SequenceB_TradeDetails_98E_Type, scope=MT541_SequenceB_TradeDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1529, 4)))

MT541_SequenceB_TradeDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DealPrice_A'), MT541_SequenceB_TradeDetails_90A_Type, scope=MT541_SequenceB_TradeDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1532, 4)))

MT541_SequenceB_TradeDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DealPrice_B'), MT541_SequenceB_TradeDetails_90B_Type, scope=MT541_SequenceB_TradeDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1533, 4)))

MT541_SequenceB_TradeDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'NumberOfDaysAccrued'), MT541_SequenceB_TradeDetails_99A_Type, scope=MT541_SequenceB_TradeDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1535, 3)))

MT541_SequenceB_TradeDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'IdentificationOfFinancialInstrument'), MT541_SequenceB_TradeDetails_35B_Type, scope=MT541_SequenceB_TradeDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1536, 3)))

MT541_SequenceB_TradeDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SubSequenceB1_FinancialInstrumentAttributes'), MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes, scope=MT541_SequenceB_TradeDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1537, 3)))

MT541_SequenceB_TradeDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Indicator'), MT541_SequenceB_TradeDetails_22F_Type, scope=MT541_SequenceB_TradeDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1538, 3)))

MT541_SequenceB_TradeDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'CurrencyToSell'), MT541_SequenceB_TradeDetails_11A_Type, scope=MT541_SequenceB_TradeDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1539, 3)))

MT541_SequenceB_TradeDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Status'), MT541_SequenceB_TradeDetails_25D_Type, scope=MT541_SequenceB_TradeDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1540, 3)))

MT541_SequenceB_TradeDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Narrative'), MT541_SequenceB_TradeDetails_70E_Type, scope=MT541_SequenceB_TradeDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1541, 3)))

def _BuildAutomaton_2 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_2
    del _BuildAutomaton_2
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1520, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1521, 4))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1522, 4))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1523, 4))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1531, 3))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1532, 4))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1533, 4))
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1535, 3))
    counters.add(cc_7)
    cc_8 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1537, 3))
    counters.add(cc_8)
    cc_9 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1538, 3))
    counters.add(cc_9)
    cc_10 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1539, 3))
    counters.add(cc_10)
    cc_11 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1540, 3))
    counters.add(cc_11)
    cc_12 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1541, 3))
    counters.add(cc_12)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceB_TradeDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Place_B')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1521, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceB_TradeDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Place_H')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1522, 4))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceB_TradeDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Place_L')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1523, 4))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceB_TradeDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'DateTime_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1526, 4))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceB_TradeDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'DateTime_B')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1527, 4))
    st_4 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceB_TradeDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'DateTime_C')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1528, 4))
    st_5 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceB_TradeDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'DateTime_E')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1529, 4))
    st_6 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceB_TradeDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'DealPrice_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1532, 4))
    st_7 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceB_TradeDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'DealPrice_B')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1533, 4))
    st_8 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceB_TradeDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'NumberOfDaysAccrued')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1535, 3))
    st_9 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceB_TradeDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'IdentificationOfFinancialInstrument')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1536, 3))
    st_10 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_10)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_8, False))
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceB_TradeDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SubSequenceB1_FinancialInstrumentAttributes')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1537, 3))
    st_11 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_11)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_9, False))
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceB_TradeDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Indicator')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1538, 3))
    st_12 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_12)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_10, False))
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceB_TradeDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'CurrencyToSell')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1539, 3))
    st_13 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_13)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_11, False))
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceB_TradeDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Status')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1540, 3))
    st_14 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_14)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_12, False))
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceB_TradeDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Narrative')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1541, 3))
    st_15 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_15)
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
    st_2._set_transitionSet(transitions)
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
    st_3._set_transitionSet(transitions)
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
    st_4._set_transitionSet(transitions)
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
    st_5._set_transitionSet(transitions)
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
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_4, True),
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_5, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_4, True),
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_5, False) ]))
    st_7._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_4, True),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_4, True),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_6, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_4, False),
        fac.UpdateInstruction(cc_6, False) ]))
    st_8._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_7, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_7, False) ]))
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
    st_10._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_8, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_8, False) ]))
    st_11._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_9, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_9, False) ]))
    st_12._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_10, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_10, False) ]))
    st_13._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_11, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_11, False) ]))
    st_14._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_12, True) ]))
    st_15._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
MT541_SequenceB_TradeDetails._Automaton = _BuildAutomaton_2()




MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PlaceOfListing'), MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_94B_Type, scope=MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1549, 3)))

MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Indicator'), MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_22F_Type, scope=MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1550, 3)))

MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'TypeOfFinancialInstrument_A'), MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_12A_Type, scope=MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1552, 4)))

MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'TypeOfFinancialInstrument_B'), MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_12B_Type, scope=MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1553, 4)))

MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'TypeOfFinancialInstrument_C'), MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_12C_Type, scope=MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1554, 4)))

MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'CurrencyOfDenomination'), MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_11A_Type, scope=MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1556, 3)))

MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Date'), MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_98A_Type, scope=MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1557, 3)))

MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Rate'), MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_92A_Type, scope=MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1558, 3)))

MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'NumberIdentification_A'), MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_13A_Type, scope=MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1560, 4)))

MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'NumberIdentification_B'), MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_13B_Type, scope=MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1561, 4)))

MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Flag'), MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_17B_Type, scope=MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1563, 3)))

MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Price_A'), MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_90A_Type, scope=MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1565, 4)))

MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Price_B'), MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_90B_Type, scope=MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1566, 4)))

MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'QuantityOfFinancialInstrument'), MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_36B_Type, scope=MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1568, 3)))

MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'IdentificationOfFinancialInstrument'), MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_35B_Type, scope=MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1569, 3)))

MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'FinancialInstrumentAttributeNarrative'), MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes_70E_Type, scope=MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1570, 3)))

def _BuildAutomaton_3 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_3
    del _BuildAutomaton_3
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1549, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1550, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1551, 3))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1552, 4))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1553, 4))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1554, 4))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1556, 3))
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1557, 3))
    counters.add(cc_7)
    cc_8 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1558, 3))
    counters.add(cc_8)
    cc_9 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1559, 3))
    counters.add(cc_9)
    cc_10 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1560, 4))
    counters.add(cc_10)
    cc_11 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1561, 4))
    counters.add(cc_11)
    cc_12 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1563, 3))
    counters.add(cc_12)
    cc_13 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1564, 3))
    counters.add(cc_13)
    cc_14 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1565, 4))
    counters.add(cc_14)
    cc_15 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1566, 4))
    counters.add(cc_15)
    cc_16 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1568, 3))
    counters.add(cc_16)
    cc_17 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1569, 3))
    counters.add(cc_17)
    cc_18 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1570, 3))
    counters.add(cc_18)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PlaceOfListing')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1549, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Indicator')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1550, 3))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'TypeOfFinancialInstrument_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1552, 4))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'TypeOfFinancialInstrument_B')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1553, 4))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    final_update.add(fac.UpdateInstruction(cc_5, False))
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'TypeOfFinancialInstrument_C')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1554, 4))
    st_4 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_6, False))
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'CurrencyOfDenomination')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1556, 3))
    st_5 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_7, False))
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Date')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1557, 3))
    st_6 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_8, False))
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Rate')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1558, 3))
    st_7 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_9, False))
    final_update.add(fac.UpdateInstruction(cc_10, False))
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'NumberIdentification_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1560, 4))
    st_8 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_9, False))
    final_update.add(fac.UpdateInstruction(cc_11, False))
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'NumberIdentification_B')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1561, 4))
    st_9 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_12, False))
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Flag')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1563, 3))
    st_10 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_10)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_13, False))
    final_update.add(fac.UpdateInstruction(cc_14, False))
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Price_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1565, 4))
    st_11 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_11)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_13, False))
    final_update.add(fac.UpdateInstruction(cc_15, False))
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Price_B')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1566, 4))
    st_12 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_12)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_16, False))
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'QuantityOfFinancialInstrument')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1568, 3))
    st_13 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_13)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_17, False))
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'IdentificationOfFinancialInstrument')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1569, 3))
    st_14 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_14)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_18, False))
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'FinancialInstrumentAttributeNarrative')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1570, 3))
    st_15 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_15)
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
        fac.UpdateInstruction(cc_2, False),
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
        fac.UpdateInstruction(cc_2, False),
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
        fac.UpdateInstruction(cc_2, False),
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
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_6, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_6, False) ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_7, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_7, False) ]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_8, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_8, False) ]))
    st_7._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_9, True),
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_10, True) ]))
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
    st_8._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_9, True),
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_9, True),
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_11, True) ]))
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
    st_9._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_12, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_12, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_12, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_12, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_12, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_12, False) ]))
    st_10._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_13, True),
        fac.UpdateInstruction(cc_14, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_14, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_13, True),
        fac.UpdateInstruction(cc_14, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_13, False),
        fac.UpdateInstruction(cc_14, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_13, False),
        fac.UpdateInstruction(cc_14, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_13, False),
        fac.UpdateInstruction(cc_14, False) ]))
    st_11._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_13, True),
        fac.UpdateInstruction(cc_15, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_13, True),
        fac.UpdateInstruction(cc_15, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_15, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_13, False),
        fac.UpdateInstruction(cc_15, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_13, False),
        fac.UpdateInstruction(cc_15, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_13, False),
        fac.UpdateInstruction(cc_15, False) ]))
    st_12._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_16, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_16, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_16, False) ]))
    st_13._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_17, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_17, False) ]))
    st_14._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_18, True) ]))
    st_15._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
MT541_SequenceB_TradeDetails_SubSequenceB1_FinancialInstrumentAttributes._Automaton = _BuildAutomaton_3()




MT541_SequenceC_FinancialInstrumentAccount._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'QuantityOfFinancialInstrumentToBeSettled'), MT541_SequenceC_FinancialInstrumentAccount_36B_Type, scope=MT541_SequenceC_FinancialInstrumentAccount, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1578, 3)))

MT541_SequenceC_FinancialInstrumentAccount._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DenominationChoice'), MT541_SequenceC_FinancialInstrumentAccount_70D_Type, scope=MT541_SequenceC_FinancialInstrumentAccount, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1579, 3)))

MT541_SequenceC_FinancialInstrumentAccount._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'CertificateNumber'), MT541_SequenceC_FinancialInstrumentAccount_13B_Type, scope=MT541_SequenceC_FinancialInstrumentAccount, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1580, 3)))

MT541_SequenceC_FinancialInstrumentAccount._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Party_L'), MT541_SequenceC_FinancialInstrumentAccount_95L_Type, scope=MT541_SequenceC_FinancialInstrumentAccount, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1582, 4)))

MT541_SequenceC_FinancialInstrumentAccount._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Party_P'), MT541_SequenceC_FinancialInstrumentAccount_95P_Type, scope=MT541_SequenceC_FinancialInstrumentAccount, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1583, 4)))

MT541_SequenceC_FinancialInstrumentAccount._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Party_R'), MT541_SequenceC_FinancialInstrumentAccount_95R_Type, scope=MT541_SequenceC_FinancialInstrumentAccount, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1584, 4)))

MT541_SequenceC_FinancialInstrumentAccount._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Account_A'), MT541_SequenceC_FinancialInstrumentAccount_97A_Type, scope=MT541_SequenceC_FinancialInstrumentAccount, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1587, 4)))

MT541_SequenceC_FinancialInstrumentAccount._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Account_B'), MT541_SequenceC_FinancialInstrumentAccount_97B_Type, scope=MT541_SequenceC_FinancialInstrumentAccount, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1588, 4)))

MT541_SequenceC_FinancialInstrumentAccount._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Account_E'), MT541_SequenceC_FinancialInstrumentAccount_97E_Type, scope=MT541_SequenceC_FinancialInstrumentAccount, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1589, 4)))

MT541_SequenceC_FinancialInstrumentAccount._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PlaceOfSafekeeping_B'), MT541_SequenceC_FinancialInstrumentAccount_94B_Type, scope=MT541_SequenceC_FinancialInstrumentAccount, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1592, 4)))

MT541_SequenceC_FinancialInstrumentAccount._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PlaceOfSafekeeping_C'), MT541_SequenceC_FinancialInstrumentAccount_94C_Type, scope=MT541_SequenceC_FinancialInstrumentAccount, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1593, 4)))

MT541_SequenceC_FinancialInstrumentAccount._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PlaceOfSafekeeping_F'), MT541_SequenceC_FinancialInstrumentAccount_94F_Type, scope=MT541_SequenceC_FinancialInstrumentAccount, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1594, 4)))

MT541_SequenceC_FinancialInstrumentAccount._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PlaceOfSafekeeping_L'), MT541_SequenceC_FinancialInstrumentAccount_94L_Type, scope=MT541_SequenceC_FinancialInstrumentAccount, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1595, 4)))

MT541_SequenceC_FinancialInstrumentAccount._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SubSequenceC1_QuantityBreakdown'), MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown, scope=MT541_SequenceC_FinancialInstrumentAccount, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1597, 3)))

def _BuildAutomaton_4 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_4
    del _BuildAutomaton_4
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1579, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1580, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1581, 3))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1582, 4))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1583, 4))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1584, 4))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1591, 3))
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1592, 4))
    counters.add(cc_7)
    cc_8 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1593, 4))
    counters.add(cc_8)
    cc_9 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1594, 4))
    counters.add(cc_9)
    cc_10 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1595, 4))
    counters.add(cc_10)
    cc_11 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1597, 3))
    counters.add(cc_11)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceC_FinancialInstrumentAccount._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'QuantityOfFinancialInstrumentToBeSettled')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1578, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceC_FinancialInstrumentAccount._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'DenominationChoice')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1579, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceC_FinancialInstrumentAccount._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'CertificateNumber')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1580, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceC_FinancialInstrumentAccount._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Party_L')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1582, 4))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceC_FinancialInstrumentAccount._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Party_P')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1583, 4))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceC_FinancialInstrumentAccount._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Party_R')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1584, 4))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceC_FinancialInstrumentAccount._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Account_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1587, 4))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceC_FinancialInstrumentAccount._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Account_B')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1588, 4))
    st_7 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceC_FinancialInstrumentAccount._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Account_E')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1589, 4))
    st_8 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_6, False))
    final_update.add(fac.UpdateInstruction(cc_7, False))
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceC_FinancialInstrumentAccount._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PlaceOfSafekeeping_B')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1592, 4))
    st_9 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_6, False))
    final_update.add(fac.UpdateInstruction(cc_8, False))
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceC_FinancialInstrumentAccount._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PlaceOfSafekeeping_C')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1593, 4))
    st_10 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_10)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_6, False))
    final_update.add(fac.UpdateInstruction(cc_9, False))
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceC_FinancialInstrumentAccount._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PlaceOfSafekeeping_F')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1594, 4))
    st_11 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_11)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_6, False))
    final_update.add(fac.UpdateInstruction(cc_10, False))
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceC_FinancialInstrumentAccount._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PlaceOfSafekeeping_L')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1595, 4))
    st_12 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_12)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_11, False))
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceC_FinancialInstrumentAccount._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SubSequenceC1_QuantityBreakdown')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1597, 3))
    st_13 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_13)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
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
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
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
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, True) ]))
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
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, True),
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_3, True) ]))
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
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, True),
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_2, True),
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_4, True) ]))
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
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, True),
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_2, True),
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_2, True),
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_5, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_2, False),
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_2, False),
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_2, False),
        fac.UpdateInstruction(cc_5, False) ]))
    st_5._set_transitionSet(transitions)
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
    transitions.append(fac.Transition(st_11, [
         ]))
    transitions.append(fac.Transition(st_12, [
         ]))
    transitions.append(fac.Transition(st_13, [
         ]))
    st_6._set_transitionSet(transitions)
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
    transitions.append(fac.Transition(st_11, [
         ]))
    transitions.append(fac.Transition(st_12, [
         ]))
    transitions.append(fac.Transition(st_13, [
         ]))
    st_7._set_transitionSet(transitions)
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
    transitions.append(fac.Transition(st_11, [
         ]))
    transitions.append(fac.Transition(st_12, [
         ]))
    transitions.append(fac.Transition(st_13, [
         ]))
    st_8._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_6, True),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_7, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_6, True),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_6, True),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_6, True),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_6, False),
        fac.UpdateInstruction(cc_7, False) ]))
    st_9._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_6, True),
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_6, True),
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_8, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_6, True),
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_6, True),
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_6, False),
        fac.UpdateInstruction(cc_8, False) ]))
    st_10._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_6, True),
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_6, True),
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_6, True),
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_9, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_6, True),
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_6, False),
        fac.UpdateInstruction(cc_9, False) ]))
    st_11._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_6, True),
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_6, True),
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_6, True),
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_6, True),
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_10, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_6, False),
        fac.UpdateInstruction(cc_10, False) ]))
    st_12._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_11, True) ]))
    st_13._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
MT541_SequenceC_FinancialInstrumentAccount._Automaton = _BuildAutomaton_4()




MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'LotNumber'), MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_13B_Type, scope=MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1605, 3)))

MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'QuantityOfFinancialInstrumentInTheLot'), MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_36B_Type, scope=MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1606, 3)))

MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'LotDateTime_A'), MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_98A_Type, scope=MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1608, 4)))

MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'LotDateTime_C'), MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_98C_Type, scope=MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1609, 4)))

MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'LotDateTime_E'), MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_98E_Type, scope=MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1610, 4)))

MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'BookLotPrice_A'), MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_90A_Type, scope=MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1613, 4)))

MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'BookLotPrice_B'), MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_90B_Type, scope=MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1614, 4)))

MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'TypeOfPriceIndicator'), MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown_22F_Type, scope=MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1616, 3)))

def _BuildAutomaton_5 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_5
    del _BuildAutomaton_5
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1605, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1606, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1607, 3))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1608, 4))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1609, 4))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1610, 4))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1612, 3))
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1613, 4))
    counters.add(cc_7)
    cc_8 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1614, 4))
    counters.add(cc_8)
    cc_9 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1616, 3))
    counters.add(cc_9)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'LotNumber')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1605, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'QuantityOfFinancialInstrumentInTheLot')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1606, 3))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'LotDateTime_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1608, 4))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'LotDateTime_C')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1609, 4))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    final_update.add(fac.UpdateInstruction(cc_5, False))
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'LotDateTime_E')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1610, 4))
    st_4 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_6, False))
    final_update.add(fac.UpdateInstruction(cc_7, False))
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'BookLotPrice_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1613, 4))
    st_5 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_6, False))
    final_update.add(fac.UpdateInstruction(cc_8, False))
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'BookLotPrice_B')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1614, 4))
    st_6 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_9, False))
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'TypeOfPriceIndicator')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1616, 3))
    st_7 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
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
        fac.UpdateInstruction(cc_2, False),
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_2, False),
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_7, [
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
        fac.UpdateInstruction(cc_2, False),
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_2, False),
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_7, [
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
        fac.UpdateInstruction(cc_2, False),
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_2, False),
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_2, False),
        fac.UpdateInstruction(cc_5, False) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_6, True),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_7, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_6, True),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_6, False),
        fac.UpdateInstruction(cc_7, False) ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_6, True),
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_6, True),
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_8, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_6, False),
        fac.UpdateInstruction(cc_8, False) ]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_9, True) ]))
    st_7._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
MT541_SequenceC_FinancialInstrumentAccount_SubSequenceC1_QuantityBreakdown._Automaton = _BuildAutomaton_5()




MT541_SequenceD_TwoLegTransactionDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DateTime_A'), MT541_SequenceD_TwoLegTransactionDetails_98A_Type, scope=MT541_SequenceD_TwoLegTransactionDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1625, 4)))

MT541_SequenceD_TwoLegTransactionDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DateTime_B'), MT541_SequenceD_TwoLegTransactionDetails_98B_Type, scope=MT541_SequenceD_TwoLegTransactionDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1626, 4)))

MT541_SequenceD_TwoLegTransactionDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DateTime_C'), MT541_SequenceD_TwoLegTransactionDetails_98C_Type, scope=MT541_SequenceD_TwoLegTransactionDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1627, 4)))

MT541_SequenceD_TwoLegTransactionDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Indicator'), MT541_SequenceD_TwoLegTransactionDetails_22F_Type, scope=MT541_SequenceD_TwoLegTransactionDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1629, 3)))

MT541_SequenceD_TwoLegTransactionDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Reference'), MT541_SequenceD_TwoLegTransactionDetails_20C_Type, scope=MT541_SequenceD_TwoLegTransactionDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1630, 3)))

MT541_SequenceD_TwoLegTransactionDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Rate_A'), MT541_SequenceD_TwoLegTransactionDetails_92A_Type, scope=MT541_SequenceD_TwoLegTransactionDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1632, 4)))

MT541_SequenceD_TwoLegTransactionDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Rate_C'), MT541_SequenceD_TwoLegTransactionDetails_92C_Type, scope=MT541_SequenceD_TwoLegTransactionDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1633, 4)))

MT541_SequenceD_TwoLegTransactionDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'NumberCount'), MT541_SequenceD_TwoLegTransactionDetails_99B_Type, scope=MT541_SequenceD_TwoLegTransactionDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1635, 3)))

MT541_SequenceD_TwoLegTransactionDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Amount'), MT541_SequenceD_TwoLegTransactionDetails_19A_Type, scope=MT541_SequenceD_TwoLegTransactionDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1636, 3)))

MT541_SequenceD_TwoLegTransactionDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SecondLegNarrative'), MT541_SequenceD_TwoLegTransactionDetails_70C_Type, scope=MT541_SequenceD_TwoLegTransactionDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1637, 3)))

def _BuildAutomaton_6 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_6
    del _BuildAutomaton_6
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1624, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1625, 4))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1626, 4))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1627, 4))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1629, 3))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1630, 3))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1631, 3))
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1632, 4))
    counters.add(cc_7)
    cc_8 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1633, 4))
    counters.add(cc_8)
    cc_9 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1635, 3))
    counters.add(cc_9)
    cc_10 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1636, 3))
    counters.add(cc_10)
    cc_11 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1637, 3))
    counters.add(cc_11)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceD_TwoLegTransactionDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'DateTime_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1625, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceD_TwoLegTransactionDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'DateTime_B')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1626, 4))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceD_TwoLegTransactionDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'DateTime_C')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1627, 4))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceD_TwoLegTransactionDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Indicator')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1629, 3))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_5, False))
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceD_TwoLegTransactionDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Reference')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1630, 3))
    st_4 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_6, False))
    final_update.add(fac.UpdateInstruction(cc_7, False))
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceD_TwoLegTransactionDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Rate_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1632, 4))
    st_5 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_6, False))
    final_update.add(fac.UpdateInstruction(cc_8, False))
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceD_TwoLegTransactionDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Rate_C')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1633, 4))
    st_6 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_9, False))
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceD_TwoLegTransactionDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'NumberCount')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1635, 3))
    st_7 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_10, False))
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceD_TwoLegTransactionDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Amount')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1636, 3))
    st_8 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_11, False))
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceD_TwoLegTransactionDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SecondLegNarrative')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1637, 3))
    st_9 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
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
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_4, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_4, False) ]))
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
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_5, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_5, False) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_6, True),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_7, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_6, True),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_6, False),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_6, False),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_6, False),
        fac.UpdateInstruction(cc_7, False) ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_6, True),
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_6, True),
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_8, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_6, False),
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_6, False),
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_6, False),
        fac.UpdateInstruction(cc_8, False) ]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_9, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_9, False) ]))
    st_7._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_10, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_10, False) ]))
    st_8._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_11, True) ]))
    st_9._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
MT541_SequenceD_TwoLegTransactionDetails._Automaton = _BuildAutomaton_6()




MT541_SequenceE_SettlementDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Indicator'), MT541_SequenceE_SettlementDetails_22F_Type, scope=MT541_SequenceE_SettlementDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1645, 3)))

MT541_SequenceE_SettlementDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SubSequenceE1_SettlementParties'), MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties, scope=MT541_SequenceE_SettlementDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1646, 3)))

MT541_SequenceE_SettlementDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SubSequenceE2_CashParties'), MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties, scope=MT541_SequenceE_SettlementDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1647, 3)))

MT541_SequenceE_SettlementDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SubSequenceE3_Amounts'), MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts, scope=MT541_SequenceE_SettlementDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1648, 3)))

def _BuildAutomaton_7 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_7
    del _BuildAutomaton_7
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1647, 3))
    counters.add(cc_0)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceE_SettlementDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Indicator')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1645, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceE_SettlementDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SubSequenceE1_SettlementParties')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1646, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceE_SettlementDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SubSequenceE2_CashParties')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1647, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceE_SettlementDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SubSequenceE3_Amounts')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1648, 3))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
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
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
         ]))
    st_3._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
MT541_SequenceE_SettlementDetails._Automaton = _BuildAutomaton_7()




MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PARTY_C'), MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95C_Type, scope=MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1657, 4)))

MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PARTY_L'), MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95L_Type, scope=MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1658, 4)))

MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PARTY_P'), MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95P_Type, scope=MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1659, 4)))

MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PARTY_Q'), MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95Q_Type, scope=MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1660, 4)))

MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PARTY_R'), MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95R_Type, scope=MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1661, 4)))

MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PARTY_S'), MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_95S_Type, scope=MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1662, 4)))

MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SafekeepingAccount_A'), MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_97A_Type, scope=MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1665, 4)))

MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SafekeepingAccount_B'), MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_97B_Type, scope=MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1666, 4)))

MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ProcessingDateTime_A'), MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_98A_Type, scope=MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1669, 4)))

MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ProcessingDateTime_C'), MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_98C_Type, scope=MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1670, 4)))

MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ProcessingReference'), MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_20C_Type, scope=MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1672, 3)))

MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Narrative_C'), MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_70C_Type, scope=MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1674, 4)))

MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Narrative_D'), MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_70D_Type, scope=MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1675, 4)))

MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Narrative_E'), MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties_70E_Type, scope=MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1676, 4)))

def _BuildAutomaton_8 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_8
    del _BuildAutomaton_8
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1664, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1665, 4))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1666, 4))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1668, 3))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1669, 4))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1670, 4))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1672, 3))
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1673, 3))
    counters.add(cc_7)
    cc_8 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1674, 4))
    counters.add(cc_8)
    cc_9 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1675, 4))
    counters.add(cc_9)
    cc_10 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1676, 4))
    counters.add(cc_10)
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PARTY_C')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1657, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PARTY_L')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1658, 4))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PARTY_P')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1659, 4))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PARTY_Q')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1660, 4))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PARTY_R')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1661, 4))
    st_4 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PARTY_S')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1662, 4))
    st_5 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SafekeepingAccount_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1665, 4))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SafekeepingAccount_B')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1666, 4))
    st_7 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ProcessingDateTime_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1669, 4))
    st_8 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    final_update.add(fac.UpdateInstruction(cc_5, False))
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ProcessingDateTime_C')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1670, 4))
    st_9 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_6, False))
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ProcessingReference')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1672, 3))
    st_10 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_10)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_7, False))
    final_update.add(fac.UpdateInstruction(cc_8, False))
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Narrative_C')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1674, 4))
    st_11 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_11)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_7, False))
    final_update.add(fac.UpdateInstruction(cc_9, False))
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Narrative_D')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1675, 4))
    st_12 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_12)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_7, False))
    final_update.add(fac.UpdateInstruction(cc_10, False))
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Narrative_E')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1676, 4))
    st_13 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_13)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
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
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
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
    transitions.append(fac.Transition(st_0, [
         ]))
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
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
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
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
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
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
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
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True),
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, True),
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
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True),
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, True),
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_2, True) ]))
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
    st_7._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_3, True),
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_4, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_3, True),
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
    st_8._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_3, True),
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_3, True),
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_5, True) ]))
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
    st_9._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_6, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_6, False) ]))
    st_10._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_7, True),
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_8, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_7, True),
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_7, True),
        fac.UpdateInstruction(cc_8, False) ]))
    st_11._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_7, True),
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_7, True),
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_9, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_7, True),
        fac.UpdateInstruction(cc_9, False) ]))
    st_12._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_7, True),
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_7, True),
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_7, True),
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_10, True) ]))
    st_13._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
MT541_SequenceE_SettlementDetails_SubSequenceE1_SettlementParties._Automaton = _BuildAutomaton_8()




MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PARTY_L'), MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95L_Type, scope=MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1686, 4)))

MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PARTY_P'), MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95P_Type, scope=MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1687, 4)))

MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PARTY_Q'), MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95Q_Type, scope=MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1688, 4)))

MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PARTY_R'), MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95R_Type, scope=MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1689, 4)))

MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PARTY_S'), MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_95S_Type, scope=MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1690, 4)))

MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Account_A'), MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_97A_Type, scope=MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1693, 4)))

MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Account_E'), MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_97E_Type, scope=MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1694, 4)))

MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Narrative_C'), MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_70C_Type, scope=MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1697, 4)))

MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Narrative_E'), MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties_70E_Type, scope=MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1698, 4)))

def _BuildAutomaton_9 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_9
    del _BuildAutomaton_9
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1692, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1693, 4))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1694, 4))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1696, 3))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1697, 4))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1698, 4))
    counters.add(cc_5)
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PARTY_L')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1686, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PARTY_P')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1687, 4))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PARTY_Q')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1688, 4))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PARTY_R')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1689, 4))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PARTY_S')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1690, 4))
    st_4 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Account_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1693, 4))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Account_E')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1694, 4))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Narrative_C')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1697, 4))
    st_7 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    final_update.add(fac.UpdateInstruction(cc_5, False))
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Narrative_E')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1698, 4))
    st_8 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
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
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
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
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
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
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
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
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
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
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True),
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True),
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_1, False) ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True),
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True),
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_2, False) ]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_3, True),
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_4, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_3, True),
        fac.UpdateInstruction(cc_4, False) ]))
    st_7._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_3, True),
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_3, True),
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_5, True) ]))
    st_8._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
MT541_SequenceE_SettlementDetails_SubSequenceE2_CashParties._Automaton = _BuildAutomaton_9()




MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Flag'), MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_17B_Type, scope=MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1707, 3)))

MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Amount'), MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_19A_Type, scope=MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1708, 3)))

MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ValueDateTime_A'), MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_98A_Type, scope=MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1710, 4)))

MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ValueDateTime_C'), MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_98C_Type, scope=MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1711, 4)))

MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ExchangeRate'), MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts_92B_Type, scope=MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1713, 3)))

def _BuildAutomaton_10 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_10
    del _BuildAutomaton_10
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1707, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1709, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1710, 4))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1711, 4))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1713, 3))
    counters.add(cc_4)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Flag')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1707, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Amount')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1708, 3))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ValueDateTime_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1710, 4))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ValueDateTime_C')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1711, 4))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ExchangeRate')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1713, 3))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
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
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, True),
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, True),
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, False),
        fac.UpdateInstruction(cc_2, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, True),
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, True),
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_3, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, False),
        fac.UpdateInstruction(cc_3, False) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_4, True) ]))
    st_4._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
MT541_SequenceE_SettlementDetails_SubSequenceE3_Amounts._Automaton = _BuildAutomaton_10()




MT541_SequenceF_OtherParties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PARTY_C'), MT541_SequenceF_OtherParties_95C_Type, scope=MT541_SequenceF_OtherParties, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1722, 4)))

MT541_SequenceF_OtherParties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PARTY_L'), MT541_SequenceF_OtherParties_95L_Type, scope=MT541_SequenceF_OtherParties, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1723, 4)))

MT541_SequenceF_OtherParties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PARTY_P'), MT541_SequenceF_OtherParties_95P_Type, scope=MT541_SequenceF_OtherParties, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1724, 4)))

MT541_SequenceF_OtherParties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PARTY_Q'), MT541_SequenceF_OtherParties_95Q_Type, scope=MT541_SequenceF_OtherParties, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1725, 4)))

MT541_SequenceF_OtherParties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PARTY_R'), MT541_SequenceF_OtherParties_95R_Type, scope=MT541_SequenceF_OtherParties, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1726, 4)))

MT541_SequenceF_OtherParties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PARTY_S'), MT541_SequenceF_OtherParties_95S_Type, scope=MT541_SequenceF_OtherParties, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1727, 4)))

MT541_SequenceF_OtherParties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SafekeepingAccount'), MT541_SequenceF_OtherParties_97A_Type, scope=MT541_SequenceF_OtherParties, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1729, 3)))

MT541_SequenceF_OtherParties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Narrative_C'), MT541_SequenceF_OtherParties_70C_Type, scope=MT541_SequenceF_OtherParties, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1731, 4)))

MT541_SequenceF_OtherParties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Narrative_D'), MT541_SequenceF_OtherParties_70D_Type, scope=MT541_SequenceF_OtherParties, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1732, 4)))

MT541_SequenceF_OtherParties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Narrative_E'), MT541_SequenceF_OtherParties_70E_Type, scope=MT541_SequenceF_OtherParties, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1733, 4)))

MT541_SequenceF_OtherParties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ProcessingReference'), MT541_SequenceF_OtherParties_20C_Type, scope=MT541_SequenceF_OtherParties, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1735, 3)))

def _BuildAutomaton_11 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_11
    del _BuildAutomaton_11
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1729, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1730, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1731, 4))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1732, 4))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1733, 4))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1735, 3))
    counters.add(cc_5)
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceF_OtherParties._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PARTY_C')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1722, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceF_OtherParties._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PARTY_L')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1723, 4))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceF_OtherParties._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PARTY_P')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1724, 4))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceF_OtherParties._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PARTY_Q')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1725, 4))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceF_OtherParties._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PARTY_R')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1726, 4))
    st_4 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceF_OtherParties._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PARTY_S')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1727, 4))
    st_5 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceF_OtherParties._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SafekeepingAccount')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1729, 3))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceF_OtherParties._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Narrative_C')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1731, 4))
    st_7 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceF_OtherParties._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Narrative_D')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1732, 4))
    st_8 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceF_OtherParties._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Narrative_E')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1733, 4))
    st_9 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_5, False))
    symbol = pyxb.binding.content.ElementUse(MT541_SequenceF_OtherParties._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ProcessingReference')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1735, 3))
    st_10 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_10)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
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
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
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
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
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
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
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
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
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
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
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
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_1, True),
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_1, True),
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_1, True),
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_1, False),
        fac.UpdateInstruction(cc_2, False) ]))
    st_7._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_1, True),
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_1, True),
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_3, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_1, True),
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_1, False),
        fac.UpdateInstruction(cc_3, False) ]))
    st_8._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_1, True),
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_1, True),
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_1, True),
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_4, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_1, False),
        fac.UpdateInstruction(cc_4, False) ]))
    st_9._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_5, True) ]))
    st_10._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
MT541_SequenceF_OtherParties._Automaton = _BuildAutomaton_11()




CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SequenceA_GeneralInformation'), MT541_SequenceA_GeneralInformation, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1744, 4)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SequenceB_TradeDetails'), MT541_SequenceB_TradeDetails, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1745, 4)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SequenceC_FinancialInstrumentAccount'), MT541_SequenceC_FinancialInstrumentAccount, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1746, 4)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SequenceD_TwoLegTransactionDetails'), MT541_SequenceD_TwoLegTransactionDetails, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1747, 4)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SequenceE_SettlementDetails'), MT541_SequenceE_SettlementDetails, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1748, 4)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SequenceF_OtherParties'), MT541_SequenceF_OtherParties, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1749, 4)))

def _BuildAutomaton_12 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_12
    del _BuildAutomaton_12
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1747, 4))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1749, 4))
    counters.add(cc_1)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SequenceA_GeneralInformation')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1744, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SequenceB_TradeDetails')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1745, 4))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SequenceC_FinancialInstrumentAccount')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1746, 4))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SequenceD_TwoLegTransactionDetails')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1747, 4))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SequenceE_SettlementDetails')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1748, 4))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SequenceF_OtherParties')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\TemplateFiles\\MT541.xsd', 1749, 4))
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
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_1, True) ]))
    st_5._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON._Automaton = _BuildAutomaton_12()


