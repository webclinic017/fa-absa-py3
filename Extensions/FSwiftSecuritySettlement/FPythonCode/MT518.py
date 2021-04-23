# C:\Projects\Code\SwiftMessagingSolution_Python3\base\extensions\SwiftIntegration\Utilities\XSD\MT518.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:96afad3d20bbfe8d040a1a097fa388d9fecd10e3
# Generated 2019-11-07 19:00:27.041159 by PyXB version 1.2.6 using Python 3.7.4.final.0
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
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:c25e76dc-0162-11ea-9d2b-509a4c321f2f')

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


# Atomic simple type: {http://www.w3schools.com}MT518_SequenceA_GeneralInformation_20C_Type_Pattern
class MT518_SequenceA_GeneralInformation_20C_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceA_GeneralInformation_20C_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 3, 1)
    _Documentation = None
MT518_SequenceA_GeneralInformation_20C_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceA_GeneralInformation_20C_Type_Pattern._CF_pattern.addPattern(pattern="(:(SEME)//[^/]([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,16}[^/])")
MT518_SequenceA_GeneralInformation_20C_Type_Pattern._InitializeFacetMap(MT518_SequenceA_GeneralInformation_20C_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceA_GeneralInformation_20C_Type_Pattern', MT518_SequenceA_GeneralInformation_20C_Type_Pattern)
_module_typeBindings.MT518_SequenceA_GeneralInformation_20C_Type_Pattern = MT518_SequenceA_GeneralInformation_20C_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceA_GeneralInformation_23G_Type_Pattern
class MT518_SequenceA_GeneralInformation_23G_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceA_GeneralInformation_23G_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 16, 1)
    _Documentation = None
MT518_SequenceA_GeneralInformation_23G_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceA_GeneralInformation_23G_Type_Pattern._CF_pattern.addPattern(pattern='((CANC|NEWM)(/(CODU|COPY|DUPL))?)')
MT518_SequenceA_GeneralInformation_23G_Type_Pattern._InitializeFacetMap(MT518_SequenceA_GeneralInformation_23G_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceA_GeneralInformation_23G_Type_Pattern', MT518_SequenceA_GeneralInformation_23G_Type_Pattern)
_module_typeBindings.MT518_SequenceA_GeneralInformation_23G_Type_Pattern = MT518_SequenceA_GeneralInformation_23G_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceA_GeneralInformation_98A_Type_Pattern
class MT518_SequenceA_GeneralInformation_98A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceA_GeneralInformation_98A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 29, 1)
    _Documentation = None
MT518_SequenceA_GeneralInformation_98A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceA_GeneralInformation_98A_Type_Pattern._CF_pattern.addPattern(pattern='(:(PREP)//[0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01]))')
MT518_SequenceA_GeneralInformation_98A_Type_Pattern._InitializeFacetMap(MT518_SequenceA_GeneralInformation_98A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceA_GeneralInformation_98A_Type_Pattern', MT518_SequenceA_GeneralInformation_98A_Type_Pattern)
_module_typeBindings.MT518_SequenceA_GeneralInformation_98A_Type_Pattern = MT518_SequenceA_GeneralInformation_98A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceA_GeneralInformation_98C_Type_Pattern
class MT518_SequenceA_GeneralInformation_98C_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceA_GeneralInformation_98C_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 42, 1)
    _Documentation = None
MT518_SequenceA_GeneralInformation_98C_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceA_GeneralInformation_98C_Type_Pattern._CF_pattern.addPattern(pattern='(:(PREP)//[0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])(0[0-9]|[1][0-9]|2[1-3])([0-5][0-9])([0-5][0-9]))')
MT518_SequenceA_GeneralInformation_98C_Type_Pattern._InitializeFacetMap(MT518_SequenceA_GeneralInformation_98C_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceA_GeneralInformation_98C_Type_Pattern', MT518_SequenceA_GeneralInformation_98C_Type_Pattern)
_module_typeBindings.MT518_SequenceA_GeneralInformation_98C_Type_Pattern = MT518_SequenceA_GeneralInformation_98C_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceA_GeneralInformation_98E_Type_Pattern
class MT518_SequenceA_GeneralInformation_98E_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceA_GeneralInformation_98E_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 55, 1)
    _Documentation = None
MT518_SequenceA_GeneralInformation_98E_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceA_GeneralInformation_98E_Type_Pattern._CF_pattern.addPattern(pattern='(:(PREP)//[0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])(0[0-9]|[1][0-9]|2[1-3])([0-5][0-9])([0-5][0-9])(,[0-9]{1,3})?(/(N)?(0[0-9]|[1][0-9]|2[1-3])(([0-5][0-9]))?)?)')
MT518_SequenceA_GeneralInformation_98E_Type_Pattern._InitializeFacetMap(MT518_SequenceA_GeneralInformation_98E_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceA_GeneralInformation_98E_Type_Pattern', MT518_SequenceA_GeneralInformation_98E_Type_Pattern)
_module_typeBindings.MT518_SequenceA_GeneralInformation_98E_Type_Pattern = MT518_SequenceA_GeneralInformation_98E_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceA_GeneralInformation_22F_Type_Pattern
class MT518_SequenceA_GeneralInformation_22F_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceA_GeneralInformation_22F_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 68, 1)
    _Documentation = None
MT518_SequenceA_GeneralInformation_22F_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceA_GeneralInformation_22F_Type_Pattern._CF_pattern.addPattern(pattern='(:(TRTR)/([A-Z0-9]{1,8})?/[A-Z0-9]{4})')
MT518_SequenceA_GeneralInformation_22F_Type_Pattern._InitializeFacetMap(MT518_SequenceA_GeneralInformation_22F_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceA_GeneralInformation_22F_Type_Pattern', MT518_SequenceA_GeneralInformation_22F_Type_Pattern)
_module_typeBindings.MT518_SequenceA_GeneralInformation_22F_Type_Pattern = MT518_SequenceA_GeneralInformation_22F_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13A_Type_Pattern
class MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 81, 1)
    _Documentation = None
MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13A_Type_Pattern._CF_pattern.addPattern(pattern='(:(LINK)//[A-Z0-9]{3})')
MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13A_Type_Pattern._InitializeFacetMap(MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13A_Type_Pattern', MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13A_Type_Pattern)
_module_typeBindings.MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13A_Type_Pattern = MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13B_Type_Pattern
class MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 94, 1)
    _Documentation = None
MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13B_Type_Pattern._CF_pattern.addPattern(pattern="(:(LINK)/([A-Z0-9]{1,8})?/[^/]([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,30}[^/])")
MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13B_Type_Pattern._InitializeFacetMap(MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13B_Type_Pattern', MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13B_Type_Pattern)
_module_typeBindings.MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13B_Type_Pattern = MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20C_Type_Pattern
class MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20C_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20C_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 107, 1)
    _Documentation = None
MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20C_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20C_Type_Pattern._CF_pattern.addPattern(pattern="(:(RELA|PREV|MAST|BASK|INDX|LIST|PROG|TRRF|COMM|COLR|ISSU|BMRB|ALMR)//[^/]([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,16}[^/])")
MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20C_Type_Pattern._InitializeFacetMap(MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20C_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20C_Type_Pattern', MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20C_Type_Pattern)
_module_typeBindings.MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20C_Type_Pattern = MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20C_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20U_Type_Pattern
class MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20U_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20U_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 120, 1)
    _Documentation = None
MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20U_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20U_Type_Pattern._CF_pattern.addPattern(pattern="(:(TRRF)//([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,52})")
MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20U_Type_Pattern._InitializeFacetMap(MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20U_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20U_Type_Pattern', MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20U_Type_Pattern)
_module_typeBindings.MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20U_Type_Pattern = MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20U_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_98A_Type_Pattern
class MT518_SequenceB_ConfirmationDetails_98A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceB_ConfirmationDetails_98A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 133, 1)
    _Documentation = None
MT518_SequenceB_ConfirmationDetails_98A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceB_ConfirmationDetails_98A_Type_Pattern._CF_pattern.addPattern(pattern='(:(SETT|TRAD|NAVD)//[0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01]))')
MT518_SequenceB_ConfirmationDetails_98A_Type_Pattern._InitializeFacetMap(MT518_SequenceB_ConfirmationDetails_98A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceB_ConfirmationDetails_98A_Type_Pattern', MT518_SequenceB_ConfirmationDetails_98A_Type_Pattern)
_module_typeBindings.MT518_SequenceB_ConfirmationDetails_98A_Type_Pattern = MT518_SequenceB_ConfirmationDetails_98A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_98B_Type_Pattern
class MT518_SequenceB_ConfirmationDetails_98B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceB_ConfirmationDetails_98B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 146, 1)
    _Documentation = None
MT518_SequenceB_ConfirmationDetails_98B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceB_ConfirmationDetails_98B_Type_Pattern._CF_pattern.addPattern(pattern='(:(SETT|TRAD)/([A-Z0-9]{1,8})?/[A-Z0-9]{4})')
MT518_SequenceB_ConfirmationDetails_98B_Type_Pattern._InitializeFacetMap(MT518_SequenceB_ConfirmationDetails_98B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceB_ConfirmationDetails_98B_Type_Pattern', MT518_SequenceB_ConfirmationDetails_98B_Type_Pattern)
_module_typeBindings.MT518_SequenceB_ConfirmationDetails_98B_Type_Pattern = MT518_SequenceB_ConfirmationDetails_98B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_98C_Type_Pattern
class MT518_SequenceB_ConfirmationDetails_98C_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceB_ConfirmationDetails_98C_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 159, 1)
    _Documentation = None
MT518_SequenceB_ConfirmationDetails_98C_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceB_ConfirmationDetails_98C_Type_Pattern._CF_pattern.addPattern(pattern='(:(SETT|TRAD|NAVD)//[0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])(0[0-9]|[1][0-9]|2[1-3])([0-5][0-9])([0-5][0-9]))')
MT518_SequenceB_ConfirmationDetails_98C_Type_Pattern._InitializeFacetMap(MT518_SequenceB_ConfirmationDetails_98C_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceB_ConfirmationDetails_98C_Type_Pattern', MT518_SequenceB_ConfirmationDetails_98C_Type_Pattern)
_module_typeBindings.MT518_SequenceB_ConfirmationDetails_98C_Type_Pattern = MT518_SequenceB_ConfirmationDetails_98C_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_98E_Type_Pattern
class MT518_SequenceB_ConfirmationDetails_98E_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceB_ConfirmationDetails_98E_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 172, 1)
    _Documentation = None
MT518_SequenceB_ConfirmationDetails_98E_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceB_ConfirmationDetails_98E_Type_Pattern._CF_pattern.addPattern(pattern='(:(TRAD)//[0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])(0[0-9]|[1][0-9]|2[1-3])([0-5][0-9])([0-5][0-9])(,[0-9]{1,3})?(/(N)?(0[0-9]|[1][0-9]|2[1-3])(([0-5][0-9]))?)?)')
MT518_SequenceB_ConfirmationDetails_98E_Type_Pattern._InitializeFacetMap(MT518_SequenceB_ConfirmationDetails_98E_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceB_ConfirmationDetails_98E_Type_Pattern', MT518_SequenceB_ConfirmationDetails_98E_Type_Pattern)
_module_typeBindings.MT518_SequenceB_ConfirmationDetails_98E_Type_Pattern = MT518_SequenceB_ConfirmationDetails_98E_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_90A_Type_Pattern
class MT518_SequenceB_ConfirmationDetails_90A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceB_ConfirmationDetails_90A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 185, 1)
    _Documentation = None
MT518_SequenceB_ConfirmationDetails_90A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceB_ConfirmationDetails_90A_Type_Pattern._CF_pattern.addPattern(pattern='(:(DEAL)//(DISC|PRCT|PREM|YIEL)/(N)?[0-9,(?0-9)]{1,15})')
MT518_SequenceB_ConfirmationDetails_90A_Type_Pattern._InitializeFacetMap(MT518_SequenceB_ConfirmationDetails_90A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceB_ConfirmationDetails_90A_Type_Pattern', MT518_SequenceB_ConfirmationDetails_90A_Type_Pattern)
_module_typeBindings.MT518_SequenceB_ConfirmationDetails_90A_Type_Pattern = MT518_SequenceB_ConfirmationDetails_90A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_90B_Type_Pattern
class MT518_SequenceB_ConfirmationDetails_90B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceB_ConfirmationDetails_90B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 198, 1)
    _Documentation = None
MT518_SequenceB_ConfirmationDetails_90B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceB_ConfirmationDetails_90B_Type_Pattern._CF_pattern.addPattern(pattern='(:(DEAL)//(ACTU|DISC|PREM)/(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})')
MT518_SequenceB_ConfirmationDetails_90B_Type_Pattern._InitializeFacetMap(MT518_SequenceB_ConfirmationDetails_90B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceB_ConfirmationDetails_90B_Type_Pattern', MT518_SequenceB_ConfirmationDetails_90B_Type_Pattern)
_module_typeBindings.MT518_SequenceB_ConfirmationDetails_90B_Type_Pattern = MT518_SequenceB_ConfirmationDetails_90B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_92A_Type_Pattern
class MT518_SequenceB_ConfirmationDetails_92A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceB_ConfirmationDetails_92A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 211, 1)
    _Documentation = None
MT518_SequenceB_ConfirmationDetails_92A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceB_ConfirmationDetails_92A_Type_Pattern._CF_pattern.addPattern(pattern='(:(CORA|COWA|BAKL|ENTF|NAVR)//(N)?[0-9,(?0-9)]{1,15})')
MT518_SequenceB_ConfirmationDetails_92A_Type_Pattern._InitializeFacetMap(MT518_SequenceB_ConfirmationDetails_92A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceB_ConfirmationDetails_92A_Type_Pattern', MT518_SequenceB_ConfirmationDetails_92A_Type_Pattern)
_module_typeBindings.MT518_SequenceB_ConfirmationDetails_92A_Type_Pattern = MT518_SequenceB_ConfirmationDetails_92A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_99A_Type_Pattern
class MT518_SequenceB_ConfirmationDetails_99A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceB_ConfirmationDetails_99A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 224, 1)
    _Documentation = None
MT518_SequenceB_ConfirmationDetails_99A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceB_ConfirmationDetails_99A_Type_Pattern._CF_pattern.addPattern(pattern='(:(DAAC|GIUP)//(N)?[0-9]{3})')
MT518_SequenceB_ConfirmationDetails_99A_Type_Pattern._InitializeFacetMap(MT518_SequenceB_ConfirmationDetails_99A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceB_ConfirmationDetails_99A_Type_Pattern', MT518_SequenceB_ConfirmationDetails_99A_Type_Pattern)
_module_typeBindings.MT518_SequenceB_ConfirmationDetails_99A_Type_Pattern = MT518_SequenceB_ConfirmationDetails_99A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_94B_Type_Pattern
class MT518_SequenceB_ConfirmationDetails_94B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceB_ConfirmationDetails_94B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 237, 1)
    _Documentation = None
MT518_SequenceB_ConfirmationDetails_94B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceB_ConfirmationDetails_94B_Type_Pattern._CF_pattern.addPattern(pattern="(:(TRAD|SAFE)/([A-Z0-9]{1,8})?/[A-Z0-9]{4}(/[^/]([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,30}[^/])?)")
MT518_SequenceB_ConfirmationDetails_94B_Type_Pattern._InitializeFacetMap(MT518_SequenceB_ConfirmationDetails_94B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceB_ConfirmationDetails_94B_Type_Pattern', MT518_SequenceB_ConfirmationDetails_94B_Type_Pattern)
_module_typeBindings.MT518_SequenceB_ConfirmationDetails_94B_Type_Pattern = MT518_SequenceB_ConfirmationDetails_94B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_94C_Type_Pattern
class MT518_SequenceB_ConfirmationDetails_94C_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceB_ConfirmationDetails_94C_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 250, 1)
    _Documentation = None
MT518_SequenceB_ConfirmationDetails_94C_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceB_ConfirmationDetails_94C_Type_Pattern._CF_pattern.addPattern(pattern='(:(SAFE)//[A-Z]{2})')
MT518_SequenceB_ConfirmationDetails_94C_Type_Pattern._InitializeFacetMap(MT518_SequenceB_ConfirmationDetails_94C_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceB_ConfirmationDetails_94C_Type_Pattern', MT518_SequenceB_ConfirmationDetails_94C_Type_Pattern)
_module_typeBindings.MT518_SequenceB_ConfirmationDetails_94C_Type_Pattern = MT518_SequenceB_ConfirmationDetails_94C_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_94F_Type_Pattern
class MT518_SequenceB_ConfirmationDetails_94F_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceB_ConfirmationDetails_94F_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 263, 1)
    _Documentation = None
MT518_SequenceB_ConfirmationDetails_94F_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceB_ConfirmationDetails_94F_Type_Pattern._CF_pattern.addPattern(pattern='(:(SAFE)//(CUST|ICSD|NCSD|SHHE)/[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)')
MT518_SequenceB_ConfirmationDetails_94F_Type_Pattern._InitializeFacetMap(MT518_SequenceB_ConfirmationDetails_94F_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceB_ConfirmationDetails_94F_Type_Pattern', MT518_SequenceB_ConfirmationDetails_94F_Type_Pattern)
_module_typeBindings.MT518_SequenceB_ConfirmationDetails_94F_Type_Pattern = MT518_SequenceB_ConfirmationDetails_94F_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_94L_Type_Pattern
class MT518_SequenceB_ConfirmationDetails_94L_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceB_ConfirmationDetails_94L_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 276, 1)
    _Documentation = None
MT518_SequenceB_ConfirmationDetails_94L_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceB_ConfirmationDetails_94L_Type_Pattern._CF_pattern.addPattern(pattern='(:(TRAD|SAFE)//[A-Z0-9]{18}[0-9]{2})')
MT518_SequenceB_ConfirmationDetails_94L_Type_Pattern._InitializeFacetMap(MT518_SequenceB_ConfirmationDetails_94L_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceB_ConfirmationDetails_94L_Type_Pattern', MT518_SequenceB_ConfirmationDetails_94L_Type_Pattern)
_module_typeBindings.MT518_SequenceB_ConfirmationDetails_94L_Type_Pattern = MT518_SequenceB_ConfirmationDetails_94L_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_19A_Type_Pattern
class MT518_SequenceB_ConfirmationDetails_19A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceB_ConfirmationDetails_19A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 289, 1)
    _Documentation = None
MT518_SequenceB_ConfirmationDetails_19A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceB_ConfirmationDetails_19A_Type_Pattern._CF_pattern.addPattern(pattern='(:(SETT)//(N)?(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})')
MT518_SequenceB_ConfirmationDetails_19A_Type_Pattern._InitializeFacetMap(MT518_SequenceB_ConfirmationDetails_19A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceB_ConfirmationDetails_19A_Type_Pattern', MT518_SequenceB_ConfirmationDetails_19A_Type_Pattern)
_module_typeBindings.MT518_SequenceB_ConfirmationDetails_19A_Type_Pattern = MT518_SequenceB_ConfirmationDetails_19A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_22F_Type_Pattern
class MT518_SequenceB_ConfirmationDetails_22F_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceB_ConfirmationDetails_22F_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 302, 1)
    _Documentation = None
MT518_SequenceB_ConfirmationDetails_22F_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceB_ConfirmationDetails_22F_Type_Pattern._CF_pattern.addPattern(pattern='(:(MPLE|PRIC|PROC|RPOR|PRIR|SETG|TTCO|COST|CATB|TRCN)/([A-Z0-9]{1,8})?/[A-Z0-9]{4})')
MT518_SequenceB_ConfirmationDetails_22F_Type_Pattern._InitializeFacetMap(MT518_SequenceB_ConfirmationDetails_22F_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceB_ConfirmationDetails_22F_Type_Pattern', MT518_SequenceB_ConfirmationDetails_22F_Type_Pattern)
_module_typeBindings.MT518_SequenceB_ConfirmationDetails_22F_Type_Pattern = MT518_SequenceB_ConfirmationDetails_22F_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_22H_Type_Pattern
class MT518_SequenceB_ConfirmationDetails_22H_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceB_ConfirmationDetails_22H_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 315, 1)
    _Documentation = None
MT518_SequenceB_ConfirmationDetails_22H_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceB_ConfirmationDetails_22H_Type_Pattern._CF_pattern.addPattern(pattern='(:(BUSE|PAYM)//[A-Z0-9]{4})')
MT518_SequenceB_ConfirmationDetails_22H_Type_Pattern._InitializeFacetMap(MT518_SequenceB_ConfirmationDetails_22H_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceB_ConfirmationDetails_22H_Type_Pattern', MT518_SequenceB_ConfirmationDetails_22H_Type_Pattern)
_module_typeBindings.MT518_SequenceB_ConfirmationDetails_22H_Type_Pattern = MT518_SequenceB_ConfirmationDetails_22H_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_11A_Type_Pattern
class MT518_SequenceB_ConfirmationDetails_11A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceB_ConfirmationDetails_11A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 328, 1)
    _Documentation = None
MT518_SequenceB_ConfirmationDetails_11A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceB_ConfirmationDetails_11A_Type_Pattern._CF_pattern.addPattern(pattern='(:(FXIB|FXIS)//(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD))')
MT518_SequenceB_ConfirmationDetails_11A_Type_Pattern._InitializeFacetMap(MT518_SequenceB_ConfirmationDetails_11A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceB_ConfirmationDetails_11A_Type_Pattern', MT518_SequenceB_ConfirmationDetails_11A_Type_Pattern)
_module_typeBindings.MT518_SequenceB_ConfirmationDetails_11A_Type_Pattern = MT518_SequenceB_ConfirmationDetails_11A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95L_Type_Pattern
class MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95L_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95L_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 341, 1)
    _Documentation = None
MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95L_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95L_Type_Pattern._CF_pattern.addPattern(pattern='(:(ALTE)//[A-Z0-9]{18}[0-9]{2})')
MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95L_Type_Pattern._InitializeFacetMap(MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95L_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95L_Type_Pattern', MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95L_Type_Pattern)
_module_typeBindings.MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95L_Type_Pattern = MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95L_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95P_Type_Pattern
class MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95P_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95P_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 354, 1)
    _Documentation = None
MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95P_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95P_Type_Pattern._CF_pattern.addPattern(pattern='(:(INVE|BUYR|CLBR|SELL|STBR|INBR|BRCR|ETC1|ETC2|AFFM|RQBR)//[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)')
MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95P_Type_Pattern._InitializeFacetMap(MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95P_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95P_Type_Pattern', MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95P_Type_Pattern)
_module_typeBindings.MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95P_Type_Pattern = MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95P_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95Q_Type_Pattern
class MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95Q_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95Q_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 367, 1)
    _Documentation = None
MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95Q_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95Q_Type_Pattern._CF_pattern.addPattern(pattern="(:(INVE|BUYR|CLBR|SELL|STBR|INBR|BRCR|ETC1|ETC2|AFFM|RQBR)//(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95Q_Type_Pattern._InitializeFacetMap(MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95Q_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95Q_Type_Pattern', MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95Q_Type_Pattern)
_module_typeBindings.MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95Q_Type_Pattern = MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95Q_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95R_Type_Pattern
class MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95R_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95R_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 380, 1)
    _Documentation = None
MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95R_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95R_Type_Pattern._CF_pattern.addPattern(pattern="(:(INVE|BUYR|CLBR|SELL|STBR|INBR|BRCR|ETC1|ETC2|AFFM|RQBR)/[A-Z0-9]{1,8}/[^/]([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34}[^/])")
MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95R_Type_Pattern._InitializeFacetMap(MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95R_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95R_Type_Pattern', MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95R_Type_Pattern)
_module_typeBindings.MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95R_Type_Pattern = MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95R_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95S_Type_Pattern
class MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95S_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95S_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 393, 1)
    _Documentation = None
MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95S_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95S_Type_Pattern._CF_pattern.addPattern(pattern="(:(ALTE)/([A-Z0-9]{1,8})?/[A-Z0-9]{4}/[A-Z]{2}/[^/]([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,30}[^/])")
MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95S_Type_Pattern._InitializeFacetMap(MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95S_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95S_Type_Pattern', MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95S_Type_Pattern)
_module_typeBindings.MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95S_Type_Pattern = MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95S_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_97A_Type_Pattern
class MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_97A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_97A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 406, 1)
    _Documentation = None
MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_97A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_97A_Type_Pattern._CF_pattern.addPattern(pattern="(:(SAFE|CASH)//([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35})")
MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_97A_Type_Pattern._InitializeFacetMap(MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_97A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_97A_Type_Pattern', MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_97A_Type_Pattern)
_module_typeBindings.MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_97A_Type_Pattern = MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_97A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_97B_Type_Pattern
class MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_97B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_97B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 419, 1)
    _Documentation = None
MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_97B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_97B_Type_Pattern._CF_pattern.addPattern(pattern="(:(SAFE)/([A-Z0-9]{1,8})?/[A-Z0-9]{4}/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35})")
MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_97B_Type_Pattern._InitializeFacetMap(MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_97B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_97B_Type_Pattern', MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_97B_Type_Pattern)
_module_typeBindings.MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_97B_Type_Pattern = MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_97B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_97E_Type_Pattern
class MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_97E_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_97E_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 432, 1)
    _Documentation = None
MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_97E_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_97E_Type_Pattern._CF_pattern.addPattern(pattern="(:(CASH)//([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})")
MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_97E_Type_Pattern._InitializeFacetMap(MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_97E_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_97E_Type_Pattern', MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_97E_Type_Pattern)
_module_typeBindings.MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_97E_Type_Pattern = MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_97E_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_98A_Type_Pattern
class MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_98A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_98A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 445, 1)
    _Documentation = None
MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_98A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_98A_Type_Pattern._CF_pattern.addPattern(pattern='(:(PROC)//[0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01]))')
MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_98A_Type_Pattern._InitializeFacetMap(MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_98A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_98A_Type_Pattern', MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_98A_Type_Pattern)
_module_typeBindings.MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_98A_Type_Pattern = MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_98A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_98C_Type_Pattern
class MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_98C_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_98C_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 458, 1)
    _Documentation = None
MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_98C_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_98C_Type_Pattern._CF_pattern.addPattern(pattern='(:(PROC)//[0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])(0[0-9]|[1][0-9]|2[1-3])([0-5][0-9])([0-5][0-9]))')
MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_98C_Type_Pattern._InitializeFacetMap(MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_98C_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_98C_Type_Pattern', MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_98C_Type_Pattern)
_module_typeBindings.MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_98C_Type_Pattern = MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_98C_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_20C_Type_Pattern
class MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_20C_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_20C_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 471, 1)
    _Documentation = None
MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_20C_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_20C_Type_Pattern._CF_pattern.addPattern(pattern="(:(PROC)//[^/]([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,16}[^/])")
MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_20C_Type_Pattern._InitializeFacetMap(MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_20C_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_20C_Type_Pattern', MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_20C_Type_Pattern)
_module_typeBindings.MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_20C_Type_Pattern = MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_20C_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_70C_Type_Pattern
class MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_70C_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_70C_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 484, 1)
    _Documentation = None
MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_70C_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_70C_Type_Pattern._CF_pattern.addPattern(pattern="(:(PACO)//(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_70C_Type_Pattern._InitializeFacetMap(MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_70C_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_70C_Type_Pattern', MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_70C_Type_Pattern)
_module_typeBindings.MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_70C_Type_Pattern = MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_70C_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_70E_Type_Pattern
class MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_70E_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_70E_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 497, 1)
    _Documentation = None
MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_70E_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_70E_Type_Pattern._CF_pattern.addPattern(pattern="(:(DECL)//(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,10})")
MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_70E_Type_Pattern._InitializeFacetMap(MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_70E_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_70E_Type_Pattern', MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_70E_Type_Pattern)
_module_typeBindings.MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_70E_Type_Pattern = MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_70E_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_22F_Type_Pattern
class MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_22F_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_22F_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 510, 1)
    _Documentation = None
MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_22F_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_22F_Type_Pattern._CF_pattern.addPattern(pattern='(:(TRCA|INCA)/([A-Z0-9]{1,8})?/[A-Z0-9]{4})')
MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_22F_Type_Pattern._InitializeFacetMap(MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_22F_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_22F_Type_Pattern', MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_22F_Type_Pattern)
_module_typeBindings.MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_22F_Type_Pattern = MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_22F_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_36B_Type_Pattern
class MT518_SequenceB_ConfirmationDetails_36B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceB_ConfirmationDetails_36B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 523, 1)
    _Documentation = None
MT518_SequenceB_ConfirmationDetails_36B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceB_ConfirmationDetails_36B_Type_Pattern._CF_pattern.addPattern(pattern='(:(CONF)//(AMOR|FAMT|UNIT)/[0-9,(?0-9)]{1,15})')
MT518_SequenceB_ConfirmationDetails_36B_Type_Pattern._InitializeFacetMap(MT518_SequenceB_ConfirmationDetails_36B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceB_ConfirmationDetails_36B_Type_Pattern', MT518_SequenceB_ConfirmationDetails_36B_Type_Pattern)
_module_typeBindings.MT518_SequenceB_ConfirmationDetails_36B_Type_Pattern = MT518_SequenceB_ConfirmationDetails_36B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_35B_Type_Pattern
class MT518_SequenceB_ConfirmationDetails_35B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceB_ConfirmationDetails_35B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 536, 1)
    _Documentation = None
MT518_SequenceB_ConfirmationDetails_35B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceB_ConfirmationDetails_35B_Type_Pattern._CF_pattern.addPattern(pattern="((ISIN {1}[A-Z0-9]{12})?(\\n)?((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})?)")
MT518_SequenceB_ConfirmationDetails_35B_Type_Pattern._InitializeFacetMap(MT518_SequenceB_ConfirmationDetails_35B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceB_ConfirmationDetails_35B_Type_Pattern', MT518_SequenceB_ConfirmationDetails_35B_Type_Pattern)
_module_typeBindings.MT518_SequenceB_ConfirmationDetails_35B_Type_Pattern = MT518_SequenceB_ConfirmationDetails_35B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_94B_Type_Pattern
class MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_94B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_94B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 549, 1)
    _Documentation = None
MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_94B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_94B_Type_Pattern._CF_pattern.addPattern(pattern="(:(PLIS)/([A-Z0-9]{1,8})?/[A-Z0-9]{4}(/[^/]([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,30}[^/])?)")
MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_94B_Type_Pattern._InitializeFacetMap(MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_94B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_94B_Type_Pattern', MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_94B_Type_Pattern)
_module_typeBindings.MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_94B_Type_Pattern = MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_94B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_22F_Type_Pattern
class MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_22F_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_22F_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 562, 1)
    _Documentation = None
MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_22F_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_22F_Type_Pattern._CF_pattern.addPattern(pattern='(:(MICO|FORM|PFRE|PAYS|CFRE)/([A-Z0-9]{1,8})?/[A-Z0-9]{4})')
MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_22F_Type_Pattern._InitializeFacetMap(MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_22F_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_22F_Type_Pattern', MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_22F_Type_Pattern)
_module_typeBindings.MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_22F_Type_Pattern = MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_22F_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_12A_Type_Pattern
class MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_12A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_12A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 575, 1)
    _Documentation = None
MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_12A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_12A_Type_Pattern._CF_pattern.addPattern(pattern="(:(CLAS)/([A-Z0-9]{1,8})?/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,30})")
MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_12A_Type_Pattern._InitializeFacetMap(MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_12A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_12A_Type_Pattern', MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_12A_Type_Pattern)
_module_typeBindings.MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_12A_Type_Pattern = MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_12A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_12B_Type_Pattern
class MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_12B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_12B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 588, 1)
    _Documentation = None
MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_12B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_12B_Type_Pattern._CF_pattern.addPattern(pattern='(:(OPST|OPTI)/([A-Z0-9]{1,8})?/[A-Z0-9]{4})')
MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_12B_Type_Pattern._InitializeFacetMap(MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_12B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_12B_Type_Pattern', MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_12B_Type_Pattern)
_module_typeBindings.MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_12B_Type_Pattern = MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_12B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_12C_Type_Pattern
class MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_12C_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_12C_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 601, 1)
    _Documentation = None
MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_12C_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_12C_Type_Pattern._CF_pattern.addPattern(pattern='(:(CLAS)//[A-Z0-9]{6})')
MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_12C_Type_Pattern._InitializeFacetMap(MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_12C_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_12C_Type_Pattern', MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_12C_Type_Pattern)
_module_typeBindings.MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_12C_Type_Pattern = MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_12C_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_11A_Type_Pattern
class MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_11A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_11A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 614, 1)
    _Documentation = None
MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_11A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_11A_Type_Pattern._CF_pattern.addPattern(pattern='(:(DENO)//(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD))')
MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_11A_Type_Pattern._InitializeFacetMap(MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_11A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_11A_Type_Pattern', MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_11A_Type_Pattern)
_module_typeBindings.MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_11A_Type_Pattern = MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_11A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_98A_Type_Pattern
class MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_98A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_98A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 627, 1)
    _Documentation = None
MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_98A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_98A_Type_Pattern._CF_pattern.addPattern(pattern='(:(COUP|EXPI|FRNR|MATU|ISSU|CALD|CONV|PUTT|DDTE|FCOU|NWFC)//[0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01]))')
MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_98A_Type_Pattern._InitializeFacetMap(MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_98A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_98A_Type_Pattern', MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_98A_Type_Pattern)
_module_typeBindings.MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_98A_Type_Pattern = MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_98A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_92A_Type_Pattern
class MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_92A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_92A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 640, 1)
    _Documentation = None
MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_92A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_92A_Type_Pattern._CF_pattern.addPattern(pattern='(:(PRFC|CUFC|NWFC|INTR|NXRT|INDX|YTMR)//(N)?[0-9,(?0-9)]{1,15})')
MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_92A_Type_Pattern._InitializeFacetMap(MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_92A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_92A_Type_Pattern', MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_92A_Type_Pattern)
_module_typeBindings.MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_92A_Type_Pattern = MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_92A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_13A_Type_Pattern
class MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_13A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_13A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 653, 1)
    _Documentation = None
MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_13A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_13A_Type_Pattern._CF_pattern.addPattern(pattern='(:(COUP|VERN)//[A-Z0-9]{3})')
MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_13A_Type_Pattern._InitializeFacetMap(MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_13A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_13A_Type_Pattern', MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_13A_Type_Pattern)
_module_typeBindings.MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_13A_Type_Pattern = MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_13A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_13B_Type_Pattern
class MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_13B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_13B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 666, 1)
    _Documentation = None
MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_13B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_13B_Type_Pattern._CF_pattern.addPattern(pattern="(:(COUP|POOL|LOTS|VERN)/([A-Z0-9]{1,8})?/[^/]([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,30}[^/])")
MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_13B_Type_Pattern._InitializeFacetMap(MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_13B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_13B_Type_Pattern', MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_13B_Type_Pattern)
_module_typeBindings.MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_13B_Type_Pattern = MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_13B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_17B_Type_Pattern
class MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_17B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_17B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 679, 1)
    _Documentation = None
MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_17B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_17B_Type_Pattern._CF_pattern.addPattern(pattern='(:(CONV|FRNF|COVE|CALL|PUTT|WRTS|ODDC)//(Y|N))')
MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_17B_Type_Pattern._InitializeFacetMap(MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_17B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_17B_Type_Pattern', MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_17B_Type_Pattern)
_module_typeBindings.MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_17B_Type_Pattern = MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_17B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_90A_Type_Pattern
class MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_90A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_90A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 692, 1)
    _Documentation = None
MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_90A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_90A_Type_Pattern._CF_pattern.addPattern(pattern='(:(INDC|MRKT|EXER)//(DISC|PRCT|PREM|YIEL)/(N)?[0-9,(?0-9)]{1,15})')
MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_90A_Type_Pattern._InitializeFacetMap(MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_90A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_90A_Type_Pattern', MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_90A_Type_Pattern)
_module_typeBindings.MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_90A_Type_Pattern = MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_90A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_90B_Type_Pattern
class MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_90B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_90B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 705, 1)
    _Documentation = None
MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_90B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_90B_Type_Pattern._CF_pattern.addPattern(pattern='(:(INDC|MRKT|EXER)//(ACTU|DISC|PREM)/(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})')
MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_90B_Type_Pattern._InitializeFacetMap(MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_90B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_90B_Type_Pattern', MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_90B_Type_Pattern)
_module_typeBindings.MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_90B_Type_Pattern = MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_90B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_36B_Type_Pattern
class MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_36B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_36B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 718, 1)
    _Documentation = None
MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_36B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_36B_Type_Pattern._CF_pattern.addPattern(pattern='(:(MINO|SIZE|ORGV)//(AMOR|FAMT|UNIT)/[0-9,(?0-9)]{1,15})')
MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_36B_Type_Pattern._InitializeFacetMap(MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_36B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_36B_Type_Pattern', MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_36B_Type_Pattern)
_module_typeBindings.MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_36B_Type_Pattern = MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_36B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_35B_Type_Pattern
class MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_35B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_35B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 731, 1)
    _Documentation = None
MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_35B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_35B_Type_Pattern._CF_pattern.addPattern(pattern="((ISIN {1}[A-Z0-9]{12})?(\\n)?((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})?)")
MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_35B_Type_Pattern._InitializeFacetMap(MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_35B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_35B_Type_Pattern', MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_35B_Type_Pattern)
_module_typeBindings.MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_35B_Type_Pattern = MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_35B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_70E_Type_Pattern
class MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_70E_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_70E_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 744, 1)
    _Documentation = None
MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_70E_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_70E_Type_Pattern._CF_pattern.addPattern(pattern="(:(FIAN)//(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,10})")
MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_70E_Type_Pattern._InitializeFacetMap(MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_70E_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_70E_Type_Pattern', MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_70E_Type_Pattern)
_module_typeBindings.MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_70E_Type_Pattern = MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_70E_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_13B_Type_Pattern
class MT518_SequenceB_ConfirmationDetails_13B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceB_ConfirmationDetails_13B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 757, 1)
    _Documentation = None
MT518_SequenceB_ConfirmationDetails_13B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceB_ConfirmationDetails_13B_Type_Pattern._CF_pattern.addPattern(pattern="(:(CERT)/([A-Z0-9]{1,8})?/[^/]([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,30}[^/])")
MT518_SequenceB_ConfirmationDetails_13B_Type_Pattern._InitializeFacetMap(MT518_SequenceB_ConfirmationDetails_13B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceB_ConfirmationDetails_13B_Type_Pattern', MT518_SequenceB_ConfirmationDetails_13B_Type_Pattern)
_module_typeBindings.MT518_SequenceB_ConfirmationDetails_13B_Type_Pattern = MT518_SequenceB_ConfirmationDetails_13B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_70E_Type_Pattern
class MT518_SequenceB_ConfirmationDetails_70E_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceB_ConfirmationDetails_70E_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 770, 1)
    _Documentation = None
MT518_SequenceB_ConfirmationDetails_70E_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceB_ConfirmationDetails_70E_Type_Pattern._CF_pattern.addPattern(pattern="(:(TPRO|RSTR)//(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,10})")
MT518_SequenceB_ConfirmationDetails_70E_Type_Pattern._InitializeFacetMap(MT518_SequenceB_ConfirmationDetails_70E_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceB_ConfirmationDetails_70E_Type_Pattern', MT518_SequenceB_ConfirmationDetails_70E_Type_Pattern)
_module_typeBindings.MT518_SequenceB_ConfirmationDetails_70E_Type_Pattern = MT518_SequenceB_ConfirmationDetails_70E_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceC_SettlementDetails_22F_Type_Pattern
class MT518_SequenceC_SettlementDetails_22F_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceC_SettlementDetails_22F_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 783, 1)
    _Documentation = None
MT518_SequenceC_SettlementDetails_22F_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceC_SettlementDetails_22F_Type_Pattern._CF_pattern.addPattern(pattern='(:(SETR|STCO|STAM|RTGS|REGT|BENE|CASY|DBNM|REST|LEOG|SETS|REPT)/([A-Z0-9]{1,8})?/[A-Z0-9]{4})')
MT518_SequenceC_SettlementDetails_22F_Type_Pattern._InitializeFacetMap(MT518_SequenceC_SettlementDetails_22F_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceC_SettlementDetails_22F_Type_Pattern', MT518_SequenceC_SettlementDetails_22F_Type_Pattern)
_module_typeBindings.MT518_SequenceC_SettlementDetails_22F_Type_Pattern = MT518_SequenceC_SettlementDetails_22F_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceC_SettlementDetails_11A_Type_Pattern
class MT518_SequenceC_SettlementDetails_11A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceC_SettlementDetails_11A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 796, 1)
    _Documentation = None
MT518_SequenceC_SettlementDetails_11A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceC_SettlementDetails_11A_Type_Pattern._CF_pattern.addPattern(pattern='(:(FXIB|FXIS)//(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD))')
MT518_SequenceC_SettlementDetails_11A_Type_Pattern._InitializeFacetMap(MT518_SequenceC_SettlementDetails_11A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceC_SettlementDetails_11A_Type_Pattern', MT518_SequenceC_SettlementDetails_11A_Type_Pattern)
_module_typeBindings.MT518_SequenceC_SettlementDetails_11A_Type_Pattern = MT518_SequenceC_SettlementDetails_11A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95C_Type_Pattern
class MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95C_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95C_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 809, 1)
    _Documentation = None
MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95C_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95C_Type_Pattern._CF_pattern.addPattern(pattern='(:(PSET)//[A-Z]{2})')
MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95C_Type_Pattern._InitializeFacetMap(MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95C_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95C_Type_Pattern', MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95C_Type_Pattern)
_module_typeBindings.MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95C_Type_Pattern = MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95C_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95L_Type_Pattern
class MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95L_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95L_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 822, 1)
    _Documentation = None
MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95L_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95L_Type_Pattern._CF_pattern.addPattern(pattern='(:(ALTE)//[A-Z0-9]{18}[0-9]{2})')
MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95L_Type_Pattern._InitializeFacetMap(MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95L_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95L_Type_Pattern', MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95L_Type_Pattern)
_module_typeBindings.MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95L_Type_Pattern = MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95L_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95P_Type_Pattern
class MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95P_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95P_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 835, 1)
    _Documentation = None
MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95P_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95P_Type_Pattern._CF_pattern.addPattern(pattern='(:(BUYR|DEAG|DECU|DEI1|DEI2|PSET|REAG|RECU|REI1|REI2|SELL)//[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)')
MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95P_Type_Pattern._InitializeFacetMap(MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95P_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95P_Type_Pattern', MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95P_Type_Pattern)
_module_typeBindings.MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95P_Type_Pattern = MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95P_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95Q_Type_Pattern
class MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95Q_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95Q_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 848, 1)
    _Documentation = None
MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95Q_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95Q_Type_Pattern._CF_pattern.addPattern(pattern="(:(BUYR|DEAG|DECU|DEI1|DEI2|PSET|REAG|RECU|REI1|REI2|SELL)//(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95Q_Type_Pattern._InitializeFacetMap(MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95Q_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95Q_Type_Pattern', MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95Q_Type_Pattern)
_module_typeBindings.MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95Q_Type_Pattern = MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95Q_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95R_Type_Pattern
class MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95R_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95R_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 861, 1)
    _Documentation = None
MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95R_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95R_Type_Pattern._CF_pattern.addPattern(pattern="(:(BUYR|DEAG|DECU|DEI1|DEI2|REAG|RECU|REI1|REI2|SELL)/[A-Z0-9]{1,8}/[^/]([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34}[^/])")
MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95R_Type_Pattern._InitializeFacetMap(MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95R_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95R_Type_Pattern', MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95R_Type_Pattern)
_module_typeBindings.MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95R_Type_Pattern = MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95R_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95S_Type_Pattern
class MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95S_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95S_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 874, 1)
    _Documentation = None
MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95S_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95S_Type_Pattern._CF_pattern.addPattern(pattern="(:(ALTE)/([A-Z0-9]{1,8})?/[A-Z0-9]{4}/[A-Z]{2}/[^/]([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,30}[^/])")
MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95S_Type_Pattern._InitializeFacetMap(MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95S_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95S_Type_Pattern', MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95S_Type_Pattern)
_module_typeBindings.MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95S_Type_Pattern = MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95S_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_97A_Type_Pattern
class MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_97A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_97A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 887, 1)
    _Documentation = None
MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_97A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_97A_Type_Pattern._CF_pattern.addPattern(pattern="(:(SAFE)//([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35})")
MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_97A_Type_Pattern._InitializeFacetMap(MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_97A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_97A_Type_Pattern', MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_97A_Type_Pattern)
_module_typeBindings.MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_97A_Type_Pattern = MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_97A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_97B_Type_Pattern
class MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_97B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_97B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 900, 1)
    _Documentation = None
MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_97B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_97B_Type_Pattern._CF_pattern.addPattern(pattern="(:(SAFE)/([A-Z0-9]{1,8})?/[A-Z0-9]{4}/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35})")
MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_97B_Type_Pattern._InitializeFacetMap(MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_97B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_97B_Type_Pattern', MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_97B_Type_Pattern)
_module_typeBindings.MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_97B_Type_Pattern = MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_97B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_98A_Type_Pattern
class MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_98A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_98A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 913, 1)
    _Documentation = None
MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_98A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_98A_Type_Pattern._CF_pattern.addPattern(pattern='(:(PROC)//[0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01]))')
MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_98A_Type_Pattern._InitializeFacetMap(MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_98A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_98A_Type_Pattern', MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_98A_Type_Pattern)
_module_typeBindings.MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_98A_Type_Pattern = MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_98A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_98C_Type_Pattern
class MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_98C_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_98C_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 926, 1)
    _Documentation = None
MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_98C_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_98C_Type_Pattern._CF_pattern.addPattern(pattern='(:(PROC)//[0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])(0[0-9]|[1][0-9]|2[1-3])([0-5][0-9])([0-5][0-9]))')
MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_98C_Type_Pattern._InitializeFacetMap(MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_98C_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_98C_Type_Pattern', MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_98C_Type_Pattern)
_module_typeBindings.MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_98C_Type_Pattern = MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_98C_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_20C_Type_Pattern
class MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_20C_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_20C_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 939, 1)
    _Documentation = None
MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_20C_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_20C_Type_Pattern._CF_pattern.addPattern(pattern="(:(PROC)//[^/]([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,16}[^/])")
MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_20C_Type_Pattern._InitializeFacetMap(MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_20C_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_20C_Type_Pattern', MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_20C_Type_Pattern)
_module_typeBindings.MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_20C_Type_Pattern = MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_20C_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_70C_Type_Pattern
class MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_70C_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_70C_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 952, 1)
    _Documentation = None
MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_70C_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_70C_Type_Pattern._CF_pattern.addPattern(pattern="(:(PACO)//(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_70C_Type_Pattern._InitializeFacetMap(MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_70C_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_70C_Type_Pattern', MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_70C_Type_Pattern)
_module_typeBindings.MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_70C_Type_Pattern = MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_70C_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_70D_Type_Pattern
class MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_70D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_70D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 965, 1)
    _Documentation = None
MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_70D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_70D_Type_Pattern._CF_pattern.addPattern(pattern="(:(REGI)//(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,6})")
MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_70D_Type_Pattern._InitializeFacetMap(MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_70D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_70D_Type_Pattern', MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_70D_Type_Pattern)
_module_typeBindings.MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_70D_Type_Pattern = MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_70D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95L_Type_Pattern
class MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95L_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95L_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 978, 1)
    _Documentation = None
MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95L_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95L_Type_Pattern._CF_pattern.addPattern(pattern='(:(ALTE)//[A-Z0-9]{18}[0-9]{2})')
MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95L_Type_Pattern._InitializeFacetMap(MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95L_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95L_Type_Pattern', MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95L_Type_Pattern)
_module_typeBindings.MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95L_Type_Pattern = MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95L_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95P_Type_Pattern
class MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95P_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95P_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 991, 1)
    _Documentation = None
MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95P_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95P_Type_Pattern._CF_pattern.addPattern(pattern='(:(ACCW|BENM|DEBT|INTM|PAYE)//[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)')
MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95P_Type_Pattern._InitializeFacetMap(MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95P_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95P_Type_Pattern', MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95P_Type_Pattern)
_module_typeBindings.MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95P_Type_Pattern = MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95P_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95Q_Type_Pattern
class MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95Q_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95Q_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1004, 1)
    _Documentation = None
MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95Q_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95Q_Type_Pattern._CF_pattern.addPattern(pattern="(:(ACCW|BENM|DEBT|INTM|PAYE)//(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95Q_Type_Pattern._InitializeFacetMap(MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95Q_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95Q_Type_Pattern', MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95Q_Type_Pattern)
_module_typeBindings.MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95Q_Type_Pattern = MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95Q_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95R_Type_Pattern
class MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95R_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95R_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1017, 1)
    _Documentation = None
MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95R_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95R_Type_Pattern._CF_pattern.addPattern(pattern="(:(ACCW|BENM|DEBT|INTM|PAYE)/[A-Z0-9]{1,8}/[^/]([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34}[^/])")
MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95R_Type_Pattern._InitializeFacetMap(MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95R_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95R_Type_Pattern', MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95R_Type_Pattern)
_module_typeBindings.MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95R_Type_Pattern = MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95R_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95S_Type_Pattern
class MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95S_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95S_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1030, 1)
    _Documentation = None
MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95S_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95S_Type_Pattern._CF_pattern.addPattern(pattern="(:(ALTE)/([A-Z0-9]{1,8})?/[A-Z0-9]{4}/[A-Z]{2}/[^/]([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,30}[^/])")
MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95S_Type_Pattern._InitializeFacetMap(MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95S_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95S_Type_Pattern', MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95S_Type_Pattern)
_module_typeBindings.MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95S_Type_Pattern = MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95S_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_97A_Type_Pattern
class MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_97A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_97A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1043, 1)
    _Documentation = None
MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_97A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_97A_Type_Pattern._CF_pattern.addPattern(pattern="(:(CASH|CHAR|COMM|TAXE)//([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35})")
MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_97A_Type_Pattern._InitializeFacetMap(MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_97A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_97A_Type_Pattern', MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_97A_Type_Pattern)
_module_typeBindings.MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_97A_Type_Pattern = MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_97A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_97E_Type_Pattern
class MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_97E_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_97E_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1056, 1)
    _Documentation = None
MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_97E_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_97E_Type_Pattern._CF_pattern.addPattern(pattern="(:(CASH|CHAR|COMM|TAXE)//([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})")
MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_97E_Type_Pattern._InitializeFacetMap(MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_97E_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_97E_Type_Pattern', MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_97E_Type_Pattern)
_module_typeBindings.MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_97E_Type_Pattern = MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_97E_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_98A_Type_Pattern
class MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_98A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_98A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1069, 1)
    _Documentation = None
MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_98A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_98A_Type_Pattern._CF_pattern.addPattern(pattern='(:(PROC)//[0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01]))')
MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_98A_Type_Pattern._InitializeFacetMap(MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_98A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_98A_Type_Pattern', MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_98A_Type_Pattern)
_module_typeBindings.MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_98A_Type_Pattern = MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_98A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_98C_Type_Pattern
class MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_98C_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_98C_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1082, 1)
    _Documentation = None
MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_98C_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_98C_Type_Pattern._CF_pattern.addPattern(pattern='(:(PROC)//[0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])(0[0-9]|[1][0-9]|2[1-3])([0-5][0-9])([0-5][0-9]))')
MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_98C_Type_Pattern._InitializeFacetMap(MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_98C_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_98C_Type_Pattern', MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_98C_Type_Pattern)
_module_typeBindings.MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_98C_Type_Pattern = MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_98C_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_20C_Type_Pattern
class MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_20C_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_20C_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1095, 1)
    _Documentation = None
MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_20C_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_20C_Type_Pattern._CF_pattern.addPattern(pattern="(:(PROC)//[^/]([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,16}[^/])")
MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_20C_Type_Pattern._InitializeFacetMap(MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_20C_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_20C_Type_Pattern', MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_20C_Type_Pattern)
_module_typeBindings.MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_20C_Type_Pattern = MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_20C_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_70C_Type_Pattern
class MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_70C_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_70C_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1108, 1)
    _Documentation = None
MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_70C_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_70C_Type_Pattern._CF_pattern.addPattern(pattern="(:(PACO)//(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_70C_Type_Pattern._InitializeFacetMap(MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_70C_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_70C_Type_Pattern', MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_70C_Type_Pattern)
_module_typeBindings.MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_70C_Type_Pattern = MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_70C_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_17B_Type_Pattern
class MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_17B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_17B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1121, 1)
    _Documentation = None
MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_17B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_17B_Type_Pattern._CF_pattern.addPattern(pattern='(:(ACRU|STAM|EXEC|RSCH)//(Y|N))')
MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_17B_Type_Pattern._InitializeFacetMap(MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_17B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_17B_Type_Pattern', MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_17B_Type_Pattern)
_module_typeBindings.MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_17B_Type_Pattern = MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_17B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_19A_Type_Pattern
class MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_19A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_19A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1134, 1)
    _Documentation = None
MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_19A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_19A_Type_Pattern._CF_pattern.addPattern(pattern='(:[A-Z0-9]{4}//(N)?(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})')
MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_19A_Type_Pattern._InitializeFacetMap(MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_19A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_19A_Type_Pattern', MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_19A_Type_Pattern)
_module_typeBindings.MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_19A_Type_Pattern = MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_19A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_98A_Type_Pattern
class MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_98A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_98A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1147, 1)
    _Documentation = None
MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_98A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_98A_Type_Pattern._CF_pattern.addPattern(pattern='(:(VALU)//[0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01]))')
MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_98A_Type_Pattern._InitializeFacetMap(MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_98A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_98A_Type_Pattern', MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_98A_Type_Pattern)
_module_typeBindings.MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_98A_Type_Pattern = MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_98A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_98C_Type_Pattern
class MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_98C_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_98C_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1160, 1)
    _Documentation = None
MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_98C_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_98C_Type_Pattern._CF_pattern.addPattern(pattern='(:(VALU)//[0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])(0[0-9]|[1][0-9]|2[1-3])([0-5][0-9])([0-5][0-9]))')
MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_98C_Type_Pattern._InitializeFacetMap(MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_98C_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_98C_Type_Pattern', MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_98C_Type_Pattern)
_module_typeBindings.MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_98C_Type_Pattern = MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_98C_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_92B_Type_Pattern
class MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_92B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_92B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1173, 1)
    _Documentation = None
MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_92B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_92B_Type_Pattern._CF_pattern.addPattern(pattern='(:(EXCH)//(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)/(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)/[0-9,(?0-9)]{1,15})')
MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_92B_Type_Pattern._InitializeFacetMap(MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_92B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_92B_Type_Pattern', MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_92B_Type_Pattern)
_module_typeBindings.MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_92B_Type_Pattern = MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_92B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceD_OtherParties_95L_Type_Pattern
class MT518_SequenceD_OtherParties_95L_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceD_OtherParties_95L_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1186, 1)
    _Documentation = None
MT518_SequenceD_OtherParties_95L_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceD_OtherParties_95L_Type_Pattern._CF_pattern.addPattern(pattern='(:(ALTE)//[A-Z0-9]{18}[0-9]{2})')
MT518_SequenceD_OtherParties_95L_Type_Pattern._InitializeFacetMap(MT518_SequenceD_OtherParties_95L_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceD_OtherParties_95L_Type_Pattern', MT518_SequenceD_OtherParties_95L_Type_Pattern)
_module_typeBindings.MT518_SequenceD_OtherParties_95L_Type_Pattern = MT518_SequenceD_OtherParties_95L_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceD_OtherParties_95P_Type_Pattern
class MT518_SequenceD_OtherParties_95P_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceD_OtherParties_95P_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1199, 1)
    _Documentation = None
MT518_SequenceD_OtherParties_95P_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceD_OtherParties_95P_Type_Pattern._CF_pattern.addPattern(pattern='(:(EXCH|MEOR|MERE|TRRE|TRAG|VEND|INPA)//[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)')
MT518_SequenceD_OtherParties_95P_Type_Pattern._InitializeFacetMap(MT518_SequenceD_OtherParties_95P_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceD_OtherParties_95P_Type_Pattern', MT518_SequenceD_OtherParties_95P_Type_Pattern)
_module_typeBindings.MT518_SequenceD_OtherParties_95P_Type_Pattern = MT518_SequenceD_OtherParties_95P_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceD_OtherParties_95Q_Type_Pattern
class MT518_SequenceD_OtherParties_95Q_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceD_OtherParties_95Q_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1212, 1)
    _Documentation = None
MT518_SequenceD_OtherParties_95Q_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceD_OtherParties_95Q_Type_Pattern._CF_pattern.addPattern(pattern="(:(EXCH|MEOR|MERE|TRRE|TRAG|VEND|INPA)//(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT518_SequenceD_OtherParties_95Q_Type_Pattern._InitializeFacetMap(MT518_SequenceD_OtherParties_95Q_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceD_OtherParties_95Q_Type_Pattern', MT518_SequenceD_OtherParties_95Q_Type_Pattern)
_module_typeBindings.MT518_SequenceD_OtherParties_95Q_Type_Pattern = MT518_SequenceD_OtherParties_95Q_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceD_OtherParties_95R_Type_Pattern
class MT518_SequenceD_OtherParties_95R_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceD_OtherParties_95R_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1225, 1)
    _Documentation = None
MT518_SequenceD_OtherParties_95R_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceD_OtherParties_95R_Type_Pattern._CF_pattern.addPattern(pattern="(:(EXCH|MEOR|MERE|TRRE|TRAG|VEND|INPA)/[A-Z0-9]{1,8}/[^/]([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34}[^/])")
MT518_SequenceD_OtherParties_95R_Type_Pattern._InitializeFacetMap(MT518_SequenceD_OtherParties_95R_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceD_OtherParties_95R_Type_Pattern', MT518_SequenceD_OtherParties_95R_Type_Pattern)
_module_typeBindings.MT518_SequenceD_OtherParties_95R_Type_Pattern = MT518_SequenceD_OtherParties_95R_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceD_OtherParties_95S_Type_Pattern
class MT518_SequenceD_OtherParties_95S_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceD_OtherParties_95S_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1238, 1)
    _Documentation = None
MT518_SequenceD_OtherParties_95S_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceD_OtherParties_95S_Type_Pattern._CF_pattern.addPattern(pattern="(:(ALTE)/([A-Z0-9]{1,8})?/[A-Z0-9]{4}/[A-Z]{2}/[^/]([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,30}[^/])")
MT518_SequenceD_OtherParties_95S_Type_Pattern._InitializeFacetMap(MT518_SequenceD_OtherParties_95S_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceD_OtherParties_95S_Type_Pattern', MT518_SequenceD_OtherParties_95S_Type_Pattern)
_module_typeBindings.MT518_SequenceD_OtherParties_95S_Type_Pattern = MT518_SequenceD_OtherParties_95S_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceD_OtherParties_97A_Type_Pattern
class MT518_SequenceD_OtherParties_97A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceD_OtherParties_97A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1251, 1)
    _Documentation = None
MT518_SequenceD_OtherParties_97A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceD_OtherParties_97A_Type_Pattern._CF_pattern.addPattern(pattern="(:(SAFE|CASH)//([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35})")
MT518_SequenceD_OtherParties_97A_Type_Pattern._InitializeFacetMap(MT518_SequenceD_OtherParties_97A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceD_OtherParties_97A_Type_Pattern', MT518_SequenceD_OtherParties_97A_Type_Pattern)
_module_typeBindings.MT518_SequenceD_OtherParties_97A_Type_Pattern = MT518_SequenceD_OtherParties_97A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceD_OtherParties_97B_Type_Pattern
class MT518_SequenceD_OtherParties_97B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceD_OtherParties_97B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1264, 1)
    _Documentation = None
MT518_SequenceD_OtherParties_97B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceD_OtherParties_97B_Type_Pattern._CF_pattern.addPattern(pattern="(:(SAFE)/([A-Z0-9]{1,8})?/[A-Z0-9]{4}/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35})")
MT518_SequenceD_OtherParties_97B_Type_Pattern._InitializeFacetMap(MT518_SequenceD_OtherParties_97B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceD_OtherParties_97B_Type_Pattern', MT518_SequenceD_OtherParties_97B_Type_Pattern)
_module_typeBindings.MT518_SequenceD_OtherParties_97B_Type_Pattern = MT518_SequenceD_OtherParties_97B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceD_OtherParties_97E_Type_Pattern
class MT518_SequenceD_OtherParties_97E_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceD_OtherParties_97E_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1277, 1)
    _Documentation = None
MT518_SequenceD_OtherParties_97E_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceD_OtherParties_97E_Type_Pattern._CF_pattern.addPattern(pattern="(:(CASH)//([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})")
MT518_SequenceD_OtherParties_97E_Type_Pattern._InitializeFacetMap(MT518_SequenceD_OtherParties_97E_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceD_OtherParties_97E_Type_Pattern', MT518_SequenceD_OtherParties_97E_Type_Pattern)
_module_typeBindings.MT518_SequenceD_OtherParties_97E_Type_Pattern = MT518_SequenceD_OtherParties_97E_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceD_OtherParties_70C_Type_Pattern
class MT518_SequenceD_OtherParties_70C_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceD_OtherParties_70C_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1290, 1)
    _Documentation = None
MT518_SequenceD_OtherParties_70C_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceD_OtherParties_70C_Type_Pattern._CF_pattern.addPattern(pattern="(:(PACO)//(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT518_SequenceD_OtherParties_70C_Type_Pattern._InitializeFacetMap(MT518_SequenceD_OtherParties_70C_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceD_OtherParties_70C_Type_Pattern', MT518_SequenceD_OtherParties_70C_Type_Pattern)
_module_typeBindings.MT518_SequenceD_OtherParties_70C_Type_Pattern = MT518_SequenceD_OtherParties_70C_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceD_OtherParties_20C_Type_Pattern
class MT518_SequenceD_OtherParties_20C_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceD_OtherParties_20C_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1303, 1)
    _Documentation = None
MT518_SequenceD_OtherParties_20C_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceD_OtherParties_20C_Type_Pattern._CF_pattern.addPattern(pattern="(:(PROC)//[^/]([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,16}[^/])")
MT518_SequenceD_OtherParties_20C_Type_Pattern._InitializeFacetMap(MT518_SequenceD_OtherParties_20C_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceD_OtherParties_20C_Type_Pattern', MT518_SequenceD_OtherParties_20C_Type_Pattern)
_module_typeBindings.MT518_SequenceD_OtherParties_20C_Type_Pattern = MT518_SequenceD_OtherParties_20C_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceE_TwoLegTransactionDetails_98A_Type_Pattern
class MT518_SequenceE_TwoLegTransactionDetails_98A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceE_TwoLegTransactionDetails_98A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1316, 1)
    _Documentation = None
MT518_SequenceE_TwoLegTransactionDetails_98A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceE_TwoLegTransactionDetails_98A_Type_Pattern._CF_pattern.addPattern(pattern='(:(TERM|RERA)//[0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01]))')
MT518_SequenceE_TwoLegTransactionDetails_98A_Type_Pattern._InitializeFacetMap(MT518_SequenceE_TwoLegTransactionDetails_98A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceE_TwoLegTransactionDetails_98A_Type_Pattern', MT518_SequenceE_TwoLegTransactionDetails_98A_Type_Pattern)
_module_typeBindings.MT518_SequenceE_TwoLegTransactionDetails_98A_Type_Pattern = MT518_SequenceE_TwoLegTransactionDetails_98A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceE_TwoLegTransactionDetails_98B_Type_Pattern
class MT518_SequenceE_TwoLegTransactionDetails_98B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceE_TwoLegTransactionDetails_98B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1329, 1)
    _Documentation = None
MT518_SequenceE_TwoLegTransactionDetails_98B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceE_TwoLegTransactionDetails_98B_Type_Pattern._CF_pattern.addPattern(pattern='(:(TERM)/([A-Z0-9]{1,8})?/[A-Z0-9]{4})')
MT518_SequenceE_TwoLegTransactionDetails_98B_Type_Pattern._InitializeFacetMap(MT518_SequenceE_TwoLegTransactionDetails_98B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceE_TwoLegTransactionDetails_98B_Type_Pattern', MT518_SequenceE_TwoLegTransactionDetails_98B_Type_Pattern)
_module_typeBindings.MT518_SequenceE_TwoLegTransactionDetails_98B_Type_Pattern = MT518_SequenceE_TwoLegTransactionDetails_98B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceE_TwoLegTransactionDetails_98C_Type_Pattern
class MT518_SequenceE_TwoLegTransactionDetails_98C_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceE_TwoLegTransactionDetails_98C_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1342, 1)
    _Documentation = None
MT518_SequenceE_TwoLegTransactionDetails_98C_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceE_TwoLegTransactionDetails_98C_Type_Pattern._CF_pattern.addPattern(pattern='(:(TERM|RERA)//[0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])(0[0-9]|[1][0-9]|2[1-3])([0-5][0-9])([0-5][0-9]))')
MT518_SequenceE_TwoLegTransactionDetails_98C_Type_Pattern._InitializeFacetMap(MT518_SequenceE_TwoLegTransactionDetails_98C_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceE_TwoLegTransactionDetails_98C_Type_Pattern', MT518_SequenceE_TwoLegTransactionDetails_98C_Type_Pattern)
_module_typeBindings.MT518_SequenceE_TwoLegTransactionDetails_98C_Type_Pattern = MT518_SequenceE_TwoLegTransactionDetails_98C_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceE_TwoLegTransactionDetails_22F_Type_Pattern
class MT518_SequenceE_TwoLegTransactionDetails_22F_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceE_TwoLegTransactionDetails_22F_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1355, 1)
    _Documentation = None
MT518_SequenceE_TwoLegTransactionDetails_22F_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceE_TwoLegTransactionDetails_22F_Type_Pattern._CF_pattern.addPattern(pattern='(:(RERT|MICO|REVA|LEGA)/([A-Z0-9]{1,8})?/[A-Z0-9]{4})')
MT518_SequenceE_TwoLegTransactionDetails_22F_Type_Pattern._InitializeFacetMap(MT518_SequenceE_TwoLegTransactionDetails_22F_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceE_TwoLegTransactionDetails_22F_Type_Pattern', MT518_SequenceE_TwoLegTransactionDetails_22F_Type_Pattern)
_module_typeBindings.MT518_SequenceE_TwoLegTransactionDetails_22F_Type_Pattern = MT518_SequenceE_TwoLegTransactionDetails_22F_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceE_TwoLegTransactionDetails_20C_Type_Pattern
class MT518_SequenceE_TwoLegTransactionDetails_20C_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceE_TwoLegTransactionDetails_20C_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1368, 1)
    _Documentation = None
MT518_SequenceE_TwoLegTransactionDetails_20C_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceE_TwoLegTransactionDetails_20C_Type_Pattern._CF_pattern.addPattern(pattern="(:(SECO|REPO)//[^/]([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,16}[^/])")
MT518_SequenceE_TwoLegTransactionDetails_20C_Type_Pattern._InitializeFacetMap(MT518_SequenceE_TwoLegTransactionDetails_20C_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceE_TwoLegTransactionDetails_20C_Type_Pattern', MT518_SequenceE_TwoLegTransactionDetails_20C_Type_Pattern)
_module_typeBindings.MT518_SequenceE_TwoLegTransactionDetails_20C_Type_Pattern = MT518_SequenceE_TwoLegTransactionDetails_20C_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceE_TwoLegTransactionDetails_92A_Type_Pattern
class MT518_SequenceE_TwoLegTransactionDetails_92A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceE_TwoLegTransactionDetails_92A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1381, 1)
    _Documentation = None
MT518_SequenceE_TwoLegTransactionDetails_92A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceE_TwoLegTransactionDetails_92A_Type_Pattern._CF_pattern.addPattern(pattern='(:(REPO|RSPR|PRIC|SLMG|SHAI)//(N)?[0-9,(?0-9)]{1,15})')
MT518_SequenceE_TwoLegTransactionDetails_92A_Type_Pattern._InitializeFacetMap(MT518_SequenceE_TwoLegTransactionDetails_92A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceE_TwoLegTransactionDetails_92A_Type_Pattern', MT518_SequenceE_TwoLegTransactionDetails_92A_Type_Pattern)
_module_typeBindings.MT518_SequenceE_TwoLegTransactionDetails_92A_Type_Pattern = MT518_SequenceE_TwoLegTransactionDetails_92A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceE_TwoLegTransactionDetails_92C_Type_Pattern
class MT518_SequenceE_TwoLegTransactionDetails_92C_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceE_TwoLegTransactionDetails_92C_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1394, 1)
    _Documentation = None
MT518_SequenceE_TwoLegTransactionDetails_92C_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceE_TwoLegTransactionDetails_92C_Type_Pattern._CF_pattern.addPattern(pattern="(:(VASU|PRIC)/([A-Z0-9]{1,8})?/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,24})")
MT518_SequenceE_TwoLegTransactionDetails_92C_Type_Pattern._InitializeFacetMap(MT518_SequenceE_TwoLegTransactionDetails_92C_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceE_TwoLegTransactionDetails_92C_Type_Pattern', MT518_SequenceE_TwoLegTransactionDetails_92C_Type_Pattern)
_module_typeBindings.MT518_SequenceE_TwoLegTransactionDetails_92C_Type_Pattern = MT518_SequenceE_TwoLegTransactionDetails_92C_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceE_TwoLegTransactionDetails_99B_Type_Pattern
class MT518_SequenceE_TwoLegTransactionDetails_99B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceE_TwoLegTransactionDetails_99B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1407, 1)
    _Documentation = None
MT518_SequenceE_TwoLegTransactionDetails_99B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceE_TwoLegTransactionDetails_99B_Type_Pattern._CF_pattern.addPattern(pattern='(:(CADE|TOCO)//[0-9]{3})')
MT518_SequenceE_TwoLegTransactionDetails_99B_Type_Pattern._InitializeFacetMap(MT518_SequenceE_TwoLegTransactionDetails_99B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceE_TwoLegTransactionDetails_99B_Type_Pattern', MT518_SequenceE_TwoLegTransactionDetails_99B_Type_Pattern)
_module_typeBindings.MT518_SequenceE_TwoLegTransactionDetails_99B_Type_Pattern = MT518_SequenceE_TwoLegTransactionDetails_99B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceE_TwoLegTransactionDetails_19A_Type_Pattern
class MT518_SequenceE_TwoLegTransactionDetails_19A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceE_TwoLegTransactionDetails_19A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1420, 1)
    _Documentation = None
MT518_SequenceE_TwoLegTransactionDetails_19A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceE_TwoLegTransactionDetails_19A_Type_Pattern._CF_pattern.addPattern(pattern='(:(FORF|TRTE|REPP|ACRU|DEAL|TAPC)//(N)?(ACTU|DISC|PREM)/(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})')
MT518_SequenceE_TwoLegTransactionDetails_19A_Type_Pattern._InitializeFacetMap(MT518_SequenceE_TwoLegTransactionDetails_19A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceE_TwoLegTransactionDetails_19A_Type_Pattern', MT518_SequenceE_TwoLegTransactionDetails_19A_Type_Pattern)
_module_typeBindings.MT518_SequenceE_TwoLegTransactionDetails_19A_Type_Pattern = MT518_SequenceE_TwoLegTransactionDetails_19A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT518_SequenceE_TwoLegTransactionDetails_70C_Type_Pattern
class MT518_SequenceE_TwoLegTransactionDetails_70C_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceE_TwoLegTransactionDetails_70C_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1433, 1)
    _Documentation = None
MT518_SequenceE_TwoLegTransactionDetails_70C_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT518_SequenceE_TwoLegTransactionDetails_70C_Type_Pattern._CF_pattern.addPattern(pattern="(:(SECO)//(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT518_SequenceE_TwoLegTransactionDetails_70C_Type_Pattern._InitializeFacetMap(MT518_SequenceE_TwoLegTransactionDetails_70C_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceE_TwoLegTransactionDetails_70C_Type_Pattern', MT518_SequenceE_TwoLegTransactionDetails_70C_Type_Pattern)
_module_typeBindings.MT518_SequenceE_TwoLegTransactionDetails_70C_Type_Pattern = MT518_SequenceE_TwoLegTransactionDetails_70C_Type_Pattern

# Complex type {http://www.w3schools.com}MT518_SequenceA_GeneralInformation with content type ELEMENT_ONLY
class MT518_SequenceA_GeneralInformation (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceA_GeneralInformation with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceA_GeneralInformation')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1446, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}SendersMessageReference uses Python identifier SendersMessageReference
    __SendersMessageReference = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SendersMessageReference'), 'SendersMessageReference', '__httpwww_w3schools_com_MT518_SequenceA_GeneralInformation_httpwww_w3schools_comSendersMessageReference', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1448, 3), )

    
    SendersMessageReference = property(__SendersMessageReference.value, __SendersMessageReference.set, None, None)

    
    # Element {http://www.w3schools.com}FunctionOfTheMessage uses Python identifier FunctionOfTheMessage
    __FunctionOfTheMessage = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'FunctionOfTheMessage'), 'FunctionOfTheMessage', '__httpwww_w3schools_com_MT518_SequenceA_GeneralInformation_httpwww_w3schools_comFunctionOfTheMessage', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1449, 3), )

    
    FunctionOfTheMessage = property(__FunctionOfTheMessage.value, __FunctionOfTheMessage.set, None, None)

    
    # Element {http://www.w3schools.com}PreparationDateTime_A uses Python identifier PreparationDateTime_A
    __PreparationDateTime_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PreparationDateTime_A'), 'PreparationDateTime_A', '__httpwww_w3schools_com_MT518_SequenceA_GeneralInformation_httpwww_w3schools_comPreparationDateTime_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1451, 4), )

    
    PreparationDateTime_A = property(__PreparationDateTime_A.value, __PreparationDateTime_A.set, None, None)

    
    # Element {http://www.w3schools.com}PreparationDateTime_C uses Python identifier PreparationDateTime_C
    __PreparationDateTime_C = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PreparationDateTime_C'), 'PreparationDateTime_C', '__httpwww_w3schools_com_MT518_SequenceA_GeneralInformation_httpwww_w3schools_comPreparationDateTime_C', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1452, 4), )

    
    PreparationDateTime_C = property(__PreparationDateTime_C.value, __PreparationDateTime_C.set, None, None)

    
    # Element {http://www.w3schools.com}PreparationDateTime_E uses Python identifier PreparationDateTime_E
    __PreparationDateTime_E = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PreparationDateTime_E'), 'PreparationDateTime_E', '__httpwww_w3schools_com_MT518_SequenceA_GeneralInformation_httpwww_w3schools_comPreparationDateTime_E', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1453, 4), )

    
    PreparationDateTime_E = property(__PreparationDateTime_E.value, __PreparationDateTime_E.set, None, None)

    
    # Element {http://www.w3schools.com}TradeTransactionType uses Python identifier TradeTransactionType
    __TradeTransactionType = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'TradeTransactionType'), 'TradeTransactionType', '__httpwww_w3schools_com_MT518_SequenceA_GeneralInformation_httpwww_w3schools_comTradeTransactionType', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1455, 3), )

    
    TradeTransactionType = property(__TradeTransactionType.value, __TradeTransactionType.set, None, None)

    
    # Element {http://www.w3schools.com}SubSequenceA1_Linkages uses Python identifier SubSequenceA1_Linkages
    __SubSequenceA1_Linkages = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SubSequenceA1_Linkages'), 'SubSequenceA1_Linkages', '__httpwww_w3schools_com_MT518_SequenceA_GeneralInformation_httpwww_w3schools_comSubSequenceA1_Linkages', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1456, 3), )

    
    SubSequenceA1_Linkages = property(__SubSequenceA1_Linkages.value, __SubSequenceA1_Linkages.set, None, None)

    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceA_GeneralInformation_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='16R')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1458, 2)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1458, 2)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceA_GeneralInformation_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1459, 2)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1459, 2)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    
    # Attribute formatTag uses Python identifier formatTag
    __formatTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'formatTag'), 'formatTag', '__httpwww_w3schools_com_MT518_SequenceA_GeneralInformation_formatTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='GENL')
    __formatTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1460, 2)
    __formatTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1460, 2)
    
    formatTag = property(__formatTag.value, __formatTag.set, None, None)

    _ElementMap.update({
        __SendersMessageReference.name() : __SendersMessageReference,
        __FunctionOfTheMessage.name() : __FunctionOfTheMessage,
        __PreparationDateTime_A.name() : __PreparationDateTime_A,
        __PreparationDateTime_C.name() : __PreparationDateTime_C,
        __PreparationDateTime_E.name() : __PreparationDateTime_E,
        __TradeTransactionType.name() : __TradeTransactionType,
        __SubSequenceA1_Linkages.name() : __SubSequenceA1_Linkages
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory,
        __formatTag.name() : __formatTag
    })
_module_typeBindings.MT518_SequenceA_GeneralInformation = MT518_SequenceA_GeneralInformation
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceA_GeneralInformation', MT518_SequenceA_GeneralInformation)


# Complex type {http://www.w3schools.com}MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages with content type ELEMENT_ONLY
class MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1462, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}LinkedMessage_A uses Python identifier LinkedMessage_A
    __LinkedMessage_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'LinkedMessage_A'), 'LinkedMessage_A', '__httpwww_w3schools_com_MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_httpwww_w3schools_comLinkedMessage_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1465, 4), )

    
    LinkedMessage_A = property(__LinkedMessage_A.value, __LinkedMessage_A.set, None, None)

    
    # Element {http://www.w3schools.com}LinkedMessage_B uses Python identifier LinkedMessage_B
    __LinkedMessage_B = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'LinkedMessage_B'), 'LinkedMessage_B', '__httpwww_w3schools_com_MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_httpwww_w3schools_comLinkedMessage_B', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1466, 4), )

    
    LinkedMessage_B = property(__LinkedMessage_B.value, __LinkedMessage_B.set, None, None)

    
    # Element {http://www.w3schools.com}Reference_C uses Python identifier Reference_C
    __Reference_C = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Reference_C'), 'Reference_C', '__httpwww_w3schools_com_MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_httpwww_w3schools_comReference_C', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1469, 4), )

    
    Reference_C = property(__Reference_C.value, __Reference_C.set, None, None)

    
    # Element {http://www.w3schools.com}Reference_U uses Python identifier Reference_U
    __Reference_U = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Reference_U'), 'Reference_U', '__httpwww_w3schools_com_MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_httpwww_w3schools_comReference_U', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1470, 4), )

    
    Reference_U = property(__Reference_U.value, __Reference_U.set, None, None)

    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='16R')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1473, 2)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1473, 2)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1474, 2)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1474, 2)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    
    # Attribute formatTag uses Python identifier formatTag
    __formatTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'formatTag'), 'formatTag', '__httpwww_w3schools_com_MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_formatTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='LINK')
    __formatTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1475, 2)
    __formatTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1475, 2)
    
    formatTag = property(__formatTag.value, __formatTag.set, None, None)

    _ElementMap.update({
        __LinkedMessage_A.name() : __LinkedMessage_A,
        __LinkedMessage_B.name() : __LinkedMessage_B,
        __Reference_C.name() : __Reference_C,
        __Reference_U.name() : __Reference_U
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory,
        __formatTag.name() : __formatTag
    })
_module_typeBindings.MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages = MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages', MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages)


# Complex type {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails with content type ELEMENT_ONLY
class MT518_SequenceB_ConfirmationDetails (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceB_ConfirmationDetails')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1477, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}DateTime_A uses Python identifier DateTime_A
    __DateTime_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'DateTime_A'), 'DateTime_A', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_httpwww_w3schools_comDateTime_A', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1480, 4), )

    
    DateTime_A = property(__DateTime_A.value, __DateTime_A.set, None, None)

    
    # Element {http://www.w3schools.com}DateTime_B uses Python identifier DateTime_B
    __DateTime_B = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'DateTime_B'), 'DateTime_B', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_httpwww_w3schools_comDateTime_B', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1481, 4), )

    
    DateTime_B = property(__DateTime_B.value, __DateTime_B.set, None, None)

    
    # Element {http://www.w3schools.com}DateTime_C uses Python identifier DateTime_C
    __DateTime_C = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'DateTime_C'), 'DateTime_C', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_httpwww_w3schools_comDateTime_C', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1482, 4), )

    
    DateTime_C = property(__DateTime_C.value, __DateTime_C.set, None, None)

    
    # Element {http://www.w3schools.com}DateTime_E uses Python identifier DateTime_E
    __DateTime_E = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'DateTime_E'), 'DateTime_E', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_httpwww_w3schools_comDateTime_E', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1483, 4), )

    
    DateTime_E = property(__DateTime_E.value, __DateTime_E.set, None, None)

    
    # Element {http://www.w3schools.com}DealPrice_A uses Python identifier DealPrice_A
    __DealPrice_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'DealPrice_A'), 'DealPrice_A', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_httpwww_w3schools_comDealPrice_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1486, 4), )

    
    DealPrice_A = property(__DealPrice_A.value, __DealPrice_A.set, None, None)

    
    # Element {http://www.w3schools.com}DealPrice_B uses Python identifier DealPrice_B
    __DealPrice_B = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'DealPrice_B'), 'DealPrice_B', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_httpwww_w3schools_comDealPrice_B', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1487, 4), )

    
    DealPrice_B = property(__DealPrice_B.value, __DealPrice_B.set, None, None)

    
    # Element {http://www.w3schools.com}Rate uses Python identifier Rate
    __Rate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Rate'), 'Rate', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_httpwww_w3schools_comRate', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1489, 3), )

    
    Rate = property(__Rate.value, __Rate.set, None, None)

    
    # Element {http://www.w3schools.com}NumberCount uses Python identifier NumberCount
    __NumberCount = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'NumberCount'), 'NumberCount', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_httpwww_w3schools_comNumberCount', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1490, 3), )

    
    NumberCount = property(__NumberCount.value, __NumberCount.set, None, None)

    
    # Element {http://www.w3schools.com}Place_B uses Python identifier Place_B
    __Place_B = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Place_B'), 'Place_B', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_httpwww_w3schools_comPlace_B', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1492, 4), )

    
    Place_B = property(__Place_B.value, __Place_B.set, None, None)

    
    # Element {http://www.w3schools.com}Place_C uses Python identifier Place_C
    __Place_C = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Place_C'), 'Place_C', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_httpwww_w3schools_comPlace_C', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1493, 4), )

    
    Place_C = property(__Place_C.value, __Place_C.set, None, None)

    
    # Element {http://www.w3schools.com}Place_F uses Python identifier Place_F
    __Place_F = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Place_F'), 'Place_F', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_httpwww_w3schools_comPlace_F', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1494, 4), )

    
    Place_F = property(__Place_F.value, __Place_F.set, None, None)

    
    # Element {http://www.w3schools.com}Place_L uses Python identifier Place_L
    __Place_L = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Place_L'), 'Place_L', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_httpwww_w3schools_comPlace_L', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1495, 4), )

    
    Place_L = property(__Place_L.value, __Place_L.set, None, None)

    
    # Element {http://www.w3schools.com}SettlementAmount uses Python identifier SettlementAmount
    __SettlementAmount = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SettlementAmount'), 'SettlementAmount', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_httpwww_w3schools_comSettlementAmount', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1497, 3), )

    
    SettlementAmount = property(__SettlementAmount.value, __SettlementAmount.set, None, None)

    
    # Element {http://www.w3schools.com}Indicator_F uses Python identifier Indicator_F
    __Indicator_F = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Indicator_F'), 'Indicator_F', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_httpwww_w3schools_comIndicator_F', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1499, 4), )

    
    Indicator_F = property(__Indicator_F.value, __Indicator_F.set, None, None)

    
    # Element {http://www.w3schools.com}Indicator_H uses Python identifier Indicator_H
    __Indicator_H = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Indicator_H'), 'Indicator_H', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_httpwww_w3schools_comIndicator_H', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1500, 4), )

    
    Indicator_H = property(__Indicator_H.value, __Indicator_H.set, None, None)

    
    # Element {http://www.w3schools.com}Currency uses Python identifier Currency
    __Currency = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Currency'), 'Currency', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_httpwww_w3schools_comCurrency', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1502, 3), )

    
    Currency = property(__Currency.value, __Currency.set, None, None)

    
    # Element {http://www.w3schools.com}SubSequenceB1_ConfirmationParties uses Python identifier SubSequenceB1_ConfirmationParties
    __SubSequenceB1_ConfirmationParties = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SubSequenceB1_ConfirmationParties'), 'SubSequenceB1_ConfirmationParties', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_httpwww_w3schools_comSubSequenceB1_ConfirmationParties', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1503, 3), )

    
    SubSequenceB1_ConfirmationParties = property(__SubSequenceB1_ConfirmationParties.value, __SubSequenceB1_ConfirmationParties.set, None, None)

    
    # Element {http://www.w3schools.com}QuantityOfFinancialInstrument uses Python identifier QuantityOfFinancialInstrument
    __QuantityOfFinancialInstrument = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'QuantityOfFinancialInstrument'), 'QuantityOfFinancialInstrument', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_httpwww_w3schools_comQuantityOfFinancialInstrument', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1504, 3), )

    
    QuantityOfFinancialInstrument = property(__QuantityOfFinancialInstrument.value, __QuantityOfFinancialInstrument.set, None, None)

    
    # Element {http://www.w3schools.com}IdentificationOfTheFinancialInstrument uses Python identifier IdentificationOfTheFinancialInstrument
    __IdentificationOfTheFinancialInstrument = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'IdentificationOfTheFinancialInstrument'), 'IdentificationOfTheFinancialInstrument', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_httpwww_w3schools_comIdentificationOfTheFinancialInstrument', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1505, 3), )

    
    IdentificationOfTheFinancialInstrument = property(__IdentificationOfTheFinancialInstrument.value, __IdentificationOfTheFinancialInstrument.set, None, None)

    
    # Element {http://www.w3schools.com}SubSequenceB2_FinancialInstrumentAttribute uses Python identifier SubSequenceB2_FinancialInstrumentAttribute
    __SubSequenceB2_FinancialInstrumentAttribute = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SubSequenceB2_FinancialInstrumentAttribute'), 'SubSequenceB2_FinancialInstrumentAttribute', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_httpwww_w3schools_comSubSequenceB2_FinancialInstrumentAttribute', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1506, 3), )

    
    SubSequenceB2_FinancialInstrumentAttribute = property(__SubSequenceB2_FinancialInstrumentAttribute.value, __SubSequenceB2_FinancialInstrumentAttribute.set, None, None)

    
    # Element {http://www.w3schools.com}CertificateNumber uses Python identifier CertificateNumber
    __CertificateNumber = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'CertificateNumber'), 'CertificateNumber', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_httpwww_w3schools_comCertificateNumber', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1507, 3), )

    
    CertificateNumber = property(__CertificateNumber.value, __CertificateNumber.set, None, None)

    
    # Element {http://www.w3schools.com}Narrative uses Python identifier Narrative
    __Narrative = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Narrative'), 'Narrative', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_httpwww_w3schools_comNarrative', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1508, 3), )

    
    Narrative = property(__Narrative.value, __Narrative.set, None, None)

    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='16R')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1510, 2)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1510, 2)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1511, 2)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1511, 2)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    
    # Attribute formatTag uses Python identifier formatTag
    __formatTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'formatTag'), 'formatTag', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_formatTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='CONFDET')
    __formatTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1512, 2)
    __formatTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1512, 2)
    
    formatTag = property(__formatTag.value, __formatTag.set, None, None)

    _ElementMap.update({
        __DateTime_A.name() : __DateTime_A,
        __DateTime_B.name() : __DateTime_B,
        __DateTime_C.name() : __DateTime_C,
        __DateTime_E.name() : __DateTime_E,
        __DealPrice_A.name() : __DealPrice_A,
        __DealPrice_B.name() : __DealPrice_B,
        __Rate.name() : __Rate,
        __NumberCount.name() : __NumberCount,
        __Place_B.name() : __Place_B,
        __Place_C.name() : __Place_C,
        __Place_F.name() : __Place_F,
        __Place_L.name() : __Place_L,
        __SettlementAmount.name() : __SettlementAmount,
        __Indicator_F.name() : __Indicator_F,
        __Indicator_H.name() : __Indicator_H,
        __Currency.name() : __Currency,
        __SubSequenceB1_ConfirmationParties.name() : __SubSequenceB1_ConfirmationParties,
        __QuantityOfFinancialInstrument.name() : __QuantityOfFinancialInstrument,
        __IdentificationOfTheFinancialInstrument.name() : __IdentificationOfTheFinancialInstrument,
        __SubSequenceB2_FinancialInstrumentAttribute.name() : __SubSequenceB2_FinancialInstrumentAttribute,
        __CertificateNumber.name() : __CertificateNumber,
        __Narrative.name() : __Narrative
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory,
        __formatTag.name() : __formatTag
    })
_module_typeBindings.MT518_SequenceB_ConfirmationDetails = MT518_SequenceB_ConfirmationDetails
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceB_ConfirmationDetails', MT518_SequenceB_ConfirmationDetails)


# Complex type {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties with content type ELEMENT_ONLY
class MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1514, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}PARTY_L uses Python identifier PARTY_L
    __PARTY_L = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PARTY_L'), 'PARTY_L', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_httpwww_w3schools_comPARTY_L', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1517, 4), )

    
    PARTY_L = property(__PARTY_L.value, __PARTY_L.set, None, None)

    
    # Element {http://www.w3schools.com}PARTY_P uses Python identifier PARTY_P
    __PARTY_P = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PARTY_P'), 'PARTY_P', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_httpwww_w3schools_comPARTY_P', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1518, 4), )

    
    PARTY_P = property(__PARTY_P.value, __PARTY_P.set, None, None)

    
    # Element {http://www.w3schools.com}PARTY_Q uses Python identifier PARTY_Q
    __PARTY_Q = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PARTY_Q'), 'PARTY_Q', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_httpwww_w3schools_comPARTY_Q', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1519, 4), )

    
    PARTY_Q = property(__PARTY_Q.value, __PARTY_Q.set, None, None)

    
    # Element {http://www.w3schools.com}PARTY_R uses Python identifier PARTY_R
    __PARTY_R = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PARTY_R'), 'PARTY_R', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_httpwww_w3schools_comPARTY_R', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1520, 4), )

    
    PARTY_R = property(__PARTY_R.value, __PARTY_R.set, None, None)

    
    # Element {http://www.w3schools.com}PARTY_S uses Python identifier PARTY_S
    __PARTY_S = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PARTY_S'), 'PARTY_S', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_httpwww_w3schools_comPARTY_S', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1521, 4), )

    
    PARTY_S = property(__PARTY_S.value, __PARTY_S.set, None, None)

    
    # Element {http://www.w3schools.com}Account_A uses Python identifier Account_A
    __Account_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Account_A'), 'Account_A', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_httpwww_w3schools_comAccount_A', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1524, 4), )

    
    Account_A = property(__Account_A.value, __Account_A.set, None, None)

    
    # Element {http://www.w3schools.com}Account_B uses Python identifier Account_B
    __Account_B = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Account_B'), 'Account_B', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_httpwww_w3schools_comAccount_B', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1525, 4), )

    
    Account_B = property(__Account_B.value, __Account_B.set, None, None)

    
    # Element {http://www.w3schools.com}Account_E uses Python identifier Account_E
    __Account_E = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Account_E'), 'Account_E', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_httpwww_w3schools_comAccount_E', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1526, 4), )

    
    Account_E = property(__Account_E.value, __Account_E.set, None, None)

    
    # Element {http://www.w3schools.com}ProcessingDateTime_A uses Python identifier ProcessingDateTime_A
    __ProcessingDateTime_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ProcessingDateTime_A'), 'ProcessingDateTime_A', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_httpwww_w3schools_comProcessingDateTime_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1529, 4), )

    
    ProcessingDateTime_A = property(__ProcessingDateTime_A.value, __ProcessingDateTime_A.set, None, None)

    
    # Element {http://www.w3schools.com}ProcessingDateTime_C uses Python identifier ProcessingDateTime_C
    __ProcessingDateTime_C = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ProcessingDateTime_C'), 'ProcessingDateTime_C', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_httpwww_w3schools_comProcessingDateTime_C', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1530, 4), )

    
    ProcessingDateTime_C = property(__ProcessingDateTime_C.value, __ProcessingDateTime_C.set, None, None)

    
    # Element {http://www.w3schools.com}ProcessingReference uses Python identifier ProcessingReference
    __ProcessingReference = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ProcessingReference'), 'ProcessingReference', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_httpwww_w3schools_comProcessingReference', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1532, 3), )

    
    ProcessingReference = property(__ProcessingReference.value, __ProcessingReference.set, None, None)

    
    # Element {http://www.w3schools.com}Narrative_C uses Python identifier Narrative_C
    __Narrative_C = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Narrative_C'), 'Narrative_C', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_httpwww_w3schools_comNarrative_C', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1534, 4), )

    
    Narrative_C = property(__Narrative_C.value, __Narrative_C.set, None, None)

    
    # Element {http://www.w3schools.com}Narrative_E uses Python identifier Narrative_E
    __Narrative_E = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Narrative_E'), 'Narrative_E', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_httpwww_w3schools_comNarrative_E', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1535, 4), )

    
    Narrative_E = property(__Narrative_E.value, __Narrative_E.set, None, None)

    
    # Element {http://www.w3schools.com}Indicator uses Python identifier Indicator
    __Indicator = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Indicator'), 'Indicator', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_httpwww_w3schools_comIndicator', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1537, 3), )

    
    Indicator = property(__Indicator.value, __Indicator.set, None, None)

    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='16R')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1539, 2)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1539, 2)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1540, 2)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1540, 2)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    
    # Attribute formatTag uses Python identifier formatTag
    __formatTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'formatTag'), 'formatTag', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_formatTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='CONFPRTY')
    __formatTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1541, 2)
    __formatTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1541, 2)
    
    formatTag = property(__formatTag.value, __formatTag.set, None, None)

    _ElementMap.update({
        __PARTY_L.name() : __PARTY_L,
        __PARTY_P.name() : __PARTY_P,
        __PARTY_Q.name() : __PARTY_Q,
        __PARTY_R.name() : __PARTY_R,
        __PARTY_S.name() : __PARTY_S,
        __Account_A.name() : __Account_A,
        __Account_B.name() : __Account_B,
        __Account_E.name() : __Account_E,
        __ProcessingDateTime_A.name() : __ProcessingDateTime_A,
        __ProcessingDateTime_C.name() : __ProcessingDateTime_C,
        __ProcessingReference.name() : __ProcessingReference,
        __Narrative_C.name() : __Narrative_C,
        __Narrative_E.name() : __Narrative_E,
        __Indicator.name() : __Indicator
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory,
        __formatTag.name() : __formatTag
    })
_module_typeBindings.MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties = MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties', MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties)


# Complex type {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute with content type ELEMENT_ONLY
class MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1543, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}PlaceOfListing uses Python identifier PlaceOfListing
    __PlaceOfListing = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PlaceOfListing'), 'PlaceOfListing', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_httpwww_w3schools_comPlaceOfListing', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1545, 3), )

    
    PlaceOfListing = property(__PlaceOfListing.value, __PlaceOfListing.set, None, None)

    
    # Element {http://www.w3schools.com}Indicator uses Python identifier Indicator
    __Indicator = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Indicator'), 'Indicator', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_httpwww_w3schools_comIndicator', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1546, 3), )

    
    Indicator = property(__Indicator.value, __Indicator.set, None, None)

    
    # Element {http://www.w3schools.com}TypeOfFinancialInstrument_A uses Python identifier TypeOfFinancialInstrument_A
    __TypeOfFinancialInstrument_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'TypeOfFinancialInstrument_A'), 'TypeOfFinancialInstrument_A', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_httpwww_w3schools_comTypeOfFinancialInstrument_A', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1548, 4), )

    
    TypeOfFinancialInstrument_A = property(__TypeOfFinancialInstrument_A.value, __TypeOfFinancialInstrument_A.set, None, None)

    
    # Element {http://www.w3schools.com}TypeOfFinancialInstrument_B uses Python identifier TypeOfFinancialInstrument_B
    __TypeOfFinancialInstrument_B = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'TypeOfFinancialInstrument_B'), 'TypeOfFinancialInstrument_B', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_httpwww_w3schools_comTypeOfFinancialInstrument_B', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1549, 4), )

    
    TypeOfFinancialInstrument_B = property(__TypeOfFinancialInstrument_B.value, __TypeOfFinancialInstrument_B.set, None, None)

    
    # Element {http://www.w3schools.com}TypeOfFinancialInstrument_C uses Python identifier TypeOfFinancialInstrument_C
    __TypeOfFinancialInstrument_C = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'TypeOfFinancialInstrument_C'), 'TypeOfFinancialInstrument_C', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_httpwww_w3schools_comTypeOfFinancialInstrument_C', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1550, 4), )

    
    TypeOfFinancialInstrument_C = property(__TypeOfFinancialInstrument_C.value, __TypeOfFinancialInstrument_C.set, None, None)

    
    # Element {http://www.w3schools.com}CurrencyOfDenomination uses Python identifier CurrencyOfDenomination
    __CurrencyOfDenomination = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'CurrencyOfDenomination'), 'CurrencyOfDenomination', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_httpwww_w3schools_comCurrencyOfDenomination', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1552, 3), )

    
    CurrencyOfDenomination = property(__CurrencyOfDenomination.value, __CurrencyOfDenomination.set, None, None)

    
    # Element {http://www.w3schools.com}DateTime uses Python identifier DateTime
    __DateTime = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'DateTime'), 'DateTime', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_httpwww_w3schools_comDateTime', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1553, 3), )

    
    DateTime = property(__DateTime.value, __DateTime.set, None, None)

    
    # Element {http://www.w3schools.com}Rate uses Python identifier Rate
    __Rate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Rate'), 'Rate', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_httpwww_w3schools_comRate', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1554, 3), )

    
    Rate = property(__Rate.value, __Rate.set, None, None)

    
    # Element {http://www.w3schools.com}NumberIdentification_A uses Python identifier NumberIdentification_A
    __NumberIdentification_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'NumberIdentification_A'), 'NumberIdentification_A', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_httpwww_w3schools_comNumberIdentification_A', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1556, 4), )

    
    NumberIdentification_A = property(__NumberIdentification_A.value, __NumberIdentification_A.set, None, None)

    
    # Element {http://www.w3schools.com}NumberIdentification_B uses Python identifier NumberIdentification_B
    __NumberIdentification_B = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'NumberIdentification_B'), 'NumberIdentification_B', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_httpwww_w3schools_comNumberIdentification_B', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1557, 4), )

    
    NumberIdentification_B = property(__NumberIdentification_B.value, __NumberIdentification_B.set, None, None)

    
    # Element {http://www.w3schools.com}Flag uses Python identifier Flag
    __Flag = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Flag'), 'Flag', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_httpwww_w3schools_comFlag', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1559, 3), )

    
    Flag = property(__Flag.value, __Flag.set, None, None)

    
    # Element {http://www.w3schools.com}Price_A uses Python identifier Price_A
    __Price_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Price_A'), 'Price_A', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_httpwww_w3schools_comPrice_A', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1561, 4), )

    
    Price_A = property(__Price_A.value, __Price_A.set, None, None)

    
    # Element {http://www.w3schools.com}Price_B uses Python identifier Price_B
    __Price_B = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Price_B'), 'Price_B', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_httpwww_w3schools_comPrice_B', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1562, 4), )

    
    Price_B = property(__Price_B.value, __Price_B.set, None, None)

    
    # Element {http://www.w3schools.com}QuantityOfFinancialInstrument uses Python identifier QuantityOfFinancialInstrument
    __QuantityOfFinancialInstrument = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'QuantityOfFinancialInstrument'), 'QuantityOfFinancialInstrument', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_httpwww_w3schools_comQuantityOfFinancialInstrument', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1564, 3), )

    
    QuantityOfFinancialInstrument = property(__QuantityOfFinancialInstrument.value, __QuantityOfFinancialInstrument.set, None, None)

    
    # Element {http://www.w3schools.com}IdentificationOfTheFinancialInstrument uses Python identifier IdentificationOfTheFinancialInstrument
    __IdentificationOfTheFinancialInstrument = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'IdentificationOfTheFinancialInstrument'), 'IdentificationOfTheFinancialInstrument', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_httpwww_w3schools_comIdentificationOfTheFinancialInstrument', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1565, 3), )

    
    IdentificationOfTheFinancialInstrument = property(__IdentificationOfTheFinancialInstrument.value, __IdentificationOfTheFinancialInstrument.set, None, None)

    
    # Element {http://www.w3schools.com}FinancialInstrumentAttributeNarrative uses Python identifier FinancialInstrumentAttributeNarrative
    __FinancialInstrumentAttributeNarrative = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'FinancialInstrumentAttributeNarrative'), 'FinancialInstrumentAttributeNarrative', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_httpwww_w3schools_comFinancialInstrumentAttributeNarrative', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1566, 3), )

    
    FinancialInstrumentAttributeNarrative = property(__FinancialInstrumentAttributeNarrative.value, __FinancialInstrumentAttributeNarrative.set, None, None)

    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='16R')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1568, 2)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1568, 2)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1569, 2)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1569, 2)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    
    # Attribute formatTag uses Python identifier formatTag
    __formatTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'formatTag'), 'formatTag', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_formatTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='FIA')
    __formatTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1570, 2)
    __formatTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1570, 2)
    
    formatTag = property(__formatTag.value, __formatTag.set, None, None)

    _ElementMap.update({
        __PlaceOfListing.name() : __PlaceOfListing,
        __Indicator.name() : __Indicator,
        __TypeOfFinancialInstrument_A.name() : __TypeOfFinancialInstrument_A,
        __TypeOfFinancialInstrument_B.name() : __TypeOfFinancialInstrument_B,
        __TypeOfFinancialInstrument_C.name() : __TypeOfFinancialInstrument_C,
        __CurrencyOfDenomination.name() : __CurrencyOfDenomination,
        __DateTime.name() : __DateTime,
        __Rate.name() : __Rate,
        __NumberIdentification_A.name() : __NumberIdentification_A,
        __NumberIdentification_B.name() : __NumberIdentification_B,
        __Flag.name() : __Flag,
        __Price_A.name() : __Price_A,
        __Price_B.name() : __Price_B,
        __QuantityOfFinancialInstrument.name() : __QuantityOfFinancialInstrument,
        __IdentificationOfTheFinancialInstrument.name() : __IdentificationOfTheFinancialInstrument,
        __FinancialInstrumentAttributeNarrative.name() : __FinancialInstrumentAttributeNarrative
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory,
        __formatTag.name() : __formatTag
    })
_module_typeBindings.MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute = MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute', MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute)


# Complex type {http://www.w3schools.com}MT518_SequenceC_SettlementDetails with content type ELEMENT_ONLY
class MT518_SequenceC_SettlementDetails (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceC_SettlementDetails with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceC_SettlementDetails')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1572, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}Indicator uses Python identifier Indicator
    __Indicator = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Indicator'), 'Indicator', '__httpwww_w3schools_com_MT518_SequenceC_SettlementDetails_httpwww_w3schools_comIndicator', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1574, 3), )

    
    Indicator = property(__Indicator.value, __Indicator.set, None, None)

    
    # Element {http://www.w3schools.com}Currency uses Python identifier Currency
    __Currency = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Currency'), 'Currency', '__httpwww_w3schools_com_MT518_SequenceC_SettlementDetails_httpwww_w3schools_comCurrency', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1575, 3), )

    
    Currency = property(__Currency.value, __Currency.set, None, None)

    
    # Element {http://www.w3schools.com}SubSequenceC1_SettlementParties uses Python identifier SubSequenceC1_SettlementParties
    __SubSequenceC1_SettlementParties = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SubSequenceC1_SettlementParties'), 'SubSequenceC1_SettlementParties', '__httpwww_w3schools_com_MT518_SequenceC_SettlementDetails_httpwww_w3schools_comSubSequenceC1_SettlementParties', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1576, 3), )

    
    SubSequenceC1_SettlementParties = property(__SubSequenceC1_SettlementParties.value, __SubSequenceC1_SettlementParties.set, None, None)

    
    # Element {http://www.w3schools.com}SubSequenceC2_CashParties uses Python identifier SubSequenceC2_CashParties
    __SubSequenceC2_CashParties = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SubSequenceC2_CashParties'), 'SubSequenceC2_CashParties', '__httpwww_w3schools_com_MT518_SequenceC_SettlementDetails_httpwww_w3schools_comSubSequenceC2_CashParties', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1577, 3), )

    
    SubSequenceC2_CashParties = property(__SubSequenceC2_CashParties.value, __SubSequenceC2_CashParties.set, None, None)

    
    # Element {http://www.w3schools.com}SubSequenceC3_Amounts uses Python identifier SubSequenceC3_Amounts
    __SubSequenceC3_Amounts = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SubSequenceC3_Amounts'), 'SubSequenceC3_Amounts', '__httpwww_w3schools_com_MT518_SequenceC_SettlementDetails_httpwww_w3schools_comSubSequenceC3_Amounts', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1578, 3), )

    
    SubSequenceC3_Amounts = property(__SubSequenceC3_Amounts.value, __SubSequenceC3_Amounts.set, None, None)

    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceC_SettlementDetails_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='16R')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1580, 2)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1580, 2)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceC_SettlementDetails_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1581, 2)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1581, 2)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    
    # Attribute formatTag uses Python identifier formatTag
    __formatTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'formatTag'), 'formatTag', '__httpwww_w3schools_com_MT518_SequenceC_SettlementDetails_formatTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='SETDET')
    __formatTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1582, 2)
    __formatTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1582, 2)
    
    formatTag = property(__formatTag.value, __formatTag.set, None, None)

    _ElementMap.update({
        __Indicator.name() : __Indicator,
        __Currency.name() : __Currency,
        __SubSequenceC1_SettlementParties.name() : __SubSequenceC1_SettlementParties,
        __SubSequenceC2_CashParties.name() : __SubSequenceC2_CashParties,
        __SubSequenceC3_Amounts.name() : __SubSequenceC3_Amounts
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory,
        __formatTag.name() : __formatTag
    })
_module_typeBindings.MT518_SequenceC_SettlementDetails = MT518_SequenceC_SettlementDetails
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceC_SettlementDetails', MT518_SequenceC_SettlementDetails)


# Complex type {http://www.w3schools.com}MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties with content type ELEMENT_ONLY
class MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1584, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}PARTY_C uses Python identifier PARTY_C
    __PARTY_C = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PARTY_C'), 'PARTY_C', '__httpwww_w3schools_com_MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_httpwww_w3schools_comPARTY_C', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1587, 4), )

    
    PARTY_C = property(__PARTY_C.value, __PARTY_C.set, None, None)

    
    # Element {http://www.w3schools.com}PARTY_L uses Python identifier PARTY_L
    __PARTY_L = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PARTY_L'), 'PARTY_L', '__httpwww_w3schools_com_MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_httpwww_w3schools_comPARTY_L', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1588, 4), )

    
    PARTY_L = property(__PARTY_L.value, __PARTY_L.set, None, None)

    
    # Element {http://www.w3schools.com}PARTY_P uses Python identifier PARTY_P
    __PARTY_P = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PARTY_P'), 'PARTY_P', '__httpwww_w3schools_com_MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_httpwww_w3schools_comPARTY_P', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1589, 4), )

    
    PARTY_P = property(__PARTY_P.value, __PARTY_P.set, None, None)

    
    # Element {http://www.w3schools.com}PARTY_Q uses Python identifier PARTY_Q
    __PARTY_Q = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PARTY_Q'), 'PARTY_Q', '__httpwww_w3schools_com_MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_httpwww_w3schools_comPARTY_Q', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1590, 4), )

    
    PARTY_Q = property(__PARTY_Q.value, __PARTY_Q.set, None, None)

    
    # Element {http://www.w3schools.com}PARTY_R uses Python identifier PARTY_R
    __PARTY_R = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PARTY_R'), 'PARTY_R', '__httpwww_w3schools_com_MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_httpwww_w3schools_comPARTY_R', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1591, 4), )

    
    PARTY_R = property(__PARTY_R.value, __PARTY_R.set, None, None)

    
    # Element {http://www.w3schools.com}PARTY_S uses Python identifier PARTY_S
    __PARTY_S = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PARTY_S'), 'PARTY_S', '__httpwww_w3schools_com_MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_httpwww_w3schools_comPARTY_S', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1592, 4), )

    
    PARTY_S = property(__PARTY_S.value, __PARTY_S.set, None, None)

    
    # Element {http://www.w3schools.com}SafekeepingAccount_A uses Python identifier SafekeepingAccount_A
    __SafekeepingAccount_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SafekeepingAccount_A'), 'SafekeepingAccount_A', '__httpwww_w3schools_com_MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_httpwww_w3schools_comSafekeepingAccount_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1595, 4), )

    
    SafekeepingAccount_A = property(__SafekeepingAccount_A.value, __SafekeepingAccount_A.set, None, None)

    
    # Element {http://www.w3schools.com}SafekeepingAccount_B uses Python identifier SafekeepingAccount_B
    __SafekeepingAccount_B = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SafekeepingAccount_B'), 'SafekeepingAccount_B', '__httpwww_w3schools_com_MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_httpwww_w3schools_comSafekeepingAccount_B', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1596, 4), )

    
    SafekeepingAccount_B = property(__SafekeepingAccount_B.value, __SafekeepingAccount_B.set, None, None)

    
    # Element {http://www.w3schools.com}ProcessingDateTime_A uses Python identifier ProcessingDateTime_A
    __ProcessingDateTime_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ProcessingDateTime_A'), 'ProcessingDateTime_A', '__httpwww_w3schools_com_MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_httpwww_w3schools_comProcessingDateTime_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1599, 4), )

    
    ProcessingDateTime_A = property(__ProcessingDateTime_A.value, __ProcessingDateTime_A.set, None, None)

    
    # Element {http://www.w3schools.com}ProcessingDateTime_C uses Python identifier ProcessingDateTime_C
    __ProcessingDateTime_C = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ProcessingDateTime_C'), 'ProcessingDateTime_C', '__httpwww_w3schools_com_MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_httpwww_w3schools_comProcessingDateTime_C', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1600, 4), )

    
    ProcessingDateTime_C = property(__ProcessingDateTime_C.value, __ProcessingDateTime_C.set, None, None)

    
    # Element {http://www.w3schools.com}ProcessingReference uses Python identifier ProcessingReference
    __ProcessingReference = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ProcessingReference'), 'ProcessingReference', '__httpwww_w3schools_com_MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_httpwww_w3schools_comProcessingReference', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1602, 3), )

    
    ProcessingReference = property(__ProcessingReference.value, __ProcessingReference.set, None, None)

    
    # Element {http://www.w3schools.com}Narrative_C uses Python identifier Narrative_C
    __Narrative_C = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Narrative_C'), 'Narrative_C', '__httpwww_w3schools_com_MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_httpwww_w3schools_comNarrative_C', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1604, 4), )

    
    Narrative_C = property(__Narrative_C.value, __Narrative_C.set, None, None)

    
    # Element {http://www.w3schools.com}Narrative_D uses Python identifier Narrative_D
    __Narrative_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Narrative_D'), 'Narrative_D', '__httpwww_w3schools_com_MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_httpwww_w3schools_comNarrative_D', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1605, 4), )

    
    Narrative_D = property(__Narrative_D.value, __Narrative_D.set, None, None)

    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='16R')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1608, 2)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1608, 2)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1609, 2)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1609, 2)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    
    # Attribute formatTag uses Python identifier formatTag
    __formatTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'formatTag'), 'formatTag', '__httpwww_w3schools_com_MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_formatTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='SETPRTY')
    __formatTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1610, 2)
    __formatTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1610, 2)
    
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
        __Narrative_D.name() : __Narrative_D
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory,
        __formatTag.name() : __formatTag
    })
_module_typeBindings.MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties = MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties', MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties)


# Complex type {http://www.w3schools.com}MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties with content type ELEMENT_ONLY
class MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1612, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}PARTY_L uses Python identifier PARTY_L
    __PARTY_L = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PARTY_L'), 'PARTY_L', '__httpwww_w3schools_com_MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_httpwww_w3schools_comPARTY_L', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1615, 4), )

    
    PARTY_L = property(__PARTY_L.value, __PARTY_L.set, None, None)

    
    # Element {http://www.w3schools.com}PARTY_P uses Python identifier PARTY_P
    __PARTY_P = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PARTY_P'), 'PARTY_P', '__httpwww_w3schools_com_MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_httpwww_w3schools_comPARTY_P', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1616, 4), )

    
    PARTY_P = property(__PARTY_P.value, __PARTY_P.set, None, None)

    
    # Element {http://www.w3schools.com}PARTY_Q uses Python identifier PARTY_Q
    __PARTY_Q = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PARTY_Q'), 'PARTY_Q', '__httpwww_w3schools_com_MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_httpwww_w3schools_comPARTY_Q', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1617, 4), )

    
    PARTY_Q = property(__PARTY_Q.value, __PARTY_Q.set, None, None)

    
    # Element {http://www.w3schools.com}PARTY_R uses Python identifier PARTY_R
    __PARTY_R = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PARTY_R'), 'PARTY_R', '__httpwww_w3schools_com_MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_httpwww_w3schools_comPARTY_R', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1618, 4), )

    
    PARTY_R = property(__PARTY_R.value, __PARTY_R.set, None, None)

    
    # Element {http://www.w3schools.com}PARTY_S uses Python identifier PARTY_S
    __PARTY_S = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PARTY_S'), 'PARTY_S', '__httpwww_w3schools_com_MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_httpwww_w3schools_comPARTY_S', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1619, 4), )

    
    PARTY_S = property(__PARTY_S.value, __PARTY_S.set, None, None)

    
    # Element {http://www.w3schools.com}Account_A uses Python identifier Account_A
    __Account_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Account_A'), 'Account_A', '__httpwww_w3schools_com_MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_httpwww_w3schools_comAccount_A', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1622, 4), )

    
    Account_A = property(__Account_A.value, __Account_A.set, None, None)

    
    # Element {http://www.w3schools.com}Account_E uses Python identifier Account_E
    __Account_E = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Account_E'), 'Account_E', '__httpwww_w3schools_com_MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_httpwww_w3schools_comAccount_E', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1623, 4), )

    
    Account_E = property(__Account_E.value, __Account_E.set, None, None)

    
    # Element {http://www.w3schools.com}ProcessingDateTime_A uses Python identifier ProcessingDateTime_A
    __ProcessingDateTime_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ProcessingDateTime_A'), 'ProcessingDateTime_A', '__httpwww_w3schools_com_MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_httpwww_w3schools_comProcessingDateTime_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1626, 4), )

    
    ProcessingDateTime_A = property(__ProcessingDateTime_A.value, __ProcessingDateTime_A.set, None, None)

    
    # Element {http://www.w3schools.com}ProcessingDateTime_C uses Python identifier ProcessingDateTime_C
    __ProcessingDateTime_C = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ProcessingDateTime_C'), 'ProcessingDateTime_C', '__httpwww_w3schools_com_MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_httpwww_w3schools_comProcessingDateTime_C', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1627, 4), )

    
    ProcessingDateTime_C = property(__ProcessingDateTime_C.value, __ProcessingDateTime_C.set, None, None)

    
    # Element {http://www.w3schools.com}ProcessingReference uses Python identifier ProcessingReference
    __ProcessingReference = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ProcessingReference'), 'ProcessingReference', '__httpwww_w3schools_com_MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_httpwww_w3schools_comProcessingReference', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1629, 3), )

    
    ProcessingReference = property(__ProcessingReference.value, __ProcessingReference.set, None, None)

    
    # Element {http://www.w3schools.com}PartyNarrative uses Python identifier PartyNarrative
    __PartyNarrative = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PartyNarrative'), 'PartyNarrative', '__httpwww_w3schools_com_MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_httpwww_w3schools_comPartyNarrative', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1630, 3), )

    
    PartyNarrative = property(__PartyNarrative.value, __PartyNarrative.set, None, None)

    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='16R')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1632, 2)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1632, 2)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1633, 2)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1633, 2)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    
    # Attribute formatTag uses Python identifier formatTag
    __formatTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'formatTag'), 'formatTag', '__httpwww_w3schools_com_MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_formatTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='CSHPRTY')
    __formatTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1634, 2)
    __formatTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1634, 2)
    
    formatTag = property(__formatTag.value, __formatTag.set, None, None)

    _ElementMap.update({
        __PARTY_L.name() : __PARTY_L,
        __PARTY_P.name() : __PARTY_P,
        __PARTY_Q.name() : __PARTY_Q,
        __PARTY_R.name() : __PARTY_R,
        __PARTY_S.name() : __PARTY_S,
        __Account_A.name() : __Account_A,
        __Account_E.name() : __Account_E,
        __ProcessingDateTime_A.name() : __ProcessingDateTime_A,
        __ProcessingDateTime_C.name() : __ProcessingDateTime_C,
        __ProcessingReference.name() : __ProcessingReference,
        __PartyNarrative.name() : __PartyNarrative
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory,
        __formatTag.name() : __formatTag
    })
_module_typeBindings.MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties = MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties', MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties)


# Complex type {http://www.w3schools.com}MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts with content type ELEMENT_ONLY
class MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1636, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}Flag uses Python identifier Flag
    __Flag = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Flag'), 'Flag', '__httpwww_w3schools_com_MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_httpwww_w3schools_comFlag', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1638, 3), )

    
    Flag = property(__Flag.value, __Flag.set, None, None)

    
    # Element {http://www.w3schools.com}Amount uses Python identifier Amount
    __Amount = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Amount'), 'Amount', '__httpwww_w3schools_com_MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_httpwww_w3schools_comAmount', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1639, 3), )

    
    Amount = property(__Amount.value, __Amount.set, None, None)

    
    # Element {http://www.w3schools.com}ValueDateTime_A uses Python identifier ValueDateTime_A
    __ValueDateTime_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ValueDateTime_A'), 'ValueDateTime_A', '__httpwww_w3schools_com_MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_httpwww_w3schools_comValueDateTime_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1641, 4), )

    
    ValueDateTime_A = property(__ValueDateTime_A.value, __ValueDateTime_A.set, None, None)

    
    # Element {http://www.w3schools.com}ValueDateTime_C uses Python identifier ValueDateTime_C
    __ValueDateTime_C = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ValueDateTime_C'), 'ValueDateTime_C', '__httpwww_w3schools_com_MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_httpwww_w3schools_comValueDateTime_C', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1642, 4), )

    
    ValueDateTime_C = property(__ValueDateTime_C.value, __ValueDateTime_C.set, None, None)

    
    # Element {http://www.w3schools.com}ExchangeRate uses Python identifier ExchangeRate
    __ExchangeRate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ExchangeRate'), 'ExchangeRate', '__httpwww_w3schools_com_MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_httpwww_w3schools_comExchangeRate', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1644, 3), )

    
    ExchangeRate = property(__ExchangeRate.value, __ExchangeRate.set, None, None)

    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='16R')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1646, 2)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1646, 2)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1647, 2)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1647, 2)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    
    # Attribute formatTag uses Python identifier formatTag
    __formatTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'formatTag'), 'formatTag', '__httpwww_w3schools_com_MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_formatTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='AMT')
    __formatTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1648, 2)
    __formatTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1648, 2)
    
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
_module_typeBindings.MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts = MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts', MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts)


# Complex type {http://www.w3schools.com}MT518_SequenceD_OtherParties with content type ELEMENT_ONLY
class MT518_SequenceD_OtherParties (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceD_OtherParties with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceD_OtherParties')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1650, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}PARTY_L uses Python identifier PARTY_L
    __PARTY_L = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PARTY_L'), 'PARTY_L', '__httpwww_w3schools_com_MT518_SequenceD_OtherParties_httpwww_w3schools_comPARTY_L', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1653, 4), )

    
    PARTY_L = property(__PARTY_L.value, __PARTY_L.set, None, None)

    
    # Element {http://www.w3schools.com}PARTY_P uses Python identifier PARTY_P
    __PARTY_P = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PARTY_P'), 'PARTY_P', '__httpwww_w3schools_com_MT518_SequenceD_OtherParties_httpwww_w3schools_comPARTY_P', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1654, 4), )

    
    PARTY_P = property(__PARTY_P.value, __PARTY_P.set, None, None)

    
    # Element {http://www.w3schools.com}PARTY_Q uses Python identifier PARTY_Q
    __PARTY_Q = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PARTY_Q'), 'PARTY_Q', '__httpwww_w3schools_com_MT518_SequenceD_OtherParties_httpwww_w3schools_comPARTY_Q', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1655, 4), )

    
    PARTY_Q = property(__PARTY_Q.value, __PARTY_Q.set, None, None)

    
    # Element {http://www.w3schools.com}PARTY_R uses Python identifier PARTY_R
    __PARTY_R = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PARTY_R'), 'PARTY_R', '__httpwww_w3schools_com_MT518_SequenceD_OtherParties_httpwww_w3schools_comPARTY_R', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1656, 4), )

    
    PARTY_R = property(__PARTY_R.value, __PARTY_R.set, None, None)

    
    # Element {http://www.w3schools.com}PARTY_S uses Python identifier PARTY_S
    __PARTY_S = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PARTY_S'), 'PARTY_S', '__httpwww_w3schools_com_MT518_SequenceD_OtherParties_httpwww_w3schools_comPARTY_S', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1657, 4), )

    
    PARTY_S = property(__PARTY_S.value, __PARTY_S.set, None, None)

    
    # Element {http://www.w3schools.com}Account_A uses Python identifier Account_A
    __Account_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Account_A'), 'Account_A', '__httpwww_w3schools_com_MT518_SequenceD_OtherParties_httpwww_w3schools_comAccount_A', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1660, 4), )

    
    Account_A = property(__Account_A.value, __Account_A.set, None, None)

    
    # Element {http://www.w3schools.com}Account_B uses Python identifier Account_B
    __Account_B = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Account_B'), 'Account_B', '__httpwww_w3schools_com_MT518_SequenceD_OtherParties_httpwww_w3schools_comAccount_B', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1661, 4), )

    
    Account_B = property(__Account_B.value, __Account_B.set, None, None)

    
    # Element {http://www.w3schools.com}Account_E uses Python identifier Account_E
    __Account_E = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Account_E'), 'Account_E', '__httpwww_w3schools_com_MT518_SequenceD_OtherParties_httpwww_w3schools_comAccount_E', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1662, 4), )

    
    Account_E = property(__Account_E.value, __Account_E.set, None, None)

    
    # Element {http://www.w3schools.com}PartyNarrative uses Python identifier PartyNarrative
    __PartyNarrative = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PartyNarrative'), 'PartyNarrative', '__httpwww_w3schools_com_MT518_SequenceD_OtherParties_httpwww_w3schools_comPartyNarrative', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1664, 3), )

    
    PartyNarrative = property(__PartyNarrative.value, __PartyNarrative.set, None, None)

    
    # Element {http://www.w3schools.com}ProcessingReference uses Python identifier ProcessingReference
    __ProcessingReference = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ProcessingReference'), 'ProcessingReference', '__httpwww_w3schools_com_MT518_SequenceD_OtherParties_httpwww_w3schools_comProcessingReference', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1665, 3), )

    
    ProcessingReference = property(__ProcessingReference.value, __ProcessingReference.set, None, None)

    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceD_OtherParties_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='16R')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1667, 2)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1667, 2)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceD_OtherParties_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1668, 2)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1668, 2)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    
    # Attribute formatTag uses Python identifier formatTag
    __formatTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'formatTag'), 'formatTag', '__httpwww_w3schools_com_MT518_SequenceD_OtherParties_formatTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='OTHRPRTY')
    __formatTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1669, 2)
    __formatTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1669, 2)
    
    formatTag = property(__formatTag.value, __formatTag.set, None, None)

    _ElementMap.update({
        __PARTY_L.name() : __PARTY_L,
        __PARTY_P.name() : __PARTY_P,
        __PARTY_Q.name() : __PARTY_Q,
        __PARTY_R.name() : __PARTY_R,
        __PARTY_S.name() : __PARTY_S,
        __Account_A.name() : __Account_A,
        __Account_B.name() : __Account_B,
        __Account_E.name() : __Account_E,
        __PartyNarrative.name() : __PartyNarrative,
        __ProcessingReference.name() : __ProcessingReference
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory,
        __formatTag.name() : __formatTag
    })
_module_typeBindings.MT518_SequenceD_OtherParties = MT518_SequenceD_OtherParties
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceD_OtherParties', MT518_SequenceD_OtherParties)


# Complex type {http://www.w3schools.com}MT518_SequenceE_TwoLegTransactionDetails with content type ELEMENT_ONLY
class MT518_SequenceE_TwoLegTransactionDetails (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceE_TwoLegTransactionDetails with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceE_TwoLegTransactionDetails')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1671, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}DateTime_A uses Python identifier DateTime_A
    __DateTime_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'DateTime_A'), 'DateTime_A', '__httpwww_w3schools_com_MT518_SequenceE_TwoLegTransactionDetails_httpwww_w3schools_comDateTime_A', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1674, 4), )

    
    DateTime_A = property(__DateTime_A.value, __DateTime_A.set, None, None)

    
    # Element {http://www.w3schools.com}DateTime_B uses Python identifier DateTime_B
    __DateTime_B = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'DateTime_B'), 'DateTime_B', '__httpwww_w3schools_com_MT518_SequenceE_TwoLegTransactionDetails_httpwww_w3schools_comDateTime_B', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1675, 4), )

    
    DateTime_B = property(__DateTime_B.value, __DateTime_B.set, None, None)

    
    # Element {http://www.w3schools.com}DateTime_C uses Python identifier DateTime_C
    __DateTime_C = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'DateTime_C'), 'DateTime_C', '__httpwww_w3schools_com_MT518_SequenceE_TwoLegTransactionDetails_httpwww_w3schools_comDateTime_C', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1676, 4), )

    
    DateTime_C = property(__DateTime_C.value, __DateTime_C.set, None, None)

    
    # Element {http://www.w3schools.com}Indicator uses Python identifier Indicator
    __Indicator = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Indicator'), 'Indicator', '__httpwww_w3schools_com_MT518_SequenceE_TwoLegTransactionDetails_httpwww_w3schools_comIndicator', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1678, 3), )

    
    Indicator = property(__Indicator.value, __Indicator.set, None, None)

    
    # Element {http://www.w3schools.com}Reference uses Python identifier Reference
    __Reference = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Reference'), 'Reference', '__httpwww_w3schools_com_MT518_SequenceE_TwoLegTransactionDetails_httpwww_w3schools_comReference', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1679, 3), )

    
    Reference = property(__Reference.value, __Reference.set, None, None)

    
    # Element {http://www.w3schools.com}Rate_A uses Python identifier Rate_A
    __Rate_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Rate_A'), 'Rate_A', '__httpwww_w3schools_com_MT518_SequenceE_TwoLegTransactionDetails_httpwww_w3schools_comRate_A', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1681, 4), )

    
    Rate_A = property(__Rate_A.value, __Rate_A.set, None, None)

    
    # Element {http://www.w3schools.com}Rate_C uses Python identifier Rate_C
    __Rate_C = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Rate_C'), 'Rate_C', '__httpwww_w3schools_com_MT518_SequenceE_TwoLegTransactionDetails_httpwww_w3schools_comRate_C', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1682, 4), )

    
    Rate_C = property(__Rate_C.value, __Rate_C.set, None, None)

    
    # Element {http://www.w3schools.com}NumberCount uses Python identifier NumberCount
    __NumberCount = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'NumberCount'), 'NumberCount', '__httpwww_w3schools_com_MT518_SequenceE_TwoLegTransactionDetails_httpwww_w3schools_comNumberCount', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1684, 3), )

    
    NumberCount = property(__NumberCount.value, __NumberCount.set, None, None)

    
    # Element {http://www.w3schools.com}Amount uses Python identifier Amount
    __Amount = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Amount'), 'Amount', '__httpwww_w3schools_com_MT518_SequenceE_TwoLegTransactionDetails_httpwww_w3schools_comAmount', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1685, 3), )

    
    Amount = property(__Amount.value, __Amount.set, None, None)

    
    # Element {http://www.w3schools.com}SecondLegNarrative uses Python identifier SecondLegNarrative
    __SecondLegNarrative = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SecondLegNarrative'), 'SecondLegNarrative', '__httpwww_w3schools_com_MT518_SequenceE_TwoLegTransactionDetails_httpwww_w3schools_comSecondLegNarrative', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1686, 3), )

    
    SecondLegNarrative = property(__SecondLegNarrative.value, __SecondLegNarrative.set, None, None)

    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceE_TwoLegTransactionDetails_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='16R')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1688, 2)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1688, 2)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceE_TwoLegTransactionDetails_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1689, 2)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1689, 2)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    
    # Attribute formatTag uses Python identifier formatTag
    __formatTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'formatTag'), 'formatTag', '__httpwww_w3schools_com_MT518_SequenceE_TwoLegTransactionDetails_formatTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='REPO')
    __formatTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1690, 2)
    __formatTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1690, 2)
    
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
_module_typeBindings.MT518_SequenceE_TwoLegTransactionDetails = MT518_SequenceE_TwoLegTransactionDetails
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceE_TwoLegTransactionDetails', MT518_SequenceE_TwoLegTransactionDetails)


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1693, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}SequenceA_GeneralInformation uses Python identifier SequenceA_GeneralInformation
    __SequenceA_GeneralInformation = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SequenceA_GeneralInformation'), 'SequenceA_GeneralInformation', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comSequenceA_GeneralInformation', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1695, 4), )

    
    SequenceA_GeneralInformation = property(__SequenceA_GeneralInformation.value, __SequenceA_GeneralInformation.set, None, None)

    
    # Element {http://www.w3schools.com}SequenceB_ConfirmationDetails uses Python identifier SequenceB_ConfirmationDetails
    __SequenceB_ConfirmationDetails = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SequenceB_ConfirmationDetails'), 'SequenceB_ConfirmationDetails', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comSequenceB_ConfirmationDetails', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1696, 4), )

    
    SequenceB_ConfirmationDetails = property(__SequenceB_ConfirmationDetails.value, __SequenceB_ConfirmationDetails.set, None, None)

    
    # Element {http://www.w3schools.com}SequenceC_SettlementDetails uses Python identifier SequenceC_SettlementDetails
    __SequenceC_SettlementDetails = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SequenceC_SettlementDetails'), 'SequenceC_SettlementDetails', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comSequenceC_SettlementDetails', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1697, 4), )

    
    SequenceC_SettlementDetails = property(__SequenceC_SettlementDetails.value, __SequenceC_SettlementDetails.set, None, None)

    
    # Element {http://www.w3schools.com}SequenceD_OtherParties uses Python identifier SequenceD_OtherParties
    __SequenceD_OtherParties = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SequenceD_OtherParties'), 'SequenceD_OtherParties', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comSequenceD_OtherParties', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1698, 4), )

    
    SequenceD_OtherParties = property(__SequenceD_OtherParties.value, __SequenceD_OtherParties.set, None, None)

    
    # Element {http://www.w3schools.com}SequenceE_TwoLegTransactionDetails uses Python identifier SequenceE_TwoLegTransactionDetails
    __SequenceE_TwoLegTransactionDetails = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SequenceE_TwoLegTransactionDetails'), 'SequenceE_TwoLegTransactionDetails', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comSequenceE_TwoLegTransactionDetails', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1699, 4), )

    
    SequenceE_TwoLegTransactionDetails = property(__SequenceE_TwoLegTransactionDetails.value, __SequenceE_TwoLegTransactionDetails.set, None, None)

    _ElementMap.update({
        __SequenceA_GeneralInformation.name() : __SequenceA_GeneralInformation,
        __SequenceB_ConfirmationDetails.name() : __SequenceB_ConfirmationDetails,
        __SequenceC_SettlementDetails.name() : __SequenceC_SettlementDetails,
        __SequenceD_OtherParties.name() : __SequenceD_OtherParties,
        __SequenceE_TwoLegTransactionDetails.name() : __SequenceE_TwoLegTransactionDetails
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON = CTD_ANON


# Complex type {http://www.w3schools.com}MT518_SequenceA_GeneralInformation_20C_Type with content type SIMPLE
class MT518_SequenceA_GeneralInformation_20C_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceA_GeneralInformation_20C_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceA_GeneralInformation_20C_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceA_GeneralInformation_20C_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 8, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceA_GeneralInformation_20C_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceA_GeneralInformation_20C_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='20C')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 11, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 11, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceA_GeneralInformation_20C_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 12, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 12, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceA_GeneralInformation_20C_Type = MT518_SequenceA_GeneralInformation_20C_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceA_GeneralInformation_20C_Type', MT518_SequenceA_GeneralInformation_20C_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceA_GeneralInformation_23G_Type with content type SIMPLE
class MT518_SequenceA_GeneralInformation_23G_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceA_GeneralInformation_23G_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceA_GeneralInformation_23G_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceA_GeneralInformation_23G_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 21, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceA_GeneralInformation_23G_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceA_GeneralInformation_23G_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='23G')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 24, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 24, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceA_GeneralInformation_23G_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 25, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 25, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceA_GeneralInformation_23G_Type = MT518_SequenceA_GeneralInformation_23G_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceA_GeneralInformation_23G_Type', MT518_SequenceA_GeneralInformation_23G_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceA_GeneralInformation_98A_Type with content type SIMPLE
class MT518_SequenceA_GeneralInformation_98A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceA_GeneralInformation_98A_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceA_GeneralInformation_98A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceA_GeneralInformation_98A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 34, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceA_GeneralInformation_98A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceA_GeneralInformation_98A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='98A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 37, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 37, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceA_GeneralInformation_98A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 38, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 38, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceA_GeneralInformation_98A_Type = MT518_SequenceA_GeneralInformation_98A_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceA_GeneralInformation_98A_Type', MT518_SequenceA_GeneralInformation_98A_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceA_GeneralInformation_98C_Type with content type SIMPLE
class MT518_SequenceA_GeneralInformation_98C_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceA_GeneralInformation_98C_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceA_GeneralInformation_98C_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceA_GeneralInformation_98C_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 47, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceA_GeneralInformation_98C_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceA_GeneralInformation_98C_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='98C')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 50, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 50, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceA_GeneralInformation_98C_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 51, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 51, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceA_GeneralInformation_98C_Type = MT518_SequenceA_GeneralInformation_98C_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceA_GeneralInformation_98C_Type', MT518_SequenceA_GeneralInformation_98C_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceA_GeneralInformation_98E_Type with content type SIMPLE
class MT518_SequenceA_GeneralInformation_98E_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceA_GeneralInformation_98E_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceA_GeneralInformation_98E_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceA_GeneralInformation_98E_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 60, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceA_GeneralInformation_98E_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceA_GeneralInformation_98E_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='98E')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 63, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 63, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceA_GeneralInformation_98E_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 64, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 64, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceA_GeneralInformation_98E_Type = MT518_SequenceA_GeneralInformation_98E_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceA_GeneralInformation_98E_Type', MT518_SequenceA_GeneralInformation_98E_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceA_GeneralInformation_22F_Type with content type SIMPLE
class MT518_SequenceA_GeneralInformation_22F_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceA_GeneralInformation_22F_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceA_GeneralInformation_22F_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceA_GeneralInformation_22F_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 73, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceA_GeneralInformation_22F_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceA_GeneralInformation_22F_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='22F')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 76, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 76, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceA_GeneralInformation_22F_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 77, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 77, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceA_GeneralInformation_22F_Type = MT518_SequenceA_GeneralInformation_22F_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceA_GeneralInformation_22F_Type', MT518_SequenceA_GeneralInformation_22F_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13A_Type with content type SIMPLE
class MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13A_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 86, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='13A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 89, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 89, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 90, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 90, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13A_Type = MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13A_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13A_Type', MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13A_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13B_Type with content type SIMPLE
class MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13B_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 99, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='13B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 102, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 102, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 103, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 103, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13B_Type = MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13B_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13B_Type', MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13B_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20C_Type with content type SIMPLE
class MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20C_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20C_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20C_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20C_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 112, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20C_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20C_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='20C')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 115, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 115, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20C_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 116, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 116, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20C_Type = MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20C_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20C_Type', MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20C_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20U_Type with content type SIMPLE
class MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20U_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20U_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20U_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20U_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 125, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20U_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20U_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='20U')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 128, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 128, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20U_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 129, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 129, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20U_Type = MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20U_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20U_Type', MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20U_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_98A_Type with content type SIMPLE
class MT518_SequenceB_ConfirmationDetails_98A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_98A_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceB_ConfirmationDetails_98A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceB_ConfirmationDetails_98A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 138, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceB_ConfirmationDetails_98A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_98A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='98A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 141, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 141, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_98A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 142, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 142, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceB_ConfirmationDetails_98A_Type = MT518_SequenceB_ConfirmationDetails_98A_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceB_ConfirmationDetails_98A_Type', MT518_SequenceB_ConfirmationDetails_98A_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_98B_Type with content type SIMPLE
class MT518_SequenceB_ConfirmationDetails_98B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_98B_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceB_ConfirmationDetails_98B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceB_ConfirmationDetails_98B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 151, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceB_ConfirmationDetails_98B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_98B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='98B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 154, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 154, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_98B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 155, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 155, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceB_ConfirmationDetails_98B_Type = MT518_SequenceB_ConfirmationDetails_98B_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceB_ConfirmationDetails_98B_Type', MT518_SequenceB_ConfirmationDetails_98B_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_98C_Type with content type SIMPLE
class MT518_SequenceB_ConfirmationDetails_98C_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_98C_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceB_ConfirmationDetails_98C_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceB_ConfirmationDetails_98C_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 164, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceB_ConfirmationDetails_98C_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_98C_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='98C')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 167, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 167, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_98C_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 168, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 168, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceB_ConfirmationDetails_98C_Type = MT518_SequenceB_ConfirmationDetails_98C_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceB_ConfirmationDetails_98C_Type', MT518_SequenceB_ConfirmationDetails_98C_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_98E_Type with content type SIMPLE
class MT518_SequenceB_ConfirmationDetails_98E_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_98E_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceB_ConfirmationDetails_98E_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceB_ConfirmationDetails_98E_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 177, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceB_ConfirmationDetails_98E_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_98E_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='98E')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 180, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 180, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_98E_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 181, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 181, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceB_ConfirmationDetails_98E_Type = MT518_SequenceB_ConfirmationDetails_98E_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceB_ConfirmationDetails_98E_Type', MT518_SequenceB_ConfirmationDetails_98E_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_90A_Type with content type SIMPLE
class MT518_SequenceB_ConfirmationDetails_90A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_90A_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceB_ConfirmationDetails_90A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceB_ConfirmationDetails_90A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 190, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceB_ConfirmationDetails_90A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_90A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='90A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 193, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 193, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_90A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 194, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 194, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceB_ConfirmationDetails_90A_Type = MT518_SequenceB_ConfirmationDetails_90A_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceB_ConfirmationDetails_90A_Type', MT518_SequenceB_ConfirmationDetails_90A_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_90B_Type with content type SIMPLE
class MT518_SequenceB_ConfirmationDetails_90B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_90B_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceB_ConfirmationDetails_90B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceB_ConfirmationDetails_90B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 203, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceB_ConfirmationDetails_90B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_90B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='90B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 206, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 206, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_90B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 207, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 207, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceB_ConfirmationDetails_90B_Type = MT518_SequenceB_ConfirmationDetails_90B_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceB_ConfirmationDetails_90B_Type', MT518_SequenceB_ConfirmationDetails_90B_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_92A_Type with content type SIMPLE
class MT518_SequenceB_ConfirmationDetails_92A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_92A_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceB_ConfirmationDetails_92A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceB_ConfirmationDetails_92A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 216, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceB_ConfirmationDetails_92A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_92A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='92A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 219, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 219, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_92A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 220, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 220, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceB_ConfirmationDetails_92A_Type = MT518_SequenceB_ConfirmationDetails_92A_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceB_ConfirmationDetails_92A_Type', MT518_SequenceB_ConfirmationDetails_92A_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_99A_Type with content type SIMPLE
class MT518_SequenceB_ConfirmationDetails_99A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_99A_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceB_ConfirmationDetails_99A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceB_ConfirmationDetails_99A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 229, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceB_ConfirmationDetails_99A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_99A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='99A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 232, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 232, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_99A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 233, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 233, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceB_ConfirmationDetails_99A_Type = MT518_SequenceB_ConfirmationDetails_99A_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceB_ConfirmationDetails_99A_Type', MT518_SequenceB_ConfirmationDetails_99A_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_94B_Type with content type SIMPLE
class MT518_SequenceB_ConfirmationDetails_94B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_94B_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceB_ConfirmationDetails_94B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceB_ConfirmationDetails_94B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 242, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceB_ConfirmationDetails_94B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_94B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='94B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 245, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 245, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_94B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 246, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 246, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceB_ConfirmationDetails_94B_Type = MT518_SequenceB_ConfirmationDetails_94B_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceB_ConfirmationDetails_94B_Type', MT518_SequenceB_ConfirmationDetails_94B_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_94C_Type with content type SIMPLE
class MT518_SequenceB_ConfirmationDetails_94C_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_94C_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceB_ConfirmationDetails_94C_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceB_ConfirmationDetails_94C_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 255, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceB_ConfirmationDetails_94C_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_94C_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='94C')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 258, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 258, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_94C_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 259, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 259, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceB_ConfirmationDetails_94C_Type = MT518_SequenceB_ConfirmationDetails_94C_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceB_ConfirmationDetails_94C_Type', MT518_SequenceB_ConfirmationDetails_94C_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_94F_Type with content type SIMPLE
class MT518_SequenceB_ConfirmationDetails_94F_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_94F_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceB_ConfirmationDetails_94F_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceB_ConfirmationDetails_94F_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 268, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceB_ConfirmationDetails_94F_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_94F_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='94F')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 271, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 271, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_94F_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 272, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 272, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceB_ConfirmationDetails_94F_Type = MT518_SequenceB_ConfirmationDetails_94F_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceB_ConfirmationDetails_94F_Type', MT518_SequenceB_ConfirmationDetails_94F_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_94L_Type with content type SIMPLE
class MT518_SequenceB_ConfirmationDetails_94L_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_94L_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceB_ConfirmationDetails_94L_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceB_ConfirmationDetails_94L_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 281, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceB_ConfirmationDetails_94L_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_94L_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='94L')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 284, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 284, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_94L_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 285, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 285, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceB_ConfirmationDetails_94L_Type = MT518_SequenceB_ConfirmationDetails_94L_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceB_ConfirmationDetails_94L_Type', MT518_SequenceB_ConfirmationDetails_94L_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_19A_Type with content type SIMPLE
class MT518_SequenceB_ConfirmationDetails_19A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_19A_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceB_ConfirmationDetails_19A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceB_ConfirmationDetails_19A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 294, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceB_ConfirmationDetails_19A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_19A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='19A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 297, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 297, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_19A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 298, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 298, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceB_ConfirmationDetails_19A_Type = MT518_SequenceB_ConfirmationDetails_19A_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceB_ConfirmationDetails_19A_Type', MT518_SequenceB_ConfirmationDetails_19A_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_22F_Type with content type SIMPLE
class MT518_SequenceB_ConfirmationDetails_22F_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_22F_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceB_ConfirmationDetails_22F_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceB_ConfirmationDetails_22F_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 307, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceB_ConfirmationDetails_22F_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_22F_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='22F')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 310, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 310, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_22F_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 311, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 311, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceB_ConfirmationDetails_22F_Type = MT518_SequenceB_ConfirmationDetails_22F_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceB_ConfirmationDetails_22F_Type', MT518_SequenceB_ConfirmationDetails_22F_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_22H_Type with content type SIMPLE
class MT518_SequenceB_ConfirmationDetails_22H_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_22H_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceB_ConfirmationDetails_22H_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceB_ConfirmationDetails_22H_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 320, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceB_ConfirmationDetails_22H_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_22H_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='22H')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 323, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 323, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_22H_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 324, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 324, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceB_ConfirmationDetails_22H_Type = MT518_SequenceB_ConfirmationDetails_22H_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceB_ConfirmationDetails_22H_Type', MT518_SequenceB_ConfirmationDetails_22H_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_11A_Type with content type SIMPLE
class MT518_SequenceB_ConfirmationDetails_11A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_11A_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceB_ConfirmationDetails_11A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceB_ConfirmationDetails_11A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 333, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceB_ConfirmationDetails_11A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_11A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='11A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 336, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 336, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_11A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 337, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 337, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceB_ConfirmationDetails_11A_Type = MT518_SequenceB_ConfirmationDetails_11A_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceB_ConfirmationDetails_11A_Type', MT518_SequenceB_ConfirmationDetails_11A_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95L_Type with content type SIMPLE
class MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95L_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95L_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95L_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95L_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 346, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95L_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95L_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='95L')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 349, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 349, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95L_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 350, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 350, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95L_Type = MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95L_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95L_Type', MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95L_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95P_Type with content type SIMPLE
class MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95P_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95P_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95P_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95P_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 359, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95P_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95P_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='95P')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 362, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 362, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95P_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 363, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 363, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95P_Type = MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95P_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95P_Type', MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95P_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95Q_Type with content type SIMPLE
class MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95Q_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95Q_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95Q_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95Q_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 372, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95Q_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95Q_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='95Q')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 375, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 375, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95Q_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 376, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 376, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95Q_Type = MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95Q_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95Q_Type', MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95Q_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95R_Type with content type SIMPLE
class MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95R_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95R_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95R_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95R_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 385, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95R_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95R_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='95R')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 388, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 388, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95R_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 389, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 389, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95R_Type = MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95R_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95R_Type', MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95R_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95S_Type with content type SIMPLE
class MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95S_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95S_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95S_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95S_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 398, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95S_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95S_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='95S')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 401, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 401, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95S_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 402, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 402, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95S_Type = MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95S_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95S_Type', MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95S_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_97A_Type with content type SIMPLE
class MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_97A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_97A_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_97A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_97A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 411, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_97A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_97A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='97A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 414, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 414, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_97A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 415, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 415, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_97A_Type = MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_97A_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_97A_Type', MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_97A_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_97B_Type with content type SIMPLE
class MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_97B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_97B_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_97B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_97B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 424, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_97B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_97B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='97B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 427, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 427, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_97B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 428, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 428, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_97B_Type = MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_97B_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_97B_Type', MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_97B_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_97E_Type with content type SIMPLE
class MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_97E_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_97E_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_97E_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_97E_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 437, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_97E_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_97E_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='97E')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 440, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 440, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_97E_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 441, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 441, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_97E_Type = MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_97E_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_97E_Type', MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_97E_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_98A_Type with content type SIMPLE
class MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_98A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_98A_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_98A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_98A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 450, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_98A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_98A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='98A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 453, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 453, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_98A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 454, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 454, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_98A_Type = MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_98A_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_98A_Type', MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_98A_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_98C_Type with content type SIMPLE
class MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_98C_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_98C_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_98C_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_98C_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 463, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_98C_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_98C_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='98C')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 466, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 466, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_98C_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 467, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 467, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_98C_Type = MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_98C_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_98C_Type', MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_98C_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_20C_Type with content type SIMPLE
class MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_20C_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_20C_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_20C_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_20C_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 476, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_20C_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_20C_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='20C')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 479, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 479, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_20C_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 480, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 480, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_20C_Type = MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_20C_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_20C_Type', MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_20C_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_70C_Type with content type SIMPLE
class MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_70C_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_70C_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_70C_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_70C_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 489, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_70C_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_70C_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='70C')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 492, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 492, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_70C_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 493, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 493, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_70C_Type = MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_70C_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_70C_Type', MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_70C_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_70E_Type with content type SIMPLE
class MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_70E_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_70E_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_70E_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_70E_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 502, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_70E_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_70E_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='70E')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 505, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 505, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_70E_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 506, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 506, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_70E_Type = MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_70E_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_70E_Type', MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_70E_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_22F_Type with content type SIMPLE
class MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_22F_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_22F_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_22F_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_22F_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 515, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_22F_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_22F_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='22F')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 518, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 518, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_22F_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 519, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 519, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_22F_Type = MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_22F_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_22F_Type', MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_22F_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_36B_Type with content type SIMPLE
class MT518_SequenceB_ConfirmationDetails_36B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_36B_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceB_ConfirmationDetails_36B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceB_ConfirmationDetails_36B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 528, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceB_ConfirmationDetails_36B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_36B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='36B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 531, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 531, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_36B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 532, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 532, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceB_ConfirmationDetails_36B_Type = MT518_SequenceB_ConfirmationDetails_36B_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceB_ConfirmationDetails_36B_Type', MT518_SequenceB_ConfirmationDetails_36B_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_35B_Type with content type SIMPLE
class MT518_SequenceB_ConfirmationDetails_35B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_35B_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceB_ConfirmationDetails_35B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceB_ConfirmationDetails_35B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 541, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceB_ConfirmationDetails_35B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_35B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='35B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 544, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 544, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_35B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 545, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 545, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceB_ConfirmationDetails_35B_Type = MT518_SequenceB_ConfirmationDetails_35B_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceB_ConfirmationDetails_35B_Type', MT518_SequenceB_ConfirmationDetails_35B_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_94B_Type with content type SIMPLE
class MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_94B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_94B_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_94B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_94B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 554, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_94B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_94B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='94B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 557, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 557, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_94B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 558, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 558, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_94B_Type = MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_94B_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_94B_Type', MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_94B_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_22F_Type with content type SIMPLE
class MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_22F_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_22F_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_22F_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_22F_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 567, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_22F_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_22F_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='22F')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 570, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 570, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_22F_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 571, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 571, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_22F_Type = MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_22F_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_22F_Type', MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_22F_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_12A_Type with content type SIMPLE
class MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_12A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_12A_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_12A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_12A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 580, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_12A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_12A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='12A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 583, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 583, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_12A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 584, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 584, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_12A_Type = MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_12A_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_12A_Type', MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_12A_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_12B_Type with content type SIMPLE
class MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_12B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_12B_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_12B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_12B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 593, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_12B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_12B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='12B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 596, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 596, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_12B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 597, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 597, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_12B_Type = MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_12B_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_12B_Type', MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_12B_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_12C_Type with content type SIMPLE
class MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_12C_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_12C_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_12C_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_12C_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 606, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_12C_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_12C_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='12C')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 609, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 609, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_12C_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 610, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 610, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_12C_Type = MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_12C_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_12C_Type', MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_12C_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_11A_Type with content type SIMPLE
class MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_11A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_11A_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_11A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_11A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 619, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_11A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_11A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='11A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 622, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 622, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_11A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 623, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 623, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_11A_Type = MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_11A_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_11A_Type', MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_11A_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_98A_Type with content type SIMPLE
class MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_98A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_98A_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_98A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_98A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 632, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_98A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_98A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='98A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 635, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 635, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_98A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 636, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 636, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_98A_Type = MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_98A_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_98A_Type', MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_98A_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_92A_Type with content type SIMPLE
class MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_92A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_92A_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_92A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_92A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 645, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_92A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_92A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='92A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 648, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 648, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_92A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 649, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 649, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_92A_Type = MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_92A_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_92A_Type', MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_92A_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_13A_Type with content type SIMPLE
class MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_13A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_13A_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_13A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_13A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 658, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_13A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_13A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='13A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 661, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 661, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_13A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 662, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 662, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_13A_Type = MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_13A_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_13A_Type', MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_13A_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_13B_Type with content type SIMPLE
class MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_13B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_13B_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_13B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_13B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 671, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_13B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_13B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='13B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 674, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 674, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_13B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 675, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 675, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_13B_Type = MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_13B_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_13B_Type', MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_13B_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_17B_Type with content type SIMPLE
class MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_17B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_17B_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_17B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_17B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 684, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_17B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_17B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='17B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 687, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 687, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_17B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 688, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 688, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_17B_Type = MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_17B_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_17B_Type', MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_17B_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_90A_Type with content type SIMPLE
class MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_90A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_90A_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_90A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_90A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 697, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_90A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_90A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='90A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 700, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 700, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_90A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 701, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 701, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_90A_Type = MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_90A_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_90A_Type', MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_90A_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_90B_Type with content type SIMPLE
class MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_90B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_90B_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_90B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_90B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 710, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_90B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_90B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='90B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 713, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 713, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_90B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 714, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 714, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_90B_Type = MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_90B_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_90B_Type', MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_90B_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_36B_Type with content type SIMPLE
class MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_36B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_36B_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_36B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_36B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 723, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_36B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_36B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='36B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 726, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 726, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_36B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 727, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 727, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_36B_Type = MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_36B_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_36B_Type', MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_36B_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_35B_Type with content type SIMPLE
class MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_35B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_35B_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_35B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_35B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 736, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_35B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_35B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='35B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 739, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 739, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_35B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 740, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 740, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_35B_Type = MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_35B_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_35B_Type', MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_35B_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_70E_Type with content type SIMPLE
class MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_70E_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_70E_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_70E_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_70E_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 749, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_70E_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_70E_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='70E')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 752, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 752, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_70E_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 753, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 753, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_70E_Type = MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_70E_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_70E_Type', MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_70E_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_13B_Type with content type SIMPLE
class MT518_SequenceB_ConfirmationDetails_13B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_13B_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceB_ConfirmationDetails_13B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceB_ConfirmationDetails_13B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 762, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceB_ConfirmationDetails_13B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_13B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='13B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 765, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 765, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_13B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 766, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 766, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceB_ConfirmationDetails_13B_Type = MT518_SequenceB_ConfirmationDetails_13B_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceB_ConfirmationDetails_13B_Type', MT518_SequenceB_ConfirmationDetails_13B_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_70E_Type with content type SIMPLE
class MT518_SequenceB_ConfirmationDetails_70E_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceB_ConfirmationDetails_70E_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceB_ConfirmationDetails_70E_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceB_ConfirmationDetails_70E_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 775, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceB_ConfirmationDetails_70E_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_70E_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='70E')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 778, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 778, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceB_ConfirmationDetails_70E_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 779, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 779, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceB_ConfirmationDetails_70E_Type = MT518_SequenceB_ConfirmationDetails_70E_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceB_ConfirmationDetails_70E_Type', MT518_SequenceB_ConfirmationDetails_70E_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceC_SettlementDetails_22F_Type with content type SIMPLE
class MT518_SequenceC_SettlementDetails_22F_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceC_SettlementDetails_22F_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceC_SettlementDetails_22F_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceC_SettlementDetails_22F_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 788, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceC_SettlementDetails_22F_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceC_SettlementDetails_22F_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='22F')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 791, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 791, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceC_SettlementDetails_22F_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 792, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 792, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceC_SettlementDetails_22F_Type = MT518_SequenceC_SettlementDetails_22F_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceC_SettlementDetails_22F_Type', MT518_SequenceC_SettlementDetails_22F_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceC_SettlementDetails_11A_Type with content type SIMPLE
class MT518_SequenceC_SettlementDetails_11A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceC_SettlementDetails_11A_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceC_SettlementDetails_11A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceC_SettlementDetails_11A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 801, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceC_SettlementDetails_11A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceC_SettlementDetails_11A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='11A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 804, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 804, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceC_SettlementDetails_11A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 805, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 805, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceC_SettlementDetails_11A_Type = MT518_SequenceC_SettlementDetails_11A_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceC_SettlementDetails_11A_Type', MT518_SequenceC_SettlementDetails_11A_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95C_Type with content type SIMPLE
class MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95C_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95C_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95C_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95C_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 814, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95C_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95C_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='95C')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 817, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 817, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95C_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 818, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 818, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95C_Type = MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95C_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95C_Type', MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95C_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95L_Type with content type SIMPLE
class MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95L_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95L_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95L_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95L_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 827, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95L_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95L_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='95L')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 830, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 830, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95L_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 831, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 831, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95L_Type = MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95L_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95L_Type', MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95L_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95P_Type with content type SIMPLE
class MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95P_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95P_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95P_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95P_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 840, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95P_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95P_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='95P')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 843, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 843, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95P_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 844, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 844, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95P_Type = MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95P_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95P_Type', MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95P_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95Q_Type with content type SIMPLE
class MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95Q_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95Q_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95Q_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95Q_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 853, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95Q_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95Q_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='95Q')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 856, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 856, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95Q_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 857, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 857, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95Q_Type = MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95Q_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95Q_Type', MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95Q_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95R_Type with content type SIMPLE
class MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95R_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95R_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95R_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95R_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 866, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95R_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95R_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='95R')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 869, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 869, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95R_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 870, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 870, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95R_Type = MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95R_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95R_Type', MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95R_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95S_Type with content type SIMPLE
class MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95S_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95S_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95S_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95S_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 879, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95S_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95S_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='95S')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 882, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 882, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95S_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 883, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 883, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95S_Type = MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95S_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95S_Type', MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95S_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_97A_Type with content type SIMPLE
class MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_97A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_97A_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_97A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_97A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 892, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_97A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_97A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='97A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 895, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 895, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_97A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 896, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 896, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_97A_Type = MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_97A_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_97A_Type', MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_97A_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_97B_Type with content type SIMPLE
class MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_97B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_97B_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_97B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_97B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 905, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_97B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_97B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='97B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 908, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 908, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_97B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 909, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 909, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_97B_Type = MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_97B_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_97B_Type', MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_97B_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_98A_Type with content type SIMPLE
class MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_98A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_98A_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_98A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_98A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 918, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_98A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_98A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='98A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 921, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 921, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_98A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 922, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 922, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_98A_Type = MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_98A_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_98A_Type', MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_98A_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_98C_Type with content type SIMPLE
class MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_98C_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_98C_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_98C_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_98C_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 931, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_98C_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_98C_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='98C')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 934, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 934, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_98C_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 935, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 935, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_98C_Type = MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_98C_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_98C_Type', MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_98C_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_20C_Type with content type SIMPLE
class MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_20C_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_20C_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_20C_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_20C_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 944, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_20C_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_20C_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='20C')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 947, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 947, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_20C_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 948, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 948, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_20C_Type = MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_20C_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_20C_Type', MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_20C_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_70C_Type with content type SIMPLE
class MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_70C_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_70C_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_70C_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_70C_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 957, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_70C_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_70C_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='70C')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 960, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 960, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_70C_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 961, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 961, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_70C_Type = MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_70C_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_70C_Type', MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_70C_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_70D_Type with content type SIMPLE
class MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_70D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_70D_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_70D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_70D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 970, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_70D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_70D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='70D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 973, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 973, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_70D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 974, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 974, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_70D_Type = MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_70D_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_70D_Type', MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_70D_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95L_Type with content type SIMPLE
class MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95L_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95L_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95L_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95L_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 983, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95L_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95L_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='95L')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 986, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 986, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95L_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 987, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 987, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95L_Type = MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95L_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95L_Type', MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95L_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95P_Type with content type SIMPLE
class MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95P_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95P_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95P_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95P_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 996, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95P_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95P_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='95P')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 999, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 999, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95P_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1000, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1000, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95P_Type = MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95P_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95P_Type', MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95P_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95Q_Type with content type SIMPLE
class MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95Q_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95Q_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95Q_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95Q_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1009, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95Q_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95Q_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='95Q')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1012, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1012, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95Q_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1013, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1013, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95Q_Type = MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95Q_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95Q_Type', MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95Q_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95R_Type with content type SIMPLE
class MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95R_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95R_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95R_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95R_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1022, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95R_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95R_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='95R')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1025, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1025, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95R_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1026, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1026, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95R_Type = MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95R_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95R_Type', MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95R_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95S_Type with content type SIMPLE
class MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95S_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95S_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95S_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95S_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1035, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95S_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95S_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='95S')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1038, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1038, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95S_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1039, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1039, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95S_Type = MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95S_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95S_Type', MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95S_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_97A_Type with content type SIMPLE
class MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_97A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_97A_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_97A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_97A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1048, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_97A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_97A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='97A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1051, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1051, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_97A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1052, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1052, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_97A_Type = MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_97A_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_97A_Type', MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_97A_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_97E_Type with content type SIMPLE
class MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_97E_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_97E_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_97E_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_97E_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1061, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_97E_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_97E_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='97E')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1064, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1064, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_97E_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1065, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1065, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_97E_Type = MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_97E_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_97E_Type', MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_97E_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_98A_Type with content type SIMPLE
class MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_98A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_98A_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_98A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_98A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1074, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_98A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_98A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='98A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1077, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1077, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_98A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1078, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1078, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_98A_Type = MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_98A_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_98A_Type', MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_98A_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_98C_Type with content type SIMPLE
class MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_98C_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_98C_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_98C_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_98C_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1087, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_98C_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_98C_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='98C')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1090, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1090, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_98C_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1091, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1091, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_98C_Type = MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_98C_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_98C_Type', MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_98C_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_20C_Type with content type SIMPLE
class MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_20C_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_20C_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_20C_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_20C_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1100, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_20C_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_20C_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='20C')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1103, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1103, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_20C_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1104, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1104, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_20C_Type = MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_20C_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_20C_Type', MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_20C_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_70C_Type with content type SIMPLE
class MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_70C_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_70C_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_70C_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_70C_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1113, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_70C_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_70C_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='70C')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1116, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1116, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_70C_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1117, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1117, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_70C_Type = MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_70C_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_70C_Type', MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_70C_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_17B_Type with content type SIMPLE
class MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_17B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_17B_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_17B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_17B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1126, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_17B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_17B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='17B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1129, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1129, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_17B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1130, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1130, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_17B_Type = MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_17B_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_17B_Type', MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_17B_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_19A_Type with content type SIMPLE
class MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_19A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_19A_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_19A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_19A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1139, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_19A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_19A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='19A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1142, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1142, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_19A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1143, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1143, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_19A_Type = MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_19A_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_19A_Type', MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_19A_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_98A_Type with content type SIMPLE
class MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_98A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_98A_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_98A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_98A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1152, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_98A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_98A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='98A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1155, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1155, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_98A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1156, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1156, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_98A_Type = MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_98A_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_98A_Type', MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_98A_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_98C_Type with content type SIMPLE
class MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_98C_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_98C_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_98C_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_98C_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1165, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_98C_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_98C_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='98C')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1168, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1168, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_98C_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1169, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1169, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_98C_Type = MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_98C_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_98C_Type', MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_98C_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_92B_Type with content type SIMPLE
class MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_92B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_92B_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_92B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_92B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1178, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_92B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_92B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='92B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1181, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1181, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_92B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1182, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1182, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_92B_Type = MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_92B_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_92B_Type', MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_92B_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceD_OtherParties_95L_Type with content type SIMPLE
class MT518_SequenceD_OtherParties_95L_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceD_OtherParties_95L_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceD_OtherParties_95L_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceD_OtherParties_95L_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1191, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceD_OtherParties_95L_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceD_OtherParties_95L_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='95L')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1194, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1194, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceD_OtherParties_95L_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1195, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1195, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceD_OtherParties_95L_Type = MT518_SequenceD_OtherParties_95L_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceD_OtherParties_95L_Type', MT518_SequenceD_OtherParties_95L_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceD_OtherParties_95P_Type with content type SIMPLE
class MT518_SequenceD_OtherParties_95P_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceD_OtherParties_95P_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceD_OtherParties_95P_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceD_OtherParties_95P_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1204, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceD_OtherParties_95P_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceD_OtherParties_95P_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='95P')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1207, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1207, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceD_OtherParties_95P_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1208, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1208, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceD_OtherParties_95P_Type = MT518_SequenceD_OtherParties_95P_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceD_OtherParties_95P_Type', MT518_SequenceD_OtherParties_95P_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceD_OtherParties_95Q_Type with content type SIMPLE
class MT518_SequenceD_OtherParties_95Q_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceD_OtherParties_95Q_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceD_OtherParties_95Q_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceD_OtherParties_95Q_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1217, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceD_OtherParties_95Q_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceD_OtherParties_95Q_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='95Q')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1220, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1220, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceD_OtherParties_95Q_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1221, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1221, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceD_OtherParties_95Q_Type = MT518_SequenceD_OtherParties_95Q_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceD_OtherParties_95Q_Type', MT518_SequenceD_OtherParties_95Q_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceD_OtherParties_95R_Type with content type SIMPLE
class MT518_SequenceD_OtherParties_95R_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceD_OtherParties_95R_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceD_OtherParties_95R_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceD_OtherParties_95R_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1230, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceD_OtherParties_95R_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceD_OtherParties_95R_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='95R')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1233, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1233, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceD_OtherParties_95R_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1234, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1234, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceD_OtherParties_95R_Type = MT518_SequenceD_OtherParties_95R_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceD_OtherParties_95R_Type', MT518_SequenceD_OtherParties_95R_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceD_OtherParties_95S_Type with content type SIMPLE
class MT518_SequenceD_OtherParties_95S_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceD_OtherParties_95S_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceD_OtherParties_95S_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceD_OtherParties_95S_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1243, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceD_OtherParties_95S_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceD_OtherParties_95S_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='95S')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1246, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1246, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceD_OtherParties_95S_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1247, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1247, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceD_OtherParties_95S_Type = MT518_SequenceD_OtherParties_95S_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceD_OtherParties_95S_Type', MT518_SequenceD_OtherParties_95S_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceD_OtherParties_97A_Type with content type SIMPLE
class MT518_SequenceD_OtherParties_97A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceD_OtherParties_97A_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceD_OtherParties_97A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceD_OtherParties_97A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1256, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceD_OtherParties_97A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceD_OtherParties_97A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='97A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1259, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1259, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceD_OtherParties_97A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1260, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1260, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceD_OtherParties_97A_Type = MT518_SequenceD_OtherParties_97A_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceD_OtherParties_97A_Type', MT518_SequenceD_OtherParties_97A_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceD_OtherParties_97B_Type with content type SIMPLE
class MT518_SequenceD_OtherParties_97B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceD_OtherParties_97B_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceD_OtherParties_97B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceD_OtherParties_97B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1269, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceD_OtherParties_97B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceD_OtherParties_97B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='97B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1272, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1272, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceD_OtherParties_97B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1273, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1273, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceD_OtherParties_97B_Type = MT518_SequenceD_OtherParties_97B_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceD_OtherParties_97B_Type', MT518_SequenceD_OtherParties_97B_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceD_OtherParties_97E_Type with content type SIMPLE
class MT518_SequenceD_OtherParties_97E_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceD_OtherParties_97E_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceD_OtherParties_97E_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceD_OtherParties_97E_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1282, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceD_OtherParties_97E_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceD_OtherParties_97E_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='97E')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1285, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1285, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceD_OtherParties_97E_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1286, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1286, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceD_OtherParties_97E_Type = MT518_SequenceD_OtherParties_97E_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceD_OtherParties_97E_Type', MT518_SequenceD_OtherParties_97E_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceD_OtherParties_70C_Type with content type SIMPLE
class MT518_SequenceD_OtherParties_70C_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceD_OtherParties_70C_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceD_OtherParties_70C_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceD_OtherParties_70C_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1295, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceD_OtherParties_70C_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceD_OtherParties_70C_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='70C')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1298, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1298, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceD_OtherParties_70C_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1299, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1299, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceD_OtherParties_70C_Type = MT518_SequenceD_OtherParties_70C_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceD_OtherParties_70C_Type', MT518_SequenceD_OtherParties_70C_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceD_OtherParties_20C_Type with content type SIMPLE
class MT518_SequenceD_OtherParties_20C_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceD_OtherParties_20C_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceD_OtherParties_20C_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceD_OtherParties_20C_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1308, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceD_OtherParties_20C_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceD_OtherParties_20C_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='20C')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1311, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1311, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceD_OtherParties_20C_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1312, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1312, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceD_OtherParties_20C_Type = MT518_SequenceD_OtherParties_20C_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceD_OtherParties_20C_Type', MT518_SequenceD_OtherParties_20C_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceE_TwoLegTransactionDetails_98A_Type with content type SIMPLE
class MT518_SequenceE_TwoLegTransactionDetails_98A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceE_TwoLegTransactionDetails_98A_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceE_TwoLegTransactionDetails_98A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceE_TwoLegTransactionDetails_98A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1321, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceE_TwoLegTransactionDetails_98A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceE_TwoLegTransactionDetails_98A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='98A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1324, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1324, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceE_TwoLegTransactionDetails_98A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1325, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1325, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceE_TwoLegTransactionDetails_98A_Type = MT518_SequenceE_TwoLegTransactionDetails_98A_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceE_TwoLegTransactionDetails_98A_Type', MT518_SequenceE_TwoLegTransactionDetails_98A_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceE_TwoLegTransactionDetails_98B_Type with content type SIMPLE
class MT518_SequenceE_TwoLegTransactionDetails_98B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceE_TwoLegTransactionDetails_98B_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceE_TwoLegTransactionDetails_98B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceE_TwoLegTransactionDetails_98B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1334, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceE_TwoLegTransactionDetails_98B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceE_TwoLegTransactionDetails_98B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='98B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1337, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1337, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceE_TwoLegTransactionDetails_98B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1338, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1338, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceE_TwoLegTransactionDetails_98B_Type = MT518_SequenceE_TwoLegTransactionDetails_98B_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceE_TwoLegTransactionDetails_98B_Type', MT518_SequenceE_TwoLegTransactionDetails_98B_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceE_TwoLegTransactionDetails_98C_Type with content type SIMPLE
class MT518_SequenceE_TwoLegTransactionDetails_98C_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceE_TwoLegTransactionDetails_98C_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceE_TwoLegTransactionDetails_98C_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceE_TwoLegTransactionDetails_98C_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1347, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceE_TwoLegTransactionDetails_98C_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceE_TwoLegTransactionDetails_98C_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='98C')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1350, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1350, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceE_TwoLegTransactionDetails_98C_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1351, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1351, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceE_TwoLegTransactionDetails_98C_Type = MT518_SequenceE_TwoLegTransactionDetails_98C_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceE_TwoLegTransactionDetails_98C_Type', MT518_SequenceE_TwoLegTransactionDetails_98C_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceE_TwoLegTransactionDetails_22F_Type with content type SIMPLE
class MT518_SequenceE_TwoLegTransactionDetails_22F_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceE_TwoLegTransactionDetails_22F_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceE_TwoLegTransactionDetails_22F_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceE_TwoLegTransactionDetails_22F_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1360, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceE_TwoLegTransactionDetails_22F_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceE_TwoLegTransactionDetails_22F_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='22F')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1363, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1363, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceE_TwoLegTransactionDetails_22F_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1364, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1364, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceE_TwoLegTransactionDetails_22F_Type = MT518_SequenceE_TwoLegTransactionDetails_22F_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceE_TwoLegTransactionDetails_22F_Type', MT518_SequenceE_TwoLegTransactionDetails_22F_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceE_TwoLegTransactionDetails_20C_Type with content type SIMPLE
class MT518_SequenceE_TwoLegTransactionDetails_20C_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceE_TwoLegTransactionDetails_20C_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceE_TwoLegTransactionDetails_20C_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceE_TwoLegTransactionDetails_20C_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1373, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceE_TwoLegTransactionDetails_20C_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceE_TwoLegTransactionDetails_20C_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='20C')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1376, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1376, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceE_TwoLegTransactionDetails_20C_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1377, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1377, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceE_TwoLegTransactionDetails_20C_Type = MT518_SequenceE_TwoLegTransactionDetails_20C_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceE_TwoLegTransactionDetails_20C_Type', MT518_SequenceE_TwoLegTransactionDetails_20C_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceE_TwoLegTransactionDetails_92A_Type with content type SIMPLE
class MT518_SequenceE_TwoLegTransactionDetails_92A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceE_TwoLegTransactionDetails_92A_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceE_TwoLegTransactionDetails_92A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceE_TwoLegTransactionDetails_92A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1386, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceE_TwoLegTransactionDetails_92A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceE_TwoLegTransactionDetails_92A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='92A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1389, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1389, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceE_TwoLegTransactionDetails_92A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1390, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1390, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceE_TwoLegTransactionDetails_92A_Type = MT518_SequenceE_TwoLegTransactionDetails_92A_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceE_TwoLegTransactionDetails_92A_Type', MT518_SequenceE_TwoLegTransactionDetails_92A_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceE_TwoLegTransactionDetails_92C_Type with content type SIMPLE
class MT518_SequenceE_TwoLegTransactionDetails_92C_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceE_TwoLegTransactionDetails_92C_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceE_TwoLegTransactionDetails_92C_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceE_TwoLegTransactionDetails_92C_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1399, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceE_TwoLegTransactionDetails_92C_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceE_TwoLegTransactionDetails_92C_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='92C')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1402, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1402, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceE_TwoLegTransactionDetails_92C_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1403, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1403, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceE_TwoLegTransactionDetails_92C_Type = MT518_SequenceE_TwoLegTransactionDetails_92C_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceE_TwoLegTransactionDetails_92C_Type', MT518_SequenceE_TwoLegTransactionDetails_92C_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceE_TwoLegTransactionDetails_99B_Type with content type SIMPLE
class MT518_SequenceE_TwoLegTransactionDetails_99B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceE_TwoLegTransactionDetails_99B_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceE_TwoLegTransactionDetails_99B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceE_TwoLegTransactionDetails_99B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1412, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceE_TwoLegTransactionDetails_99B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceE_TwoLegTransactionDetails_99B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='99B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1415, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1415, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceE_TwoLegTransactionDetails_99B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1416, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1416, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceE_TwoLegTransactionDetails_99B_Type = MT518_SequenceE_TwoLegTransactionDetails_99B_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceE_TwoLegTransactionDetails_99B_Type', MT518_SequenceE_TwoLegTransactionDetails_99B_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceE_TwoLegTransactionDetails_19A_Type with content type SIMPLE
class MT518_SequenceE_TwoLegTransactionDetails_19A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceE_TwoLegTransactionDetails_19A_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceE_TwoLegTransactionDetails_19A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceE_TwoLegTransactionDetails_19A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1425, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceE_TwoLegTransactionDetails_19A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceE_TwoLegTransactionDetails_19A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='19A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1428, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1428, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceE_TwoLegTransactionDetails_19A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1429, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1429, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceE_TwoLegTransactionDetails_19A_Type = MT518_SequenceE_TwoLegTransactionDetails_19A_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceE_TwoLegTransactionDetails_19A_Type', MT518_SequenceE_TwoLegTransactionDetails_19A_Type)


# Complex type {http://www.w3schools.com}MT518_SequenceE_TwoLegTransactionDetails_70C_Type with content type SIMPLE
class MT518_SequenceE_TwoLegTransactionDetails_70C_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT518_SequenceE_TwoLegTransactionDetails_70C_Type with content type SIMPLE"""
    _TypeDefinition = MT518_SequenceE_TwoLegTransactionDetails_70C_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT518_SequenceE_TwoLegTransactionDetails_70C_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1438, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT518_SequenceE_TwoLegTransactionDetails_70C_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT518_SequenceE_TwoLegTransactionDetails_70C_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='70C')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1441, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1441, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT518_SequenceE_TwoLegTransactionDetails_70C_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1442, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1442, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT518_SequenceE_TwoLegTransactionDetails_70C_Type = MT518_SequenceE_TwoLegTransactionDetails_70C_Type
Namespace.addCategoryObject('typeBinding', 'MT518_SequenceE_TwoLegTransactionDetails_70C_Type', MT518_SequenceE_TwoLegTransactionDetails_70C_Type)


MT518 = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'MT518'), CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1692, 1))
Namespace.addCategoryObject('elementBinding', MT518.name().localName(), MT518)



MT518_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SendersMessageReference'), MT518_SequenceA_GeneralInformation_20C_Type, scope=MT518_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1448, 3)))

MT518_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'FunctionOfTheMessage'), MT518_SequenceA_GeneralInformation_23G_Type, scope=MT518_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1449, 3)))

MT518_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PreparationDateTime_A'), MT518_SequenceA_GeneralInformation_98A_Type, scope=MT518_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1451, 4)))

MT518_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PreparationDateTime_C'), MT518_SequenceA_GeneralInformation_98C_Type, scope=MT518_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1452, 4)))

MT518_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PreparationDateTime_E'), MT518_SequenceA_GeneralInformation_98E_Type, scope=MT518_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1453, 4)))

MT518_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'TradeTransactionType'), MT518_SequenceA_GeneralInformation_22F_Type, scope=MT518_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1455, 3)))

MT518_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SubSequenceA1_Linkages'), MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages, scope=MT518_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1456, 3)))

def _BuildAutomaton ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1450, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1451, 4))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1452, 4))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1453, 4))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1456, 3))
    counters.add(cc_4)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SendersMessageReference')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1448, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'FunctionOfTheMessage')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1449, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PreparationDateTime_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1451, 4))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PreparationDateTime_C')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1452, 4))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PreparationDateTime_E')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1453, 4))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'TradeTransactionType')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1455, 3))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SubSequenceA1_Linkages')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1456, 3))
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
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
         ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_4, True) ]))
    st_6._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
MT518_SequenceA_GeneralInformation._Automaton = _BuildAutomaton()




MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'LinkedMessage_A'), MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13A_Type, scope=MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1465, 4)))

MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'LinkedMessage_B'), MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_13B_Type, scope=MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1466, 4)))

MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Reference_C'), MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20C_Type, scope=MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1469, 4)))

MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Reference_U'), MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages_20U_Type, scope=MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1470, 4)))

def _BuildAutomaton_ ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_
    del _BuildAutomaton_
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1464, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1465, 4))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1466, 4))
    counters.add(cc_2)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'LinkedMessage_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1465, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'LinkedMessage_B')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1466, 4))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Reference_C')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1469, 4))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Reference_U')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1470, 4))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
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
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_3, [
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
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_2, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    st_2._set_transitionSet(transitions)
    transitions = []
    st_3._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
MT518_SequenceA_GeneralInformation_SubSequenceA1_Linkages._Automaton = _BuildAutomaton_()




MT518_SequenceB_ConfirmationDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DateTime_A'), MT518_SequenceB_ConfirmationDetails_98A_Type, scope=MT518_SequenceB_ConfirmationDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1480, 4)))

MT518_SequenceB_ConfirmationDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DateTime_B'), MT518_SequenceB_ConfirmationDetails_98B_Type, scope=MT518_SequenceB_ConfirmationDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1481, 4)))

MT518_SequenceB_ConfirmationDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DateTime_C'), MT518_SequenceB_ConfirmationDetails_98C_Type, scope=MT518_SequenceB_ConfirmationDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1482, 4)))

MT518_SequenceB_ConfirmationDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DateTime_E'), MT518_SequenceB_ConfirmationDetails_98E_Type, scope=MT518_SequenceB_ConfirmationDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1483, 4)))

MT518_SequenceB_ConfirmationDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DealPrice_A'), MT518_SequenceB_ConfirmationDetails_90A_Type, scope=MT518_SequenceB_ConfirmationDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1486, 4)))

MT518_SequenceB_ConfirmationDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DealPrice_B'), MT518_SequenceB_ConfirmationDetails_90B_Type, scope=MT518_SequenceB_ConfirmationDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1487, 4)))

MT518_SequenceB_ConfirmationDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Rate'), MT518_SequenceB_ConfirmationDetails_92A_Type, scope=MT518_SequenceB_ConfirmationDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1489, 3)))

MT518_SequenceB_ConfirmationDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'NumberCount'), MT518_SequenceB_ConfirmationDetails_99A_Type, scope=MT518_SequenceB_ConfirmationDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1490, 3)))

MT518_SequenceB_ConfirmationDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Place_B'), MT518_SequenceB_ConfirmationDetails_94B_Type, scope=MT518_SequenceB_ConfirmationDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1492, 4)))

MT518_SequenceB_ConfirmationDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Place_C'), MT518_SequenceB_ConfirmationDetails_94C_Type, scope=MT518_SequenceB_ConfirmationDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1493, 4)))

MT518_SequenceB_ConfirmationDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Place_F'), MT518_SequenceB_ConfirmationDetails_94F_Type, scope=MT518_SequenceB_ConfirmationDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1494, 4)))

MT518_SequenceB_ConfirmationDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Place_L'), MT518_SequenceB_ConfirmationDetails_94L_Type, scope=MT518_SequenceB_ConfirmationDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1495, 4)))

MT518_SequenceB_ConfirmationDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SettlementAmount'), MT518_SequenceB_ConfirmationDetails_19A_Type, scope=MT518_SequenceB_ConfirmationDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1497, 3)))

MT518_SequenceB_ConfirmationDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Indicator_F'), MT518_SequenceB_ConfirmationDetails_22F_Type, scope=MT518_SequenceB_ConfirmationDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1499, 4)))

MT518_SequenceB_ConfirmationDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Indicator_H'), MT518_SequenceB_ConfirmationDetails_22H_Type, scope=MT518_SequenceB_ConfirmationDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1500, 4)))

MT518_SequenceB_ConfirmationDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Currency'), MT518_SequenceB_ConfirmationDetails_11A_Type, scope=MT518_SequenceB_ConfirmationDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1502, 3)))

MT518_SequenceB_ConfirmationDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SubSequenceB1_ConfirmationParties'), MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties, scope=MT518_SequenceB_ConfirmationDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1503, 3)))

MT518_SequenceB_ConfirmationDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'QuantityOfFinancialInstrument'), MT518_SequenceB_ConfirmationDetails_36B_Type, scope=MT518_SequenceB_ConfirmationDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1504, 3)))

MT518_SequenceB_ConfirmationDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'IdentificationOfTheFinancialInstrument'), MT518_SequenceB_ConfirmationDetails_35B_Type, scope=MT518_SequenceB_ConfirmationDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1505, 3)))

MT518_SequenceB_ConfirmationDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SubSequenceB2_FinancialInstrumentAttribute'), MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute, scope=MT518_SequenceB_ConfirmationDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1506, 3)))

MT518_SequenceB_ConfirmationDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'CertificateNumber'), MT518_SequenceB_ConfirmationDetails_13B_Type, scope=MT518_SequenceB_ConfirmationDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1507, 3)))

MT518_SequenceB_ConfirmationDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Narrative'), MT518_SequenceB_ConfirmationDetails_70E_Type, scope=MT518_SequenceB_ConfirmationDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1508, 3)))

def _BuildAutomaton_2 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_2
    del _BuildAutomaton_2
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1489, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1490, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1491, 3))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1492, 4))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1493, 4))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1494, 4))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1495, 4))
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1497, 3))
    counters.add(cc_7)
    cc_8 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1502, 3))
    counters.add(cc_8)
    cc_9 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1506, 3))
    counters.add(cc_9)
    cc_10 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1507, 3))
    counters.add(cc_10)
    cc_11 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1508, 3))
    counters.add(cc_11)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceB_ConfirmationDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'DateTime_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1480, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceB_ConfirmationDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'DateTime_B')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1481, 4))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceB_ConfirmationDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'DateTime_C')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1482, 4))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceB_ConfirmationDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'DateTime_E')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1483, 4))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceB_ConfirmationDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'DealPrice_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1486, 4))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceB_ConfirmationDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'DealPrice_B')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1487, 4))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceB_ConfirmationDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Rate')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1489, 3))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceB_ConfirmationDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'NumberCount')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1490, 3))
    st_7 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceB_ConfirmationDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Place_B')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1492, 4))
    st_8 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceB_ConfirmationDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Place_C')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1493, 4))
    st_9 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceB_ConfirmationDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Place_F')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1494, 4))
    st_10 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_10)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceB_ConfirmationDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Place_L')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1495, 4))
    st_11 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_11)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceB_ConfirmationDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SettlementAmount')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1497, 3))
    st_12 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_12)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceB_ConfirmationDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Indicator_F')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1499, 4))
    st_13 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_13)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceB_ConfirmationDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Indicator_H')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1500, 4))
    st_14 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_14)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceB_ConfirmationDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Currency')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1502, 3))
    st_15 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_15)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceB_ConfirmationDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SubSequenceB1_ConfirmationParties')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1503, 3))
    st_16 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_16)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceB_ConfirmationDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'QuantityOfFinancialInstrument')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1504, 3))
    st_17 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_17)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceB_ConfirmationDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'IdentificationOfTheFinancialInstrument')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1505, 3))
    st_18 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_18)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_9, False))
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceB_ConfirmationDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SubSequenceB2_FinancialInstrumentAttribute')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1506, 3))
    st_19 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_19)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_10, False))
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceB_ConfirmationDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'CertificateNumber')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1507, 3))
    st_20 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_20)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_11, False))
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceB_ConfirmationDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Narrative')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1508, 3))
    st_21 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_21)
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
    st_3._set_transitionSet(transitions)
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
    transitions.append(fac.Transition(st_14, [
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
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_1, True) ]))
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
    st_7._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_2, True),
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_3, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_2, True),
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_2, True),
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_2, True),
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
    st_8._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_2, True),
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_2, True),
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_4, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_2, True),
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_2, True),
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
    st_9._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_2, True),
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_2, True),
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_2, True),
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_5, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_2, True),
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
    st_10._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_2, True),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_2, True),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_2, True),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_2, True),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_6, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_2, False),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_2, False),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_2, False),
        fac.UpdateInstruction(cc_6, False) ]))
    st_11._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_7, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_7, False) ]))
    st_12._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_13, [
         ]))
    transitions.append(fac.Transition(st_14, [
         ]))
    transitions.append(fac.Transition(st_15, [
         ]))
    transitions.append(fac.Transition(st_16, [
         ]))
    st_13._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_13, [
         ]))
    transitions.append(fac.Transition(st_14, [
         ]))
    transitions.append(fac.Transition(st_15, [
         ]))
    transitions.append(fac.Transition(st_16, [
         ]))
    st_14._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_8, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_8, False) ]))
    st_15._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_16, [
         ]))
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
    st_18._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_9, True) ]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_9, False) ]))
    st_19._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_10, True) ]))
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_10, False) ]))
    st_20._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_11, True) ]))
    st_21._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
MT518_SequenceB_ConfirmationDetails._Automaton = _BuildAutomaton_2()




MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PARTY_L'), MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95L_Type, scope=MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1517, 4)))

MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PARTY_P'), MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95P_Type, scope=MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1518, 4)))

MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PARTY_Q'), MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95Q_Type, scope=MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1519, 4)))

MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PARTY_R'), MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95R_Type, scope=MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1520, 4)))

MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PARTY_S'), MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_95S_Type, scope=MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1521, 4)))

MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Account_A'), MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_97A_Type, scope=MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1524, 4)))

MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Account_B'), MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_97B_Type, scope=MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1525, 4)))

MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Account_E'), MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_97E_Type, scope=MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1526, 4)))

MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ProcessingDateTime_A'), MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_98A_Type, scope=MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1529, 4)))

MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ProcessingDateTime_C'), MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_98C_Type, scope=MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1530, 4)))

MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ProcessingReference'), MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_20C_Type, scope=MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1532, 3)))

MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Narrative_C'), MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_70C_Type, scope=MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1534, 4)))

MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Narrative_E'), MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_70E_Type, scope=MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1535, 4)))

MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Indicator'), MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties_22F_Type, scope=MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1537, 3)))

def _BuildAutomaton_3 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_3
    del _BuildAutomaton_3
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1523, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1524, 4))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1525, 4))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1526, 4))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1528, 3))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1529, 4))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1530, 4))
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1532, 3))
    counters.add(cc_7)
    cc_8 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1533, 3))
    counters.add(cc_8)
    cc_9 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1534, 4))
    counters.add(cc_9)
    cc_10 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1535, 4))
    counters.add(cc_10)
    cc_11 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1537, 3))
    counters.add(cc_11)
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PARTY_L')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1517, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PARTY_P')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1518, 4))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PARTY_Q')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1519, 4))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PARTY_R')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1520, 4))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PARTY_S')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1521, 4))
    st_4 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Account_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1524, 4))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Account_B')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1525, 4))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Account_E')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1526, 4))
    st_7 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    final_update.add(fac.UpdateInstruction(cc_5, False))
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ProcessingDateTime_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1529, 4))
    st_8 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    final_update.add(fac.UpdateInstruction(cc_6, False))
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ProcessingDateTime_C')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1530, 4))
    st_9 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_7, False))
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ProcessingReference')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1532, 3))
    st_10 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_10)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_8, False))
    final_update.add(fac.UpdateInstruction(cc_9, False))
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Narrative_C')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1534, 4))
    st_11 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_11)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_8, False))
    final_update.add(fac.UpdateInstruction(cc_10, False))
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Narrative_E')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1535, 4))
    st_12 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_12)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_11, False))
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Indicator')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1537, 3))
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
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True),
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True),
        fac.UpdateInstruction(cc_1, False) ]))
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
        fac.UpdateInstruction(cc_0, True),
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
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True),
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True),
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, True),
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_3, True) ]))
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
    st_7._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_4, True),
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_5, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_4, True),
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
    st_8._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_4, True),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_4, True),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_6, True) ]))
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
    st_9._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_7, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_7, False) ]))
    st_10._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_8, True),
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_9, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_8, True),
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_8, False),
        fac.UpdateInstruction(cc_9, False) ]))
    st_11._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_8, True),
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_8, True),
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_10, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_8, False),
        fac.UpdateInstruction(cc_10, False) ]))
    st_12._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_11, True) ]))
    st_13._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
MT518_SequenceB_ConfirmationDetails_SubSequenceB1_ConfirmationParties._Automaton = _BuildAutomaton_3()




MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PlaceOfListing'), MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_94B_Type, scope=MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1545, 3)))

MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Indicator'), MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_22F_Type, scope=MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1546, 3)))

MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'TypeOfFinancialInstrument_A'), MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_12A_Type, scope=MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1548, 4)))

MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'TypeOfFinancialInstrument_B'), MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_12B_Type, scope=MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1549, 4)))

MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'TypeOfFinancialInstrument_C'), MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_12C_Type, scope=MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1550, 4)))

MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'CurrencyOfDenomination'), MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_11A_Type, scope=MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1552, 3)))

MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DateTime'), MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_98A_Type, scope=MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1553, 3)))

MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Rate'), MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_92A_Type, scope=MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1554, 3)))

MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'NumberIdentification_A'), MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_13A_Type, scope=MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1556, 4)))

MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'NumberIdentification_B'), MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_13B_Type, scope=MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1557, 4)))

MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Flag'), MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_17B_Type, scope=MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1559, 3)))

MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Price_A'), MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_90A_Type, scope=MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1561, 4)))

MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Price_B'), MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_90B_Type, scope=MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1562, 4)))

MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'QuantityOfFinancialInstrument'), MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_36B_Type, scope=MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1564, 3)))

MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'IdentificationOfTheFinancialInstrument'), MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_35B_Type, scope=MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1565, 3)))

MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'FinancialInstrumentAttributeNarrative'), MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute_70E_Type, scope=MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1566, 3)))

def _BuildAutomaton_4 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_4
    del _BuildAutomaton_4
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1545, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1546, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1547, 3))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1548, 4))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1549, 4))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1550, 4))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1552, 3))
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1553, 3))
    counters.add(cc_7)
    cc_8 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1554, 3))
    counters.add(cc_8)
    cc_9 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1555, 3))
    counters.add(cc_9)
    cc_10 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1556, 4))
    counters.add(cc_10)
    cc_11 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1557, 4))
    counters.add(cc_11)
    cc_12 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1559, 3))
    counters.add(cc_12)
    cc_13 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1560, 3))
    counters.add(cc_13)
    cc_14 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1561, 4))
    counters.add(cc_14)
    cc_15 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1562, 4))
    counters.add(cc_15)
    cc_16 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1564, 3))
    counters.add(cc_16)
    cc_17 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1565, 3))
    counters.add(cc_17)
    cc_18 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1566, 3))
    counters.add(cc_18)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PlaceOfListing')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1545, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Indicator')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1546, 3))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'TypeOfFinancialInstrument_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1548, 4))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'TypeOfFinancialInstrument_B')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1549, 4))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    final_update.add(fac.UpdateInstruction(cc_5, False))
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'TypeOfFinancialInstrument_C')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1550, 4))
    st_4 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_6, False))
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'CurrencyOfDenomination')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1552, 3))
    st_5 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_7, False))
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'DateTime')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1553, 3))
    st_6 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_8, False))
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Rate')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1554, 3))
    st_7 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_9, False))
    final_update.add(fac.UpdateInstruction(cc_10, False))
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'NumberIdentification_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1556, 4))
    st_8 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_9, False))
    final_update.add(fac.UpdateInstruction(cc_11, False))
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'NumberIdentification_B')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1557, 4))
    st_9 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_12, False))
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Flag')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1559, 3))
    st_10 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_10)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_13, False))
    final_update.add(fac.UpdateInstruction(cc_14, False))
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Price_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1561, 4))
    st_11 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_11)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_13, False))
    final_update.add(fac.UpdateInstruction(cc_15, False))
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Price_B')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1562, 4))
    st_12 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_12)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_16, False))
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'QuantityOfFinancialInstrument')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1564, 3))
    st_13 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_13)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_17, False))
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'IdentificationOfTheFinancialInstrument')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1565, 3))
    st_14 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_14)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_18, False))
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'FinancialInstrumentAttributeNarrative')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1566, 3))
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
MT518_SequenceB_ConfirmationDetails_SubSequenceB2_FinancialInstrumentAttribute._Automaton = _BuildAutomaton_4()




MT518_SequenceC_SettlementDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Indicator'), MT518_SequenceC_SettlementDetails_22F_Type, scope=MT518_SequenceC_SettlementDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1574, 3)))

MT518_SequenceC_SettlementDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Currency'), MT518_SequenceC_SettlementDetails_11A_Type, scope=MT518_SequenceC_SettlementDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1575, 3)))

MT518_SequenceC_SettlementDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SubSequenceC1_SettlementParties'), MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties, scope=MT518_SequenceC_SettlementDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1576, 3)))

MT518_SequenceC_SettlementDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SubSequenceC2_CashParties'), MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties, scope=MT518_SequenceC_SettlementDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1577, 3)))

MT518_SequenceC_SettlementDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SubSequenceC3_Amounts'), MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts, scope=MT518_SequenceC_SettlementDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1578, 3)))

def _BuildAutomaton_5 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_5
    del _BuildAutomaton_5
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1575, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1576, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1577, 3))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1578, 3))
    counters.add(cc_3)
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceC_SettlementDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Indicator')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1574, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceC_SettlementDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Currency')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1575, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceC_SettlementDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SubSequenceC1_SettlementParties')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1576, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceC_SettlementDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SubSequenceC2_CashParties')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1577, 3))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceC_SettlementDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SubSequenceC3_Amounts')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1578, 3))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
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
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_3, True) ]))
    st_4._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
MT518_SequenceC_SettlementDetails._Automaton = _BuildAutomaton_5()




MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PARTY_C'), MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95C_Type, scope=MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1587, 4)))

MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PARTY_L'), MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95L_Type, scope=MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1588, 4)))

MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PARTY_P'), MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95P_Type, scope=MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1589, 4)))

MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PARTY_Q'), MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95Q_Type, scope=MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1590, 4)))

MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PARTY_R'), MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95R_Type, scope=MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1591, 4)))

MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PARTY_S'), MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_95S_Type, scope=MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1592, 4)))

MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SafekeepingAccount_A'), MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_97A_Type, scope=MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1595, 4)))

MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SafekeepingAccount_B'), MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_97B_Type, scope=MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1596, 4)))

MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ProcessingDateTime_A'), MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_98A_Type, scope=MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1599, 4)))

MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ProcessingDateTime_C'), MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_98C_Type, scope=MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1600, 4)))

MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ProcessingReference'), MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_20C_Type, scope=MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1602, 3)))

MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Narrative_C'), MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_70C_Type, scope=MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1604, 4)))

MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Narrative_D'), MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties_70D_Type, scope=MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1605, 4)))

def _BuildAutomaton_6 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_6
    del _BuildAutomaton_6
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1594, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1595, 4))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1596, 4))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1598, 3))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1599, 4))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1600, 4))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1602, 3))
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1603, 3))
    counters.add(cc_7)
    cc_8 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1604, 4))
    counters.add(cc_8)
    cc_9 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1605, 4))
    counters.add(cc_9)
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PARTY_C')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1587, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PARTY_L')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1588, 4))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PARTY_P')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1589, 4))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PARTY_Q')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1590, 4))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PARTY_R')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1591, 4))
    st_4 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PARTY_S')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1592, 4))
    st_5 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SafekeepingAccount_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1595, 4))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SafekeepingAccount_B')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1596, 4))
    st_7 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ProcessingDateTime_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1599, 4))
    st_8 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    final_update.add(fac.UpdateInstruction(cc_5, False))
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ProcessingDateTime_C')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1600, 4))
    st_9 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_6, False))
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ProcessingReference')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1602, 3))
    st_10 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_10)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_7, False))
    final_update.add(fac.UpdateInstruction(cc_8, False))
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Narrative_C')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1604, 4))
    st_11 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_11)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_7, False))
    final_update.add(fac.UpdateInstruction(cc_9, False))
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Narrative_D')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1605, 4))
    st_12 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_12)
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
    st_9._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_6, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_12, [
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
    st_12._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
MT518_SequenceC_SettlementDetails_SubSequenceC1_SettlementParties._Automaton = _BuildAutomaton_6()




MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PARTY_L'), MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95L_Type, scope=MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1615, 4)))

MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PARTY_P'), MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95P_Type, scope=MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1616, 4)))

MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PARTY_Q'), MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95Q_Type, scope=MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1617, 4)))

MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PARTY_R'), MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95R_Type, scope=MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1618, 4)))

MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PARTY_S'), MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_95S_Type, scope=MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1619, 4)))

MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Account_A'), MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_97A_Type, scope=MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1622, 4)))

MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Account_E'), MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_97E_Type, scope=MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1623, 4)))

MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ProcessingDateTime_A'), MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_98A_Type, scope=MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1626, 4)))

MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ProcessingDateTime_C'), MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_98C_Type, scope=MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1627, 4)))

MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ProcessingReference'), MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_20C_Type, scope=MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1629, 3)))

MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PartyNarrative'), MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties_70C_Type, scope=MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1630, 3)))

def _BuildAutomaton_7 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_7
    del _BuildAutomaton_7
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1621, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1622, 4))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1623, 4))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1625, 3))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1626, 4))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1627, 4))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1629, 3))
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1630, 3))
    counters.add(cc_7)
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PARTY_L')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1615, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PARTY_P')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1616, 4))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PARTY_Q')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1617, 4))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PARTY_R')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1618, 4))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PARTY_S')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1619, 4))
    st_4 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Account_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1622, 4))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Account_E')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1623, 4))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ProcessingDateTime_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1626, 4))
    st_7 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    final_update.add(fac.UpdateInstruction(cc_5, False))
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ProcessingDateTime_C')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1627, 4))
    st_8 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_6, False))
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ProcessingReference')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1629, 3))
    st_9 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_7, False))
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PartyNarrative')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1630, 3))
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
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_10, [
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
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_10, [
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
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_3, False),
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_3, False),
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
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_3, False),
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_3, False),
        fac.UpdateInstruction(cc_5, False) ]))
    st_8._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_6, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_6, False) ]))
    st_9._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_7, True) ]))
    st_10._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
MT518_SequenceC_SettlementDetails_SubSequenceC2_CashParties._Automaton = _BuildAutomaton_7()




MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Flag'), MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_17B_Type, scope=MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1638, 3)))

MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Amount'), MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_19A_Type, scope=MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1639, 3)))

MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ValueDateTime_A'), MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_98A_Type, scope=MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1641, 4)))

MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ValueDateTime_C'), MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_98C_Type, scope=MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1642, 4)))

MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ExchangeRate'), MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts_92B_Type, scope=MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1644, 3)))

def _BuildAutomaton_8 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_8
    del _BuildAutomaton_8
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1638, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1640, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1641, 4))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1642, 4))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1644, 3))
    counters.add(cc_4)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Flag')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1638, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Amount')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1639, 3))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ValueDateTime_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1641, 4))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ValueDateTime_C')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1642, 4))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ExchangeRate')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1644, 3))
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
MT518_SequenceC_SettlementDetails_SubSequenceC3_Amounts._Automaton = _BuildAutomaton_8()




MT518_SequenceD_OtherParties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PARTY_L'), MT518_SequenceD_OtherParties_95L_Type, scope=MT518_SequenceD_OtherParties, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1653, 4)))

MT518_SequenceD_OtherParties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PARTY_P'), MT518_SequenceD_OtherParties_95P_Type, scope=MT518_SequenceD_OtherParties, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1654, 4)))

MT518_SequenceD_OtherParties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PARTY_Q'), MT518_SequenceD_OtherParties_95Q_Type, scope=MT518_SequenceD_OtherParties, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1655, 4)))

MT518_SequenceD_OtherParties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PARTY_R'), MT518_SequenceD_OtherParties_95R_Type, scope=MT518_SequenceD_OtherParties, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1656, 4)))

MT518_SequenceD_OtherParties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PARTY_S'), MT518_SequenceD_OtherParties_95S_Type, scope=MT518_SequenceD_OtherParties, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1657, 4)))

MT518_SequenceD_OtherParties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Account_A'), MT518_SequenceD_OtherParties_97A_Type, scope=MT518_SequenceD_OtherParties, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1660, 4)))

MT518_SequenceD_OtherParties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Account_B'), MT518_SequenceD_OtherParties_97B_Type, scope=MT518_SequenceD_OtherParties, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1661, 4)))

MT518_SequenceD_OtherParties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Account_E'), MT518_SequenceD_OtherParties_97E_Type, scope=MT518_SequenceD_OtherParties, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1662, 4)))

MT518_SequenceD_OtherParties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PartyNarrative'), MT518_SequenceD_OtherParties_70C_Type, scope=MT518_SequenceD_OtherParties, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1664, 3)))

MT518_SequenceD_OtherParties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ProcessingReference'), MT518_SequenceD_OtherParties_20C_Type, scope=MT518_SequenceD_OtherParties, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1665, 3)))

def _BuildAutomaton_9 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_9
    del _BuildAutomaton_9
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1659, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1660, 4))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1661, 4))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1662, 4))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1664, 3))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1665, 3))
    counters.add(cc_5)
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceD_OtherParties._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PARTY_L')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1653, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceD_OtherParties._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PARTY_P')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1654, 4))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceD_OtherParties._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PARTY_Q')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1655, 4))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceD_OtherParties._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PARTY_R')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1656, 4))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceD_OtherParties._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PARTY_S')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1657, 4))
    st_4 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceD_OtherParties._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Account_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1660, 4))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceD_OtherParties._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Account_B')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1661, 4))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceD_OtherParties._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Account_E')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1662, 4))
    st_7 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceD_OtherParties._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PartyNarrative')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1664, 3))
    st_8 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_5, False))
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceD_OtherParties._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ProcessingReference')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1665, 3))
    st_9 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
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
        fac.UpdateInstruction(cc_0, True),
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_9, [
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
        fac.UpdateInstruction(cc_0, True),
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_2, False) ]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True),
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True),
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, True),
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_3, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_3, False) ]))
    st_7._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_4, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_4, False) ]))
    st_8._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_5, True) ]))
    st_9._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
MT518_SequenceD_OtherParties._Automaton = _BuildAutomaton_9()




MT518_SequenceE_TwoLegTransactionDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DateTime_A'), MT518_SequenceE_TwoLegTransactionDetails_98A_Type, scope=MT518_SequenceE_TwoLegTransactionDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1674, 4)))

MT518_SequenceE_TwoLegTransactionDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DateTime_B'), MT518_SequenceE_TwoLegTransactionDetails_98B_Type, scope=MT518_SequenceE_TwoLegTransactionDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1675, 4)))

MT518_SequenceE_TwoLegTransactionDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DateTime_C'), MT518_SequenceE_TwoLegTransactionDetails_98C_Type, scope=MT518_SequenceE_TwoLegTransactionDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1676, 4)))

MT518_SequenceE_TwoLegTransactionDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Indicator'), MT518_SequenceE_TwoLegTransactionDetails_22F_Type, scope=MT518_SequenceE_TwoLegTransactionDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1678, 3)))

MT518_SequenceE_TwoLegTransactionDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Reference'), MT518_SequenceE_TwoLegTransactionDetails_20C_Type, scope=MT518_SequenceE_TwoLegTransactionDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1679, 3)))

MT518_SequenceE_TwoLegTransactionDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Rate_A'), MT518_SequenceE_TwoLegTransactionDetails_92A_Type, scope=MT518_SequenceE_TwoLegTransactionDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1681, 4)))

MT518_SequenceE_TwoLegTransactionDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Rate_C'), MT518_SequenceE_TwoLegTransactionDetails_92C_Type, scope=MT518_SequenceE_TwoLegTransactionDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1682, 4)))

MT518_SequenceE_TwoLegTransactionDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'NumberCount'), MT518_SequenceE_TwoLegTransactionDetails_99B_Type, scope=MT518_SequenceE_TwoLegTransactionDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1684, 3)))

MT518_SequenceE_TwoLegTransactionDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Amount'), MT518_SequenceE_TwoLegTransactionDetails_19A_Type, scope=MT518_SequenceE_TwoLegTransactionDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1685, 3)))

MT518_SequenceE_TwoLegTransactionDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SecondLegNarrative'), MT518_SequenceE_TwoLegTransactionDetails_70C_Type, scope=MT518_SequenceE_TwoLegTransactionDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1686, 3)))

def _BuildAutomaton_10 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_10
    del _BuildAutomaton_10
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1673, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1674, 4))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1675, 4))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1676, 4))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1678, 3))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1679, 3))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1680, 3))
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1681, 4))
    counters.add(cc_7)
    cc_8 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1682, 4))
    counters.add(cc_8)
    cc_9 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1684, 3))
    counters.add(cc_9)
    cc_10 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1685, 3))
    counters.add(cc_10)
    cc_11 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1686, 3))
    counters.add(cc_11)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceE_TwoLegTransactionDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'DateTime_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1674, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceE_TwoLegTransactionDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'DateTime_B')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1675, 4))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceE_TwoLegTransactionDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'DateTime_C')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1676, 4))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceE_TwoLegTransactionDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Indicator')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1678, 3))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_5, False))
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceE_TwoLegTransactionDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Reference')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1679, 3))
    st_4 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_6, False))
    final_update.add(fac.UpdateInstruction(cc_7, False))
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceE_TwoLegTransactionDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Rate_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1681, 4))
    st_5 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_6, False))
    final_update.add(fac.UpdateInstruction(cc_8, False))
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceE_TwoLegTransactionDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Rate_C')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1682, 4))
    st_6 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_9, False))
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceE_TwoLegTransactionDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'NumberCount')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1684, 3))
    st_7 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_10, False))
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceE_TwoLegTransactionDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Amount')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1685, 3))
    st_8 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_11, False))
    symbol = pyxb.binding.content.ElementUse(MT518_SequenceE_TwoLegTransactionDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SecondLegNarrative')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1686, 3))
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
MT518_SequenceE_TwoLegTransactionDetails._Automaton = _BuildAutomaton_10()




CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SequenceA_GeneralInformation'), MT518_SequenceA_GeneralInformation, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1695, 4)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SequenceB_ConfirmationDetails'), MT518_SequenceB_ConfirmationDetails, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1696, 4)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SequenceC_SettlementDetails'), MT518_SequenceC_SettlementDetails, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1697, 4)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SequenceD_OtherParties'), MT518_SequenceD_OtherParties, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1698, 4)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SequenceE_TwoLegTransactionDetails'), MT518_SequenceE_TwoLegTransactionDetails, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1699, 4)))

def _BuildAutomaton_11 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_11
    del _BuildAutomaton_11
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1697, 4))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1698, 4))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1699, 4))
    counters.add(cc_2)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SequenceA_GeneralInformation')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1695, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SequenceB_ConfirmationDetails')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1696, 4))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SequenceC_SettlementDetails')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1697, 4))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SequenceD_OtherParties')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1698, 4))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SequenceE_TwoLegTransactionDetails')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT518.xsd', 1699, 4))
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
CTD_ANON._Automaton = _BuildAutomaton_11()


