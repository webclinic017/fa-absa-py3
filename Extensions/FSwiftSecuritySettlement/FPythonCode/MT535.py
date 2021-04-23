# C:\Swift\Templates\MT535.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:96afad3d20bbfe8d040a1a097fa388d9fecd10e3
# Generated 2019-11-26 18:20:25.317012 by PyXB version 1.2.6 using Python 3.7.4.final.0
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
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:50a9104c-104b-11ea-a489-8851fb4dff7a')

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


# Atomic simple type: {http://www.w3schools.com}MT535_SequenceA_GeneralInformation_28E_Type_Pattern
class MT535_SequenceA_GeneralInformation_28E_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceA_GeneralInformation_28E_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 3, 1)
    _Documentation = None
MT535_SequenceA_GeneralInformation_28E_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT535_SequenceA_GeneralInformation_28E_Type_Pattern._CF_pattern.addPattern(pattern='([0-9]{1,5}/(ONLY|LAST|MORE))')
MT535_SequenceA_GeneralInformation_28E_Type_Pattern._InitializeFacetMap(MT535_SequenceA_GeneralInformation_28E_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceA_GeneralInformation_28E_Type_Pattern', MT535_SequenceA_GeneralInformation_28E_Type_Pattern)
_module_typeBindings.MT535_SequenceA_GeneralInformation_28E_Type_Pattern = MT535_SequenceA_GeneralInformation_28E_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT535_SequenceA_GeneralInformation_13A_Type_Pattern
class MT535_SequenceA_GeneralInformation_13A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceA_GeneralInformation_13A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 24, 1)
    _Documentation = None
MT535_SequenceA_GeneralInformation_13A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT535_SequenceA_GeneralInformation_13A_Type_Pattern._CF_pattern.addPattern(pattern='(:[A-Z0-9]{4}//[A-Z0-9]{3})')
MT535_SequenceA_GeneralInformation_13A_Type_Pattern._InitializeFacetMap(MT535_SequenceA_GeneralInformation_13A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceA_GeneralInformation_13A_Type_Pattern', MT535_SequenceA_GeneralInformation_13A_Type_Pattern)
_module_typeBindings.MT535_SequenceA_GeneralInformation_13A_Type_Pattern = MT535_SequenceA_GeneralInformation_13A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT535_SequenceA_GeneralInformation_13J_Type_Pattern
class MT535_SequenceA_GeneralInformation_13J_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceA_GeneralInformation_13J_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 37, 1)
    _Documentation = None
MT535_SequenceA_GeneralInformation_13J_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT535_SequenceA_GeneralInformation_13J_Type_Pattern._CF_pattern.addPattern(pattern='(:[A-Z0-9]{4}//[A-Z0-9]{5})')
MT535_SequenceA_GeneralInformation_13J_Type_Pattern._InitializeFacetMap(MT535_SequenceA_GeneralInformation_13J_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceA_GeneralInformation_13J_Type_Pattern', MT535_SequenceA_GeneralInformation_13J_Type_Pattern)
_module_typeBindings.MT535_SequenceA_GeneralInformation_13J_Type_Pattern = MT535_SequenceA_GeneralInformation_13J_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT535_SequenceA_GeneralInformation_20C_Type_Pattern
class MT535_SequenceA_GeneralInformation_20C_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceA_GeneralInformation_20C_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 50, 1)
    _Documentation = None
MT535_SequenceA_GeneralInformation_20C_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT535_SequenceA_GeneralInformation_20C_Type_Pattern._CF_pattern.addPattern(pattern="(:[A-Z0-9]{4}//([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,16})")
MT535_SequenceA_GeneralInformation_20C_Type_Pattern._InitializeFacetMap(MT535_SequenceA_GeneralInformation_20C_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceA_GeneralInformation_20C_Type_Pattern', MT535_SequenceA_GeneralInformation_20C_Type_Pattern)
_module_typeBindings.MT535_SequenceA_GeneralInformation_20C_Type_Pattern = MT535_SequenceA_GeneralInformation_20C_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT535_SequenceA_GeneralInformation_23G_Type_Pattern
class MT535_SequenceA_GeneralInformation_23G_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceA_GeneralInformation_23G_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 63, 1)
    _Documentation = None
MT535_SequenceA_GeneralInformation_23G_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT535_SequenceA_GeneralInformation_23G_Type_Pattern._CF_pattern.addPattern(pattern='([A-Z0-9]{4}(/[A-Z0-9]{4})?)')
MT535_SequenceA_GeneralInformation_23G_Type_Pattern._InitializeFacetMap(MT535_SequenceA_GeneralInformation_23G_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceA_GeneralInformation_23G_Type_Pattern', MT535_SequenceA_GeneralInformation_23G_Type_Pattern)
_module_typeBindings.MT535_SequenceA_GeneralInformation_23G_Type_Pattern = MT535_SequenceA_GeneralInformation_23G_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT535_SequenceA_GeneralInformation_98A_Type_Pattern
class MT535_SequenceA_GeneralInformation_98A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceA_GeneralInformation_98A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 76, 1)
    _Documentation = None
MT535_SequenceA_GeneralInformation_98A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT535_SequenceA_GeneralInformation_98A_Type_Pattern._CF_pattern.addPattern(pattern='(:[A-Z0-9]{4}//[0-9]{8})')
MT535_SequenceA_GeneralInformation_98A_Type_Pattern._InitializeFacetMap(MT535_SequenceA_GeneralInformation_98A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceA_GeneralInformation_98A_Type_Pattern', MT535_SequenceA_GeneralInformation_98A_Type_Pattern)
_module_typeBindings.MT535_SequenceA_GeneralInformation_98A_Type_Pattern = MT535_SequenceA_GeneralInformation_98A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT535_SequenceA_GeneralInformation_98C_Type_Pattern
class MT535_SequenceA_GeneralInformation_98C_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceA_GeneralInformation_98C_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 89, 1)
    _Documentation = None
MT535_SequenceA_GeneralInformation_98C_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT535_SequenceA_GeneralInformation_98C_Type_Pattern._CF_pattern.addPattern(pattern='(:[A-Z0-9]{4}//[0-9]{8}[0-9]{6})')
MT535_SequenceA_GeneralInformation_98C_Type_Pattern._InitializeFacetMap(MT535_SequenceA_GeneralInformation_98C_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceA_GeneralInformation_98C_Type_Pattern', MT535_SequenceA_GeneralInformation_98C_Type_Pattern)
_module_typeBindings.MT535_SequenceA_GeneralInformation_98C_Type_Pattern = MT535_SequenceA_GeneralInformation_98C_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT535_SequenceA_GeneralInformation_98E_Type_Pattern
class MT535_SequenceA_GeneralInformation_98E_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceA_GeneralInformation_98E_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 102, 1)
    _Documentation = None
MT535_SequenceA_GeneralInformation_98E_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT535_SequenceA_GeneralInformation_98E_Type_Pattern._CF_pattern.addPattern(pattern='(:[A-Z0-9]{4}//[0-9]{8}[0-9]{6}(,[0-9]{1,3})?(/(N)?[0-9]{2}([0-9]{2})?)?)')
MT535_SequenceA_GeneralInformation_98E_Type_Pattern._InitializeFacetMap(MT535_SequenceA_GeneralInformation_98E_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceA_GeneralInformation_98E_Type_Pattern', MT535_SequenceA_GeneralInformation_98E_Type_Pattern)
_module_typeBindings.MT535_SequenceA_GeneralInformation_98E_Type_Pattern = MT535_SequenceA_GeneralInformation_98E_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT535_SequenceA_GeneralInformation_22F_Type_Pattern
class MT535_SequenceA_GeneralInformation_22F_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceA_GeneralInformation_22F_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 115, 1)
    _Documentation = None
MT535_SequenceA_GeneralInformation_22F_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT535_SequenceA_GeneralInformation_22F_Type_Pattern._CF_pattern.addPattern(pattern='(:[A-Z0-9]{4}/([A-Z0-9]{1,8})?/[A-Z0-9]{4})')
MT535_SequenceA_GeneralInformation_22F_Type_Pattern._InitializeFacetMap(MT535_SequenceA_GeneralInformation_22F_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceA_GeneralInformation_22F_Type_Pattern', MT535_SequenceA_GeneralInformation_22F_Type_Pattern)
_module_typeBindings.MT535_SequenceA_GeneralInformation_22F_Type_Pattern = MT535_SequenceA_GeneralInformation_22F_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages_13A_Type_Pattern
class MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages_13A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages_13A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 128, 1)
    _Documentation = None
MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages_13A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages_13A_Type_Pattern._CF_pattern.addPattern(pattern='(:[A-Z0-9]{4}//[A-Z0-9]{3})')
MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages_13A_Type_Pattern._InitializeFacetMap(MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages_13A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages_13A_Type_Pattern', MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages_13A_Type_Pattern)
_module_typeBindings.MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages_13A_Type_Pattern = MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages_13A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages_13B_Type_Pattern
class MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages_13B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages_13B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 141, 1)
    _Documentation = None
MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages_13B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages_13B_Type_Pattern._CF_pattern.addPattern(pattern="(:[A-Z0-9]{4}/([A-Z0-9]{1,8})?/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,30})")
MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages_13B_Type_Pattern._InitializeFacetMap(MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages_13B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages_13B_Type_Pattern', MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages_13B_Type_Pattern)
_module_typeBindings.MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages_13B_Type_Pattern = MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages_13B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages_20C_Type_Pattern
class MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages_20C_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages_20C_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 154, 1)
    _Documentation = None
MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages_20C_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages_20C_Type_Pattern._CF_pattern.addPattern(pattern="(:[A-Z0-9]{4}//([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,16})")
MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages_20C_Type_Pattern._InitializeFacetMap(MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages_20C_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages_20C_Type_Pattern', MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages_20C_Type_Pattern)
_module_typeBindings.MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages_20C_Type_Pattern = MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages_20C_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT535_SequenceA_GeneralInformation_95L_Type_Pattern
class MT535_SequenceA_GeneralInformation_95L_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceA_GeneralInformation_95L_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 167, 1)
    _Documentation = None
MT535_SequenceA_GeneralInformation_95L_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT535_SequenceA_GeneralInformation_95L_Type_Pattern._CF_pattern.addPattern(pattern='(:[A-Z0-9]{4}//[A-Z0-9]{18}[0-9]{2})')
MT535_SequenceA_GeneralInformation_95L_Type_Pattern._InitializeFacetMap(MT535_SequenceA_GeneralInformation_95L_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceA_GeneralInformation_95L_Type_Pattern', MT535_SequenceA_GeneralInformation_95L_Type_Pattern)
_module_typeBindings.MT535_SequenceA_GeneralInformation_95L_Type_Pattern = MT535_SequenceA_GeneralInformation_95L_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT535_SequenceA_GeneralInformation_95P_Type_Pattern
class MT535_SequenceA_GeneralInformation_95P_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceA_GeneralInformation_95P_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 180, 1)
    _Documentation = None
MT535_SequenceA_GeneralInformation_95P_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT535_SequenceA_GeneralInformation_95P_Type_Pattern._CF_pattern.addPattern(pattern='(:[A-Z0-9]{4}//[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)')
MT535_SequenceA_GeneralInformation_95P_Type_Pattern._InitializeFacetMap(MT535_SequenceA_GeneralInformation_95P_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceA_GeneralInformation_95P_Type_Pattern', MT535_SequenceA_GeneralInformation_95P_Type_Pattern)
_module_typeBindings.MT535_SequenceA_GeneralInformation_95P_Type_Pattern = MT535_SequenceA_GeneralInformation_95P_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT535_SequenceA_GeneralInformation_95R_Type_Pattern
class MT535_SequenceA_GeneralInformation_95R_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceA_GeneralInformation_95R_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 193, 1)
    _Documentation = None
MT535_SequenceA_GeneralInformation_95R_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT535_SequenceA_GeneralInformation_95R_Type_Pattern._CF_pattern.addPattern(pattern="(:[A-Z0-9]{4}/[A-Z0-9]{1,8}/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})")
MT535_SequenceA_GeneralInformation_95R_Type_Pattern._InitializeFacetMap(MT535_SequenceA_GeneralInformation_95R_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceA_GeneralInformation_95R_Type_Pattern', MT535_SequenceA_GeneralInformation_95R_Type_Pattern)
_module_typeBindings.MT535_SequenceA_GeneralInformation_95R_Type_Pattern = MT535_SequenceA_GeneralInformation_95R_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT535_SequenceA_GeneralInformation_97A_Type_Pattern
class MT535_SequenceA_GeneralInformation_97A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceA_GeneralInformation_97A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 206, 1)
    _Documentation = None
MT535_SequenceA_GeneralInformation_97A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT535_SequenceA_GeneralInformation_97A_Type_Pattern._CF_pattern.addPattern(pattern="(:[A-Z0-9]{4}//([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35})")
MT535_SequenceA_GeneralInformation_97A_Type_Pattern._InitializeFacetMap(MT535_SequenceA_GeneralInformation_97A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceA_GeneralInformation_97A_Type_Pattern', MT535_SequenceA_GeneralInformation_97A_Type_Pattern)
_module_typeBindings.MT535_SequenceA_GeneralInformation_97A_Type_Pattern = MT535_SequenceA_GeneralInformation_97A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT535_SequenceA_GeneralInformation_97B_Type_Pattern
class MT535_SequenceA_GeneralInformation_97B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceA_GeneralInformation_97B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 219, 1)
    _Documentation = None
MT535_SequenceA_GeneralInformation_97B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT535_SequenceA_GeneralInformation_97B_Type_Pattern._CF_pattern.addPattern(pattern="(:[A-Z0-9]{4}/([A-Z0-9]{1,8})?/[A-Z0-9]{4}/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35})")
MT535_SequenceA_GeneralInformation_97B_Type_Pattern._InitializeFacetMap(MT535_SequenceA_GeneralInformation_97B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceA_GeneralInformation_97B_Type_Pattern', MT535_SequenceA_GeneralInformation_97B_Type_Pattern)
_module_typeBindings.MT535_SequenceA_GeneralInformation_97B_Type_Pattern = MT535_SequenceA_GeneralInformation_97B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT535_SequenceA_GeneralInformation_17B_Type_Pattern
class MT535_SequenceA_GeneralInformation_17B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceA_GeneralInformation_17B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 232, 1)
    _Documentation = None
MT535_SequenceA_GeneralInformation_17B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT535_SequenceA_GeneralInformation_17B_Type_Pattern._CF_pattern.addPattern(pattern='(:[A-Z0-9]{4}//[A-Z]{1})')
MT535_SequenceA_GeneralInformation_17B_Type_Pattern._InitializeFacetMap(MT535_SequenceA_GeneralInformation_17B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceA_GeneralInformation_17B_Type_Pattern', MT535_SequenceA_GeneralInformation_17B_Type_Pattern)
_module_typeBindings.MT535_SequenceA_GeneralInformation_17B_Type_Pattern = MT535_SequenceA_GeneralInformation_17B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_95P_Type_Pattern
class MT535_SequenceB_SubSafekeepingAccount_95P_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_95P_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 245, 1)
    _Documentation = None
MT535_SequenceB_SubSafekeepingAccount_95P_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT535_SequenceB_SubSafekeepingAccount_95P_Type_Pattern._CF_pattern.addPattern(pattern='(:[A-Z0-9]{4}//[A-Z0-9]{18}[0-9]{2})|(:[A-Z0-9]{4}//[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)')
MT535_SequenceB_SubSafekeepingAccount_95P_Type_Pattern._InitializeFacetMap(MT535_SequenceB_SubSafekeepingAccount_95P_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_95P_Type_Pattern', MT535_SequenceB_SubSafekeepingAccount_95P_Type_Pattern)
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_95P_Type_Pattern = MT535_SequenceB_SubSafekeepingAccount_95P_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_95R_Type_Pattern
class MT535_SequenceB_SubSafekeepingAccount_95R_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_95R_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 258, 1)
    _Documentation = None
MT535_SequenceB_SubSafekeepingAccount_95R_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT535_SequenceB_SubSafekeepingAccount_95R_Type_Pattern._CF_pattern.addPattern(pattern="(:[A-Z0-9]{4}/[A-Z0-9]{1,8}/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})")
MT535_SequenceB_SubSafekeepingAccount_95R_Type_Pattern._InitializeFacetMap(MT535_SequenceB_SubSafekeepingAccount_95R_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_95R_Type_Pattern', MT535_SequenceB_SubSafekeepingAccount_95R_Type_Pattern)
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_95R_Type_Pattern = MT535_SequenceB_SubSafekeepingAccount_95R_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_97A_Type_Pattern
class MT535_SequenceB_SubSafekeepingAccount_97A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_97A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 271, 1)
    _Documentation = None
MT535_SequenceB_SubSafekeepingAccount_97A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT535_SequenceB_SubSafekeepingAccount_97A_Type_Pattern._CF_pattern.addPattern(pattern="(:[A-Z0-9]{4}//([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35})")
MT535_SequenceB_SubSafekeepingAccount_97A_Type_Pattern._InitializeFacetMap(MT535_SequenceB_SubSafekeepingAccount_97A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_97A_Type_Pattern', MT535_SequenceB_SubSafekeepingAccount_97A_Type_Pattern)
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_97A_Type_Pattern = MT535_SequenceB_SubSafekeepingAccount_97A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_97B_Type_Pattern
class MT535_SequenceB_SubSafekeepingAccount_97B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_97B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 284, 1)
    _Documentation = None
MT535_SequenceB_SubSafekeepingAccount_97B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT535_SequenceB_SubSafekeepingAccount_97B_Type_Pattern._CF_pattern.addPattern(pattern="(:[A-Z0-9]{4}/([A-Z0-9]{1,8})?/[A-Z0-9]{4}/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35})")
MT535_SequenceB_SubSafekeepingAccount_97B_Type_Pattern._InitializeFacetMap(MT535_SequenceB_SubSafekeepingAccount_97B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_97B_Type_Pattern', MT535_SequenceB_SubSafekeepingAccount_97B_Type_Pattern)
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_97B_Type_Pattern = MT535_SequenceB_SubSafekeepingAccount_97B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_94B_Type_Pattern
class MT535_SequenceB_SubSafekeepingAccount_94B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_94B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 297, 1)
    _Documentation = None
MT535_SequenceB_SubSafekeepingAccount_94B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT535_SequenceB_SubSafekeepingAccount_94B_Type_Pattern._CF_pattern.addPattern(pattern="(:[A-Z0-9]{4}/([A-Z0-9]{1,8})?/[A-Z0-9]{4}(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,30})?)")
MT535_SequenceB_SubSafekeepingAccount_94B_Type_Pattern._InitializeFacetMap(MT535_SequenceB_SubSafekeepingAccount_94B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_94B_Type_Pattern', MT535_SequenceB_SubSafekeepingAccount_94B_Type_Pattern)
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_94B_Type_Pattern = MT535_SequenceB_SubSafekeepingAccount_94B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_94C_Type_Pattern
class MT535_SequenceB_SubSafekeepingAccount_94C_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_94C_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 310, 1)
    _Documentation = None
MT535_SequenceB_SubSafekeepingAccount_94C_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT535_SequenceB_SubSafekeepingAccount_94C_Type_Pattern._CF_pattern.addPattern(pattern='(:[A-Z0-9]{4}//[A-Z]{2})')
MT535_SequenceB_SubSafekeepingAccount_94C_Type_Pattern._InitializeFacetMap(MT535_SequenceB_SubSafekeepingAccount_94C_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_94C_Type_Pattern', MT535_SequenceB_SubSafekeepingAccount_94C_Type_Pattern)
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_94C_Type_Pattern = MT535_SequenceB_SubSafekeepingAccount_94C_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_94F_Type_Pattern
class MT535_SequenceB_SubSafekeepingAccount_94F_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_94F_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 323, 1)
    _Documentation = None
MT535_SequenceB_SubSafekeepingAccount_94F_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT535_SequenceB_SubSafekeepingAccount_94F_Type_Pattern._CF_pattern.addPattern(pattern='(:[A-Z0-9]{4}//[A-Z0-9]{4}/[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)|(:[A-Z0-9]{4}//[A-Z0-9]{18}[0-9]{2})')
MT535_SequenceB_SubSafekeepingAccount_94F_Type_Pattern._InitializeFacetMap(MT535_SequenceB_SubSafekeepingAccount_94F_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_94F_Type_Pattern', MT535_SequenceB_SubSafekeepingAccount_94F_Type_Pattern)
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_94F_Type_Pattern = MT535_SequenceB_SubSafekeepingAccount_94F_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_17B_Type_Pattern
class MT535_SequenceB_SubSafekeepingAccount_17B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_17B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 336, 1)
    _Documentation = None
MT535_SequenceB_SubSafekeepingAccount_17B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT535_SequenceB_SubSafekeepingAccount_17B_Type_Pattern._CF_pattern.addPattern(pattern='(:[A-Z0-9]{4}//[A-Z]{1})')
MT535_SequenceB_SubSafekeepingAccount_17B_Type_Pattern._InitializeFacetMap(MT535_SequenceB_SubSafekeepingAccount_17B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_17B_Type_Pattern', MT535_SequenceB_SubSafekeepingAccount_17B_Type_Pattern)
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_17B_Type_Pattern = MT535_SequenceB_SubSafekeepingAccount_17B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_35B_Type_Pattern
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_35B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_35B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 349, 1)
    _Documentation = None
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_35B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_35B_Type_Pattern._CF_pattern.addPattern(pattern="((ISIN {1}[A-Z0-9]{12})?(\\n(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})?)")
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_35B_Type_Pattern._InitializeFacetMap(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_35B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_35B_Type_Pattern', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_35B_Type_Pattern)
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_35B_Type_Pattern = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_35B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_94B_Type_Pattern
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_94B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_94B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 362, 1)
    _Documentation = None
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_94B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_94B_Type_Pattern._CF_pattern.addPattern(pattern="(:[A-Z0-9]{4}/([A-Z0-9]{1,8})?/[A-Z0-9]{4}(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,30})?)")
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_94B_Type_Pattern._InitializeFacetMap(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_94B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_94B_Type_Pattern', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_94B_Type_Pattern)
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_94B_Type_Pattern = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_94B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_94D_Type_Pattern
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_94D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_94D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 375, 1)
    _Documentation = None
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_94D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_94D_Type_Pattern._CF_pattern.addPattern(pattern="(:[A-Z0-9]{4}//([A-Z]{2})?/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35})")
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_94D_Type_Pattern._InitializeFacetMap(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_94D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_94D_Type_Pattern', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_94D_Type_Pattern)
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_94D_Type_Pattern = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_94D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_22F_Type_Pattern
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_22F_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_22F_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 388, 1)
    _Documentation = None
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_22F_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_22F_Type_Pattern._CF_pattern.addPattern(pattern='(:[A-Z0-9]{4}/([A-Z0-9]{1,8})?/[A-Z0-9]{4})')
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_22F_Type_Pattern._InitializeFacetMap(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_22F_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_22F_Type_Pattern', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_22F_Type_Pattern)
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_22F_Type_Pattern = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_22F_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_12A_Type_Pattern
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_12A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_12A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 401, 1)
    _Documentation = None
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_12A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_12A_Type_Pattern._CF_pattern.addPattern(pattern="(:[A-Z0-9]{4}/([A-Z0-9]{1,8})?/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,30})")
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_12A_Type_Pattern._InitializeFacetMap(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_12A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_12A_Type_Pattern', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_12A_Type_Pattern)
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_12A_Type_Pattern = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_12A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_12B_Type_Pattern
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_12B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_12B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 414, 1)
    _Documentation = None
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_12B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_12B_Type_Pattern._CF_pattern.addPattern(pattern='(:[A-Z0-9]{4}/([A-Z0-9]{1,8})?/[A-Z0-9]{4})')
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_12B_Type_Pattern._InitializeFacetMap(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_12B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_12B_Type_Pattern', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_12B_Type_Pattern)
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_12B_Type_Pattern = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_12B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_12C_Type_Pattern
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_12C_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_12C_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 427, 1)
    _Documentation = None
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_12C_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_12C_Type_Pattern._CF_pattern.addPattern(pattern='(:[A-Z0-9]{4}//[A-Z0-9]{6})')
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_12C_Type_Pattern._InitializeFacetMap(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_12C_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_12C_Type_Pattern', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_12C_Type_Pattern)
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_12C_Type_Pattern = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_12C_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_11A_Type_Pattern
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_11A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_11A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 440, 1)
    _Documentation = None
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_11A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_11A_Type_Pattern._CF_pattern.addPattern(pattern='(:[A-Z0-9]{4}//[A-Z]{3})')
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_11A_Type_Pattern._InitializeFacetMap(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_11A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_11A_Type_Pattern', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_11A_Type_Pattern)
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_11A_Type_Pattern = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_11A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_98A_Type_Pattern
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_98A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_98A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 453, 1)
    _Documentation = None
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_98A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_98A_Type_Pattern._CF_pattern.addPattern(pattern='(:[A-Z0-9]{4}//[0-9]{8})')
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_98A_Type_Pattern._InitializeFacetMap(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_98A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_98A_Type_Pattern', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_98A_Type_Pattern)
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_98A_Type_Pattern = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_98A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_92A_Type_Pattern
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_92A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_92A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 466, 1)
    _Documentation = None
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_92A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_92A_Type_Pattern._CF_pattern.addPattern(pattern='(:[A-Z0-9]{4}//(N)?[0-9,(?0-9)]{1,15})')
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_92A_Type_Pattern._InitializeFacetMap(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_92A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_92A_Type_Pattern', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_92A_Type_Pattern)
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_92A_Type_Pattern = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_92A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_13A_Type_Pattern
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_13A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_13A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 479, 1)
    _Documentation = None
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_13A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_13A_Type_Pattern._CF_pattern.addPattern(pattern='(:[A-Z0-9]{4}//[A-Z0-9]{3})')
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_13A_Type_Pattern._InitializeFacetMap(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_13A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_13A_Type_Pattern', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_13A_Type_Pattern)
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_13A_Type_Pattern = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_13A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_13B_Type_Pattern
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_13B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_13B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 492, 1)
    _Documentation = None
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_13B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_13B_Type_Pattern._CF_pattern.addPattern(pattern="(:[A-Z0-9]{4}/([A-Z0-9]{1,8})?/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,30})")
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_13B_Type_Pattern._InitializeFacetMap(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_13B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_13B_Type_Pattern', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_13B_Type_Pattern)
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_13B_Type_Pattern = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_13B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_13K_Type_Pattern
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_13K_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_13K_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 505, 1)
    _Documentation = None
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_13K_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_13K_Type_Pattern._CF_pattern.addPattern(pattern='(:[A-Z0-9]{4}//[A-Z0-9]{3}/[0-9,(?0-9)]{1,15})')
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_13K_Type_Pattern._InitializeFacetMap(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_13K_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_13K_Type_Pattern', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_13K_Type_Pattern)
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_13K_Type_Pattern = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_13K_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_17B_Type_Pattern
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_17B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_17B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 518, 1)
    _Documentation = None
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_17B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_17B_Type_Pattern._CF_pattern.addPattern(pattern='(:[A-Z0-9]{4}//[A-Z]{1})')
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_17B_Type_Pattern._InitializeFacetMap(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_17B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_17B_Type_Pattern', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_17B_Type_Pattern)
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_17B_Type_Pattern = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_17B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_90A_Type_Pattern
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_90A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_90A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 531, 1)
    _Documentation = None
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_90A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_90A_Type_Pattern._CF_pattern.addPattern(pattern='(:[A-Z0-9]{4}//[A-Z0-9]{4}/[0-9,(?0-9)]{1,15})')
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_90A_Type_Pattern._InitializeFacetMap(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_90A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_90A_Type_Pattern', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_90A_Type_Pattern)
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_90A_Type_Pattern = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_90A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_90B_Type_Pattern
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_90B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_90B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 544, 1)
    _Documentation = None
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_90B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_90B_Type_Pattern._CF_pattern.addPattern(pattern='(:[A-Z0-9]{4}//[A-Z0-9]{4}/[A-Z]{3}[0-9,(?0-9)]{1,15})')
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_90B_Type_Pattern._InitializeFacetMap(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_90B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_90B_Type_Pattern', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_90B_Type_Pattern)
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_90B_Type_Pattern = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_90B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_36B_Type_Pattern
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_36B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_36B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 557, 1)
    _Documentation = None
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_36B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_36B_Type_Pattern._CF_pattern.addPattern(pattern='(:[A-Z0-9]{4}//[A-Z0-9]{4}/[0-9,(?0-9)]{1,15})')
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_36B_Type_Pattern._InitializeFacetMap(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_36B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_36B_Type_Pattern', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_36B_Type_Pattern)
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_36B_Type_Pattern = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_36B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_35B_Type_Pattern
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_35B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_35B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 570, 1)
    _Documentation = None
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_35B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_35B_Type_Pattern._CF_pattern.addPattern(pattern="((ISIN {1}[A-Z0-9]{12})?((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})?)")
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_35B_Type_Pattern._InitializeFacetMap(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_35B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_35B_Type_Pattern', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_35B_Type_Pattern)
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_35B_Type_Pattern = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_35B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_70E_Type_Pattern
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_70E_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_70E_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 583, 1)
    _Documentation = None
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_70E_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_70E_Type_Pattern._CF_pattern.addPattern(pattern="(:[A-Z0-9]{4}//(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,10})")
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_70E_Type_Pattern._InitializeFacetMap(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_70E_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_70E_Type_Pattern', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_70E_Type_Pattern)
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_70E_Type_Pattern = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_70E_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_22H_Type_Pattern
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_22H_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_22H_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 596, 1)
    _Documentation = None
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_22H_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_22H_Type_Pattern._CF_pattern.addPattern(pattern='(:[A-Z0-9]{4}//[A-Z0-9]{4})')
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_22H_Type_Pattern._InitializeFacetMap(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_22H_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_22H_Type_Pattern', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_22H_Type_Pattern)
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_22H_Type_Pattern = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_22H_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_90A_Type_Pattern
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_90A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_90A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 609, 1)
    _Documentation = None
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_90A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_90A_Type_Pattern._CF_pattern.addPattern(pattern='(:[A-Z0-9]{4}//[A-Z0-9]{4}/(N)?[0-9,(?0-9)]{1,15})')
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_90A_Type_Pattern._InitializeFacetMap(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_90A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_90A_Type_Pattern', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_90A_Type_Pattern)
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_90A_Type_Pattern = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_90A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_90B_Type_Pattern
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_90B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_90B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 622, 1)
    _Documentation = None
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_90B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_90B_Type_Pattern._CF_pattern.addPattern(pattern='(:[A-Z0-9]{4}//[A-Z0-9]{4}/[A-Z]{3}[0-9,(?0-9)]{1,15})')
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_90B_Type_Pattern._InitializeFacetMap(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_90B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_90B_Type_Pattern', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_90B_Type_Pattern)
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_90B_Type_Pattern = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_90B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_90E_Type_Pattern
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_90E_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_90E_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 635, 1)
    _Documentation = None
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_90E_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_90E_Type_Pattern._CF_pattern.addPattern(pattern='(:[A-Z0-9]{4}//[A-Z0-9]{4})')
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_90E_Type_Pattern._InitializeFacetMap(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_90E_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_90E_Type_Pattern', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_90E_Type_Pattern)
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_90E_Type_Pattern = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_90E_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_94B_Type_Pattern
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_94B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_94B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 648, 1)
    _Documentation = None
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_94B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_94B_Type_Pattern._CF_pattern.addPattern(pattern="(:[A-Z0-9]{4}/([A-Z0-9]{1,8})?/[A-Z0-9]{4}(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,30})?)")
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_94B_Type_Pattern._InitializeFacetMap(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_94B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_94B_Type_Pattern', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_94B_Type_Pattern)
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_94B_Type_Pattern = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_94B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_98A_Type_Pattern
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_98A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_98A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 661, 1)
    _Documentation = None
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_98A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_98A_Type_Pattern._CF_pattern.addPattern(pattern='(:[A-Z0-9]{4}//[0-9]{8})')
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_98A_Type_Pattern._InitializeFacetMap(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_98A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_98A_Type_Pattern', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_98A_Type_Pattern)
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_98A_Type_Pattern = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_98A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_98C_Type_Pattern
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_98C_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_98C_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 674, 1)
    _Documentation = None
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_98C_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_98C_Type_Pattern._CF_pattern.addPattern(pattern='(:[A-Z0-9]{4}//[0-9]{8}[0-9]{6})')
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_98C_Type_Pattern._InitializeFacetMap(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_98C_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_98C_Type_Pattern', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_98C_Type_Pattern)
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_98C_Type_Pattern = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_98C_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_93B_Type_Pattern
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_93B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_93B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 687, 1)
    _Documentation = None
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_93B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_93B_Type_Pattern._CF_pattern.addPattern(pattern='(:[A-Z0-9]{4}/([A-Z0-9]{1,8})?/[A-Z0-9]{4}/(N)?[0-9,(?0-9)]{1,15})')
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_93B_Type_Pattern._InitializeFacetMap(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_93B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_93B_Type_Pattern', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_93B_Type_Pattern)
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_93B_Type_Pattern = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_93B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_93B_Type_Pattern
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_93B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_93B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 700, 1)
    _Documentation = None
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_93B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_93B_Type_Pattern._CF_pattern.addPattern(pattern='(:[A-Z0-9]{4}/([A-Z0-9]{1,8})?/[A-Z0-9]{4}/(N)?[0-9,(?0-9)]{1,15})')
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_93B_Type_Pattern._InitializeFacetMap(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_93B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_93B_Type_Pattern', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_93B_Type_Pattern)
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_93B_Type_Pattern = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_93B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_93C_Type_Pattern
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_93C_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_93C_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 713, 1)
    _Documentation = None
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_93C_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_93C_Type_Pattern._CF_pattern.addPattern(pattern='(:[A-Z0-9]{4}//[A-Z0-9]{4}/[A-Z0-9]{4}/(N)?[0-9,(?0-9)]{1,15})')
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_93C_Type_Pattern._InitializeFacetMap(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_93C_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_93C_Type_Pattern', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_93C_Type_Pattern)
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_93C_Type_Pattern = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_93C_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_22F_Type_Pattern
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_22F_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_22F_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 726, 1)
    _Documentation = None
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_22F_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_22F_Type_Pattern._CF_pattern.addPattern(pattern='(:[A-Z0-9]{4}/([A-Z0-9]{1,8})?/[A-Z0-9]{4})')
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_22F_Type_Pattern._InitializeFacetMap(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_22F_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_22F_Type_Pattern', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_22F_Type_Pattern)
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_22F_Type_Pattern = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_22F_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_22H_Type_Pattern
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_22H_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_22H_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 739, 1)
    _Documentation = None
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_22H_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_22H_Type_Pattern._CF_pattern.addPattern(pattern='(:[A-Z0-9]{4}//[A-Z0-9]{4})')
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_22H_Type_Pattern._InitializeFacetMap(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_22H_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_22H_Type_Pattern', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_22H_Type_Pattern)
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_22H_Type_Pattern = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_22H_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_94B_Type_Pattern
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_94B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_94B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 752, 1)
    _Documentation = None
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_94B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_94B_Type_Pattern._CF_pattern.addPattern(pattern="(:[A-Z0-9]{4}/([A-Z0-9]{1,8})?/[A-Z0-9]{4}(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,30})?)")
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_94B_Type_Pattern._InitializeFacetMap(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_94B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_94B_Type_Pattern', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_94B_Type_Pattern)
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_94B_Type_Pattern = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_94B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_94C_Type_Pattern
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_94C_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_94C_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 765, 1)
    _Documentation = None
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_94C_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_94C_Type_Pattern._CF_pattern.addPattern(pattern='(:[A-Z0-9]{4}//[A-Z]{2})')
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_94C_Type_Pattern._InitializeFacetMap(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_94C_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_94C_Type_Pattern', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_94C_Type_Pattern)
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_94C_Type_Pattern = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_94C_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_94F_Type_Pattern
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_94F_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_94F_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 778, 1)
    _Documentation = None
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_94F_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_94F_Type_Pattern._CF_pattern.addPattern(pattern='(:[A-Z0-9]{4}//[A-Z0-9]{4}/[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)|(:[A-Z0-9]{4}//[A-Z0-9]{18}[0-9]{2})')
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_94F_Type_Pattern._InitializeFacetMap(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_94F_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_94F_Type_Pattern', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_94F_Type_Pattern)
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_94F_Type_Pattern = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_94F_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_90A_Type_Pattern
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_90A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_90A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 791, 1)
    _Documentation = None
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_90A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_90A_Type_Pattern._CF_pattern.addPattern(pattern='(:[A-Z0-9]{4}//[A-Z0-9]{4}/(N)?[0-9,(?0-9)]{1,15})')
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_90A_Type_Pattern._InitializeFacetMap(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_90A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_90A_Type_Pattern', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_90A_Type_Pattern)
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_90A_Type_Pattern = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_90A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_90B_Type_Pattern
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_90B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_90B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 804, 1)
    _Documentation = None
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_90B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_90B_Type_Pattern._CF_pattern.addPattern(pattern='(:[A-Z0-9]{4}//[A-Z0-9]{4}/[A-Z]{3}[0-9,(?0-9)]{1,15})')
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_90B_Type_Pattern._InitializeFacetMap(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_90B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_90B_Type_Pattern', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_90B_Type_Pattern)
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_90B_Type_Pattern = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_90B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_90E_Type_Pattern
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_90E_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_90E_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 817, 1)
    _Documentation = None
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_90E_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_90E_Type_Pattern._CF_pattern.addPattern(pattern='(:[A-Z0-9]{4}//[A-Z0-9]{4})')
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_90E_Type_Pattern._InitializeFacetMap(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_90E_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_90E_Type_Pattern', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_90E_Type_Pattern)
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_90E_Type_Pattern = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_90E_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_98A_Type_Pattern
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_98A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_98A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 830, 1)
    _Documentation = None
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_98A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_98A_Type_Pattern._CF_pattern.addPattern(pattern='(:[A-Z0-9]{4}//[0-9]{8})')
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_98A_Type_Pattern._InitializeFacetMap(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_98A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_98A_Type_Pattern', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_98A_Type_Pattern)
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_98A_Type_Pattern = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_98A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_98C_Type_Pattern
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_98C_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_98C_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 843, 1)
    _Documentation = None
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_98C_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_98C_Type_Pattern._CF_pattern.addPattern(pattern='(:[A-Z0-9]{4}//[0-9]{8}[0-9]{6})')
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_98C_Type_Pattern._InitializeFacetMap(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_98C_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_98C_Type_Pattern', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_98C_Type_Pattern)
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_98C_Type_Pattern = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_98C_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_99A_Type_Pattern
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_99A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_99A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 856, 1)
    _Documentation = None
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_99A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_99A_Type_Pattern._CF_pattern.addPattern(pattern='(:[A-Z0-9]{4}//(N)?[0-9]{3})')
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_99A_Type_Pattern._InitializeFacetMap(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_99A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_99A_Type_Pattern', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_99A_Type_Pattern)
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_99A_Type_Pattern = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_99A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_19A_Type_Pattern
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_19A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_19A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 869, 1)
    _Documentation = None
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_19A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_19A_Type_Pattern._CF_pattern.addPattern(pattern='(:[A-Z0-9]{4}//(N)?[A-Z]{3}[0-9,(?0-9)]{1,15})')
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_19A_Type_Pattern._InitializeFacetMap(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_19A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_19A_Type_Pattern', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_19A_Type_Pattern)
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_19A_Type_Pattern = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_19A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_92B_Type_Pattern
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_92B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_92B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 882, 1)
    _Documentation = None
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_92B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_92B_Type_Pattern._CF_pattern.addPattern(pattern='(:[A-Z0-9]{4}//[A-Z]{3}/[A-Z]{3}/[0-9,(?0-9)]{1,15})')
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_92B_Type_Pattern._InitializeFacetMap(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_92B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_92B_Type_Pattern', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_92B_Type_Pattern)
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_92B_Type_Pattern = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_92B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_70C_Type_Pattern
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_70C_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_70C_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 895, 1)
    _Documentation = None
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_70C_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_70C_Type_Pattern._CF_pattern.addPattern(pattern="(:[A-Z0-9]{4}//(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_70C_Type_Pattern._InitializeFacetMap(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_70C_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_70C_Type_Pattern', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_70C_Type_Pattern)
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_70C_Type_Pattern = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_70C_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_13B_Type_Pattern
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_13B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_13B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 908, 1)
    _Documentation = None
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_13B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_13B_Type_Pattern._CF_pattern.addPattern(pattern="(:[A-Z0-9]{4}/([A-Z0-9]{1,8})?/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,30})")
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_13B_Type_Pattern._InitializeFacetMap(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_13B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_13B_Type_Pattern', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_13B_Type_Pattern)
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_13B_Type_Pattern = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_13B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_93B_Type_Pattern
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_93B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_93B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 921, 1)
    _Documentation = None
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_93B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_93B_Type_Pattern._CF_pattern.addPattern(pattern='(:[A-Z0-9]{4}/([A-Z0-9]{1,8})?/[A-Z0-9]{4}/(N)?[0-9,(?0-9)]{1,15})')
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_93B_Type_Pattern._InitializeFacetMap(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_93B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_93B_Type_Pattern', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_93B_Type_Pattern)
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_93B_Type_Pattern = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_93B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_98A_Type_Pattern
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_98A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_98A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 934, 1)
    _Documentation = None
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_98A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_98A_Type_Pattern._CF_pattern.addPattern(pattern='(:[A-Z0-9]{4}//[0-9]{8})')
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_98A_Type_Pattern._InitializeFacetMap(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_98A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_98A_Type_Pattern', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_98A_Type_Pattern)
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_98A_Type_Pattern = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_98A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_98C_Type_Pattern
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_98C_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_98C_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 947, 1)
    _Documentation = None
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_98C_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_98C_Type_Pattern._CF_pattern.addPattern(pattern='(:[A-Z0-9]{4}//[0-9]{8}[0-9]{6})')
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_98C_Type_Pattern._InitializeFacetMap(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_98C_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_98C_Type_Pattern', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_98C_Type_Pattern)
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_98C_Type_Pattern = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_98C_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_98E_Type_Pattern
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_98E_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_98E_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 960, 1)
    _Documentation = None
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_98E_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_98E_Type_Pattern._CF_pattern.addPattern(pattern='(:[A-Z0-9]{4}//[0-9]{8}[0-9]{6}(,[0-9]{1,3})?(/(N)?[0-9]{2}([0-9]{2})?)?)')
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_98E_Type_Pattern._InitializeFacetMap(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_98E_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_98E_Type_Pattern', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_98E_Type_Pattern)
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_98E_Type_Pattern = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_98E_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_90A_Type_Pattern
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_90A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_90A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 973, 1)
    _Documentation = None
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_90A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_90A_Type_Pattern._CF_pattern.addPattern(pattern='(:[A-Z0-9]{4}//[A-Z0-9]{4}/(N)?[0-9,(?0-9)]{1,15})')
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_90A_Type_Pattern._InitializeFacetMap(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_90A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_90A_Type_Pattern', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_90A_Type_Pattern)
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_90A_Type_Pattern = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_90A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_90B_Type_Pattern
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_90B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_90B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 986, 1)
    _Documentation = None
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_90B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_90B_Type_Pattern._CF_pattern.addPattern(pattern='(:[A-Z0-9]{4}//[A-Z0-9]{4}/[A-Z]{3}[0-9,(?0-9)]{1,15})')
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_90B_Type_Pattern._InitializeFacetMap(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_90B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_90B_Type_Pattern', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_90B_Type_Pattern)
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_90B_Type_Pattern = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_90B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_22F_Type_Pattern
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_22F_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_22F_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 999, 1)
    _Documentation = None
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_22F_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_22F_Type_Pattern._CF_pattern.addPattern(pattern='(:[A-Z0-9]{4}/([A-Z0-9]{1,8})?/[A-Z0-9]{4})')
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_22F_Type_Pattern._InitializeFacetMap(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_22F_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_22F_Type_Pattern', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_22F_Type_Pattern)
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_22F_Type_Pattern = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_22F_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_19A_Type_Pattern
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_19A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_19A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1012, 1)
    _Documentation = None
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_19A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_19A_Type_Pattern._CF_pattern.addPattern(pattern='(:[A-Z0-9]{4}//(N)?[A-Z]{3}[0-9,(?0-9)]{1,15})')
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_19A_Type_Pattern._InitializeFacetMap(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_19A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_19A_Type_Pattern', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_19A_Type_Pattern)
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_19A_Type_Pattern = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_19A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_99A_Type_Pattern
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_99A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_99A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1025, 1)
    _Documentation = None
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_99A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_99A_Type_Pattern._CF_pattern.addPattern(pattern='(:[A-Z0-9]{4}//(N)?[0-9]{3})')
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_99A_Type_Pattern._InitializeFacetMap(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_99A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_99A_Type_Pattern', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_99A_Type_Pattern)
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_99A_Type_Pattern = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_99A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_19A_Type_Pattern
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_19A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_19A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1038, 1)
    _Documentation = None
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_19A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_19A_Type_Pattern._CF_pattern.addPattern(pattern='(:[A-Z0-9]{4}//(N)?[A-Z]{3}[0-9,(?0-9)]{1,15})')
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_19A_Type_Pattern._InitializeFacetMap(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_19A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_19A_Type_Pattern', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_19A_Type_Pattern)
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_19A_Type_Pattern = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_19A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_92B_Type_Pattern
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_92B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_92B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1051, 1)
    _Documentation = None
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_92B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_92B_Type_Pattern._CF_pattern.addPattern(pattern='(:[A-Z0-9]{4}//[A-Z]{3}/[A-Z]{3}/[0-9,(?0-9)]{1,15})')
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_92B_Type_Pattern._InitializeFacetMap(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_92B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_92B_Type_Pattern', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_92B_Type_Pattern)
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_92B_Type_Pattern = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_92B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_70E_Type_Pattern
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_70E_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_70E_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1064, 1)
    _Documentation = None
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_70E_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_70E_Type_Pattern._CF_pattern.addPattern(pattern="(:[A-Z0-9]{4}//(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,10})")
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_70E_Type_Pattern._InitializeFacetMap(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_70E_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_70E_Type_Pattern', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_70E_Type_Pattern)
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_70E_Type_Pattern = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_70E_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_13B_Type_Pattern
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_13B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_13B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1077, 1)
    _Documentation = None
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_13B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_13B_Type_Pattern._CF_pattern.addPattern(pattern="(:[A-Z0-9]{4}/([A-Z0-9]{1,8})?/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,30})")
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_13B_Type_Pattern._InitializeFacetMap(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_13B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_13B_Type_Pattern', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_13B_Type_Pattern)
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_13B_Type_Pattern = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_13B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_93B_Type_Pattern
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_93B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_93B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1090, 1)
    _Documentation = None
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_93B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_93B_Type_Pattern._CF_pattern.addPattern(pattern='(:[A-Z0-9]{4}/([A-Z0-9]{1,8})?/[A-Z0-9]{4}/(N)?[0-9,(?0-9)]{1,15})')
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_93B_Type_Pattern._InitializeFacetMap(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_93B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_93B_Type_Pattern', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_93B_Type_Pattern)
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_93B_Type_Pattern = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_93B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_98A_Type_Pattern
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_98A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_98A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1103, 1)
    _Documentation = None
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_98A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_98A_Type_Pattern._CF_pattern.addPattern(pattern='(:[A-Z0-9]{4}//[0-9]{8})')
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_98A_Type_Pattern._InitializeFacetMap(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_98A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_98A_Type_Pattern', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_98A_Type_Pattern)
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_98A_Type_Pattern = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_98A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_98C_Type_Pattern
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_98C_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_98C_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1116, 1)
    _Documentation = None
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_98C_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_98C_Type_Pattern._CF_pattern.addPattern(pattern='(:[A-Z0-9]{4}//[0-9]{8}[0-9]{6})')
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_98C_Type_Pattern._InitializeFacetMap(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_98C_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_98C_Type_Pattern', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_98C_Type_Pattern)
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_98C_Type_Pattern = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_98C_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_98E_Type_Pattern
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_98E_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_98E_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1129, 1)
    _Documentation = None
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_98E_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_98E_Type_Pattern._CF_pattern.addPattern(pattern='(:[A-Z0-9]{4}//[0-9]{8}[0-9]{6}(,[0-9]{1,3})?(/(N)?[0-9]{2}([0-9]{2})?)?)')
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_98E_Type_Pattern._InitializeFacetMap(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_98E_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_98E_Type_Pattern', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_98E_Type_Pattern)
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_98E_Type_Pattern = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_98E_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_90A_Type_Pattern
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_90A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_90A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1142, 1)
    _Documentation = None
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_90A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_90A_Type_Pattern._CF_pattern.addPattern(pattern='(:[A-Z0-9]{4}//[A-Z0-9]{4}/[0-9,(?0-9)]{1,15})')
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_90A_Type_Pattern._InitializeFacetMap(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_90A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_90A_Type_Pattern', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_90A_Type_Pattern)
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_90A_Type_Pattern = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_90A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_90B_Type_Pattern
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_90B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_90B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1155, 1)
    _Documentation = None
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_90B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_90B_Type_Pattern._CF_pattern.addPattern(pattern='(:[A-Z0-9]{4}//[A-Z0-9]{4}/[A-Z]{3}[0-9,(?0-9)]{1,15})')
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_90B_Type_Pattern._InitializeFacetMap(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_90B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_90B_Type_Pattern', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_90B_Type_Pattern)
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_90B_Type_Pattern = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_90B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_22F_Type_Pattern
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_22F_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_22F_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1168, 1)
    _Documentation = None
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_22F_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_22F_Type_Pattern._CF_pattern.addPattern(pattern='(:[A-Z0-9]{4}/([A-Z0-9]{1,8})?/[A-Z0-9]{4})')
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_22F_Type_Pattern._InitializeFacetMap(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_22F_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_22F_Type_Pattern', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_22F_Type_Pattern)
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_22F_Type_Pattern = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_22F_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_19A_Type_Pattern
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_19A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_19A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1181, 1)
    _Documentation = None
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_19A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_19A_Type_Pattern._CF_pattern.addPattern(pattern='(:[A-Z0-9]{4}//(N)?[A-Z]{3}[0-9,(?0-9)]{1,15})')
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_19A_Type_Pattern._InitializeFacetMap(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_19A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_19A_Type_Pattern', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_19A_Type_Pattern)
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_19A_Type_Pattern = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_19A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT535_SequenceC_AdditionalInformation_95P_Type_Pattern
class MT535_SequenceC_AdditionalInformation_95P_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceC_AdditionalInformation_95P_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1194, 1)
    _Documentation = None
MT535_SequenceC_AdditionalInformation_95P_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT535_SequenceC_AdditionalInformation_95P_Type_Pattern._CF_pattern.addPattern(pattern='(:[A-Z0-9]{4}//[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)')
MT535_SequenceC_AdditionalInformation_95P_Type_Pattern._InitializeFacetMap(MT535_SequenceC_AdditionalInformation_95P_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceC_AdditionalInformation_95P_Type_Pattern', MT535_SequenceC_AdditionalInformation_95P_Type_Pattern)
_module_typeBindings.MT535_SequenceC_AdditionalInformation_95P_Type_Pattern = MT535_SequenceC_AdditionalInformation_95P_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT535_SequenceC_AdditionalInformation_95Q_Type_Pattern
class MT535_SequenceC_AdditionalInformation_95Q_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceC_AdditionalInformation_95Q_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1207, 1)
    _Documentation = None
MT535_SequenceC_AdditionalInformation_95Q_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT535_SequenceC_AdditionalInformation_95Q_Type_Pattern._CF_pattern.addPattern(pattern="(:[A-Z0-9]{4}//(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT535_SequenceC_AdditionalInformation_95Q_Type_Pattern._InitializeFacetMap(MT535_SequenceC_AdditionalInformation_95Q_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceC_AdditionalInformation_95Q_Type_Pattern', MT535_SequenceC_AdditionalInformation_95Q_Type_Pattern)
_module_typeBindings.MT535_SequenceC_AdditionalInformation_95Q_Type_Pattern = MT535_SequenceC_AdditionalInformation_95Q_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT535_SequenceC_AdditionalInformation_95R_Type_Pattern
class MT535_SequenceC_AdditionalInformation_95R_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceC_AdditionalInformation_95R_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1220, 1)
    _Documentation = None
MT535_SequenceC_AdditionalInformation_95R_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT535_SequenceC_AdditionalInformation_95R_Type_Pattern._CF_pattern.addPattern(pattern="(:[A-Z0-9]{4}/[A-Z0-9]{1,8}/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})")
MT535_SequenceC_AdditionalInformation_95R_Type_Pattern._InitializeFacetMap(MT535_SequenceC_AdditionalInformation_95R_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceC_AdditionalInformation_95R_Type_Pattern', MT535_SequenceC_AdditionalInformation_95R_Type_Pattern)
_module_typeBindings.MT535_SequenceC_AdditionalInformation_95R_Type_Pattern = MT535_SequenceC_AdditionalInformation_95R_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT535_SequenceC_AdditionalInformation_19A_Type_Pattern
class MT535_SequenceC_AdditionalInformation_19A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceC_AdditionalInformation_19A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1233, 1)
    _Documentation = None
MT535_SequenceC_AdditionalInformation_19A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT535_SequenceC_AdditionalInformation_19A_Type_Pattern._CF_pattern.addPattern(pattern='(:[A-Z0-9]{4}//(N)?[A-Z]{3}[0-9,(?0-9)]{1,15})')
MT535_SequenceC_AdditionalInformation_19A_Type_Pattern._InitializeFacetMap(MT535_SequenceC_AdditionalInformation_19A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceC_AdditionalInformation_19A_Type_Pattern', MT535_SequenceC_AdditionalInformation_19A_Type_Pattern)
_module_typeBindings.MT535_SequenceC_AdditionalInformation_19A_Type_Pattern = MT535_SequenceC_AdditionalInformation_19A_Type_Pattern

# Complex type {http://www.w3schools.com}MT535_SequenceA_GeneralInformation_13a_Type with content type SIMPLE
class MT535_SequenceA_GeneralInformation_13a_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT535_SequenceA_GeneralInformation_13a_Type with content type SIMPLE"""
    _TypeDefinition = pyxb.binding.datatypes.string
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceA_GeneralInformation_13a_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 16, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.string
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT535_SequenceA_GeneralInformation_13a_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='13a')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 19, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 19, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT535_SequenceA_GeneralInformation_13a_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 20, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 20, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT535_SequenceA_GeneralInformation_13a_Type = MT535_SequenceA_GeneralInformation_13a_Type
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceA_GeneralInformation_13a_Type', MT535_SequenceA_GeneralInformation_13a_Type)


# Complex type {http://www.w3schools.com}MT535_SequenceA_GeneralInformation with content type ELEMENT_ONLY
class MT535_SequenceA_GeneralInformation (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT535_SequenceA_GeneralInformation with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceA_GeneralInformation')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1246, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}PageNumber uses Python identifier PageNumber
    __PageNumber = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PageNumber'), 'PageNumber', '__httpwww_w3schools_com_MT535_SequenceA_GeneralInformation_httpwww_w3schools_comPageNumber', False, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1248, 3), )

    
    PageNumber = property(__PageNumber.value, __PageNumber.set, None, None)

    
    # Element {http://www.w3schools.com}StatementNumber uses Python identifier StatementNumber
    __StatementNumber = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'StatementNumber'), 'StatementNumber', '__httpwww_w3schools_com_MT535_SequenceA_GeneralInformation_httpwww_w3schools_comStatementNumber', False, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1249, 3), )

    
    StatementNumber = property(__StatementNumber.value, __StatementNumber.set, None, None)

    
    # Element {http://www.w3schools.com}StatementNumber_A uses Python identifier StatementNumber_A
    __StatementNumber_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'StatementNumber_A'), 'StatementNumber_A', '__httpwww_w3schools_com_MT535_SequenceA_GeneralInformation_httpwww_w3schools_comStatementNumber_A', False, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1251, 4), )

    
    StatementNumber_A = property(__StatementNumber_A.value, __StatementNumber_A.set, None, None)

    
    # Element {http://www.w3schools.com}StatementNumber_J uses Python identifier StatementNumber_J
    __StatementNumber_J = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'StatementNumber_J'), 'StatementNumber_J', '__httpwww_w3schools_com_MT535_SequenceA_GeneralInformation_httpwww_w3schools_comStatementNumber_J', False, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1252, 4), )

    
    StatementNumber_J = property(__StatementNumber_J.value, __StatementNumber_J.set, None, None)

    
    # Element {http://www.w3schools.com}SendersMessageReference uses Python identifier SendersMessageReference
    __SendersMessageReference = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SendersMessageReference'), 'SendersMessageReference', '__httpwww_w3schools_com_MT535_SequenceA_GeneralInformation_httpwww_w3schools_comSendersMessageReference', False, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1254, 3), )

    
    SendersMessageReference = property(__SendersMessageReference.value, __SendersMessageReference.set, None, None)

    
    # Element {http://www.w3schools.com}FunctionOfMessage uses Python identifier FunctionOfMessage
    __FunctionOfMessage = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'FunctionOfMessage'), 'FunctionOfMessage', '__httpwww_w3schools_com_MT535_SequenceA_GeneralInformation_httpwww_w3schools_comFunctionOfMessage', False, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1255, 3), )

    
    FunctionOfMessage = property(__FunctionOfMessage.value, __FunctionOfMessage.set, None, None)

    
    # Element {http://www.w3schools.com}DateTime_A uses Python identifier DateTime_A
    __DateTime_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'DateTime_A'), 'DateTime_A', '__httpwww_w3schools_com_MT535_SequenceA_GeneralInformation_httpwww_w3schools_comDateTime_A', True, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1257, 4), )

    
    DateTime_A = property(__DateTime_A.value, __DateTime_A.set, None, None)

    
    # Element {http://www.w3schools.com}DateTime_C uses Python identifier DateTime_C
    __DateTime_C = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'DateTime_C'), 'DateTime_C', '__httpwww_w3schools_com_MT535_SequenceA_GeneralInformation_httpwww_w3schools_comDateTime_C', True, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1258, 4), )

    
    DateTime_C = property(__DateTime_C.value, __DateTime_C.set, None, None)

    
    # Element {http://www.w3schools.com}DateTime_E uses Python identifier DateTime_E
    __DateTime_E = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'DateTime_E'), 'DateTime_E', '__httpwww_w3schools_com_MT535_SequenceA_GeneralInformation_httpwww_w3schools_comDateTime_E', True, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1259, 4), )

    
    DateTime_E = property(__DateTime_E.value, __DateTime_E.set, None, None)

    
    # Element {http://www.w3schools.com}Indicator uses Python identifier Indicator
    __Indicator = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Indicator'), 'Indicator', '__httpwww_w3schools_com_MT535_SequenceA_GeneralInformation_httpwww_w3schools_comIndicator', True, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1261, 3), )

    
    Indicator = property(__Indicator.value, __Indicator.set, None, None)

    
    # Element {http://www.w3schools.com}SubsequenceA1_Linkages uses Python identifier SubsequenceA1_Linkages
    __SubsequenceA1_Linkages = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SubsequenceA1_Linkages'), 'SubsequenceA1_Linkages', '__httpwww_w3schools_com_MT535_SequenceA_GeneralInformation_httpwww_w3schools_comSubsequenceA1_Linkages', True, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1262, 3), )

    
    SubsequenceA1_Linkages = property(__SubsequenceA1_Linkages.value, __SubsequenceA1_Linkages.set, None, None)

    
    # Element {http://www.w3schools.com}Party_L uses Python identifier Party_L
    __Party_L = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Party_L'), 'Party_L', '__httpwww_w3schools_com_MT535_SequenceA_GeneralInformation_httpwww_w3schools_comParty_L', True, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1264, 4), )

    
    Party_L = property(__Party_L.value, __Party_L.set, None, None)

    
    # Element {http://www.w3schools.com}Party_P uses Python identifier Party_P
    __Party_P = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Party_P'), 'Party_P', '__httpwww_w3schools_com_MT535_SequenceA_GeneralInformation_httpwww_w3schools_comParty_P', True, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1265, 4), )

    
    Party_P = property(__Party_P.value, __Party_P.set, None, None)

    
    # Element {http://www.w3schools.com}Party_R uses Python identifier Party_R
    __Party_R = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Party_R'), 'Party_R', '__httpwww_w3schools_com_MT535_SequenceA_GeneralInformation_httpwww_w3schools_comParty_R', True, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1266, 4), )

    
    Party_R = property(__Party_R.value, __Party_R.set, None, None)

    
    # Element {http://www.w3schools.com}SafekeepingAccount_A uses Python identifier SafekeepingAccount_A
    __SafekeepingAccount_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SafekeepingAccount_A'), 'SafekeepingAccount_A', '__httpwww_w3schools_com_MT535_SequenceA_GeneralInformation_httpwww_w3schools_comSafekeepingAccount_A', False, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1269, 4), )

    
    SafekeepingAccount_A = property(__SafekeepingAccount_A.value, __SafekeepingAccount_A.set, None, None)

    
    # Element {http://www.w3schools.com}SafekeepingAccount_B uses Python identifier SafekeepingAccount_B
    __SafekeepingAccount_B = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SafekeepingAccount_B'), 'SafekeepingAccount_B', '__httpwww_w3schools_com_MT535_SequenceA_GeneralInformation_httpwww_w3schools_comSafekeepingAccount_B', False, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1270, 4), )

    
    SafekeepingAccount_B = property(__SafekeepingAccount_B.value, __SafekeepingAccount_B.set, None, None)

    
    # Element {http://www.w3schools.com}Flag uses Python identifier Flag
    __Flag = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Flag'), 'Flag', '__httpwww_w3schools_com_MT535_SequenceA_GeneralInformation_httpwww_w3schools_comFlag', True, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1272, 3), )

    
    Flag = property(__Flag.value, __Flag.set, None, None)

    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT535_SequenceA_GeneralInformation_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='16R')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1274, 2)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1274, 2)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT535_SequenceA_GeneralInformation_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1275, 2)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1275, 2)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    
    # Attribute formatTag uses Python identifier formatTag
    __formatTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'formatTag'), 'formatTag', '__httpwww_w3schools_com_MT535_SequenceA_GeneralInformation_formatTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='GENL')
    __formatTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1276, 2)
    __formatTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1276, 2)
    
    formatTag = property(__formatTag.value, __formatTag.set, None, None)

    _ElementMap.update({
        __PageNumber.name() : __PageNumber,
        __StatementNumber.name() : __StatementNumber,
        __StatementNumber_A.name() : __StatementNumber_A,
        __StatementNumber_J.name() : __StatementNumber_J,
        __SendersMessageReference.name() : __SendersMessageReference,
        __FunctionOfMessage.name() : __FunctionOfMessage,
        __DateTime_A.name() : __DateTime_A,
        __DateTime_C.name() : __DateTime_C,
        __DateTime_E.name() : __DateTime_E,
        __Indicator.name() : __Indicator,
        __SubsequenceA1_Linkages.name() : __SubsequenceA1_Linkages,
        __Party_L.name() : __Party_L,
        __Party_P.name() : __Party_P,
        __Party_R.name() : __Party_R,
        __SafekeepingAccount_A.name() : __SafekeepingAccount_A,
        __SafekeepingAccount_B.name() : __SafekeepingAccount_B,
        __Flag.name() : __Flag
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory,
        __formatTag.name() : __formatTag
    })
_module_typeBindings.MT535_SequenceA_GeneralInformation = MT535_SequenceA_GeneralInformation
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceA_GeneralInformation', MT535_SequenceA_GeneralInformation)


# Complex type {http://www.w3schools.com}MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages with content type ELEMENT_ONLY
class MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1278, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}LinkedMessage_A uses Python identifier LinkedMessage_A
    __LinkedMessage_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'LinkedMessage_A'), 'LinkedMessage_A', '__httpwww_w3schools_com_MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages_httpwww_w3schools_comLinkedMessage_A', False, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1281, 4), )

    
    LinkedMessage_A = property(__LinkedMessage_A.value, __LinkedMessage_A.set, None, None)

    
    # Element {http://www.w3schools.com}LinkedMessage_B uses Python identifier LinkedMessage_B
    __LinkedMessage_B = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'LinkedMessage_B'), 'LinkedMessage_B', '__httpwww_w3schools_com_MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages_httpwww_w3schools_comLinkedMessage_B', False, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1282, 4), )

    
    LinkedMessage_B = property(__LinkedMessage_B.value, __LinkedMessage_B.set, None, None)

    
    # Element {http://www.w3schools.com}Reference uses Python identifier Reference
    __Reference = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Reference'), 'Reference', '__httpwww_w3schools_com_MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages_httpwww_w3schools_comReference', False, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1284, 3), )

    
    Reference = property(__Reference.value, __Reference.set, None, None)

    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='16R')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1286, 2)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1286, 2)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1287, 2)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1287, 2)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    
    # Attribute formatTag uses Python identifier formatTag
    __formatTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'formatTag'), 'formatTag', '__httpwww_w3schools_com_MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages_formatTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='LINK')
    __formatTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1288, 2)
    __formatTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1288, 2)
    
    formatTag = property(__formatTag.value, __formatTag.set, None, None)

    _ElementMap.update({
        __LinkedMessage_A.name() : __LinkedMessage_A,
        __LinkedMessage_B.name() : __LinkedMessage_B,
        __Reference.name() : __Reference
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory,
        __formatTag.name() : __formatTag
    })
_module_typeBindings.MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages = MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages', MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages)


# Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount with content type ELEMENT_ONLY
class MT535_SequenceB_SubSafekeepingAccount (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1290, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}Party_L uses Python identifier Party_L
    __Party_L = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Party_L'), 'Party_L', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_httpwww_w3schools_comParty_L', True, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1293, 4), )

    
    Party_L = property(__Party_L.value, __Party_L.set, None, None)

    
    # Element {http://www.w3schools.com}Party_P uses Python identifier Party_P
    __Party_P = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Party_P'), 'Party_P', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_httpwww_w3schools_comParty_P', True, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1294, 4), )

    
    Party_P = property(__Party_P.value, __Party_P.set, None, None)

    
    # Element {http://www.w3schools.com}Party_R uses Python identifier Party_R
    __Party_R = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Party_R'), 'Party_R', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_httpwww_w3schools_comParty_R', True, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1295, 4), )

    
    Party_R = property(__Party_R.value, __Party_R.set, None, None)

    
    # Element {http://www.w3schools.com}SafekeepingAccount_A uses Python identifier SafekeepingAccount_A
    __SafekeepingAccount_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SafekeepingAccount_A'), 'SafekeepingAccount_A', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_httpwww_w3schools_comSafekeepingAccount_A', False, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1298, 4), )

    
    SafekeepingAccount_A = property(__SafekeepingAccount_A.value, __SafekeepingAccount_A.set, None, None)

    
    # Element {http://www.w3schools.com}SafekeepingAccount_B uses Python identifier SafekeepingAccount_B
    __SafekeepingAccount_B = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SafekeepingAccount_B'), 'SafekeepingAccount_B', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_httpwww_w3schools_comSafekeepingAccount_B', False, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1299, 4), )

    
    SafekeepingAccount_B = property(__SafekeepingAccount_B.value, __SafekeepingAccount_B.set, None, None)

    
    # Element {http://www.w3schools.com}PlaceOfSafekeeping_B uses Python identifier PlaceOfSafekeeping_B
    __PlaceOfSafekeeping_B = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PlaceOfSafekeeping_B'), 'PlaceOfSafekeeping_B', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_httpwww_w3schools_comPlaceOfSafekeeping_B', True, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1302, 4), )

    
    PlaceOfSafekeeping_B = property(__PlaceOfSafekeeping_B.value, __PlaceOfSafekeeping_B.set, None, None)

    
    # Element {http://www.w3schools.com}PlaceOfSafekeeping_C uses Python identifier PlaceOfSafekeeping_C
    __PlaceOfSafekeeping_C = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PlaceOfSafekeeping_C'), 'PlaceOfSafekeeping_C', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_httpwww_w3schools_comPlaceOfSafekeeping_C', True, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1303, 4), )

    
    PlaceOfSafekeeping_C = property(__PlaceOfSafekeeping_C.value, __PlaceOfSafekeeping_C.set, None, None)

    
    # Element {http://www.w3schools.com}PlaceOfSafekeeping_F uses Python identifier PlaceOfSafekeeping_F
    __PlaceOfSafekeeping_F = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PlaceOfSafekeeping_F'), 'PlaceOfSafekeeping_F', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_httpwww_w3schools_comPlaceOfSafekeeping_F', True, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1304, 4), )

    
    PlaceOfSafekeeping_F = property(__PlaceOfSafekeeping_F.value, __PlaceOfSafekeeping_F.set, None, None)

    
    # Element {http://www.w3schools.com}PlaceOfSafekeeping_L uses Python identifier PlaceOfSafekeeping_L
    __PlaceOfSafekeeping_L = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PlaceOfSafekeeping_L'), 'PlaceOfSafekeeping_L', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_httpwww_w3schools_comPlaceOfSafekeeping_L', True, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1305, 4), )

    
    PlaceOfSafekeeping_L = property(__PlaceOfSafekeeping_L.value, __PlaceOfSafekeeping_L.set, None, None)

    
    # Element {http://www.w3schools.com}ActivityFlag uses Python identifier ActivityFlag
    __ActivityFlag = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ActivityFlag'), 'ActivityFlag', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_httpwww_w3schools_comActivityFlag', False, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1307, 3), )

    
    ActivityFlag = property(__ActivityFlag.value, __ActivityFlag.set, None, None)

    
    # Element {http://www.w3schools.com}SubsequenceB1_FinancialInstrument uses Python identifier SubsequenceB1_FinancialInstrument
    __SubsequenceB1_FinancialInstrument = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SubsequenceB1_FinancialInstrument'), 'SubsequenceB1_FinancialInstrument', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_httpwww_w3schools_comSubsequenceB1_FinancialInstrument', True, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1308, 3), )

    
    SubsequenceB1_FinancialInstrument = property(__SubsequenceB1_FinancialInstrument.value, __SubsequenceB1_FinancialInstrument.set, None, None)

    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='16R')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1310, 2)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1310, 2)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1311, 2)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1311, 2)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    
    # Attribute formatTag uses Python identifier formatTag
    __formatTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'formatTag'), 'formatTag', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_formatTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='SUBSAFE')
    __formatTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1312, 2)
    __formatTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1312, 2)
    
    formatTag = property(__formatTag.value, __formatTag.set, None, None)

    _ElementMap.update({
        __Party_L.name() : __Party_L,
        __Party_P.name() : __Party_P,
        __Party_R.name() : __Party_R,
        __SafekeepingAccount_A.name() : __SafekeepingAccount_A,
        __SafekeepingAccount_B.name() : __SafekeepingAccount_B,
        __PlaceOfSafekeeping_B.name() : __PlaceOfSafekeeping_B,
        __PlaceOfSafekeeping_C.name() : __PlaceOfSafekeeping_C,
        __PlaceOfSafekeeping_F.name() : __PlaceOfSafekeeping_F,
        __PlaceOfSafekeeping_L.name() : __PlaceOfSafekeeping_L,
        __ActivityFlag.name() : __ActivityFlag,
        __SubsequenceB1_FinancialInstrument.name() : __SubsequenceB1_FinancialInstrument
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory,
        __formatTag.name() : __formatTag
    })
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount = MT535_SequenceB_SubSafekeepingAccount
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount', MT535_SequenceB_SubSafekeepingAccount)


# Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument with content type ELEMENT_ONLY
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1314, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}IdentificationOfFinancialInstrument uses Python identifier IdentificationOfFinancialInstrument
    __IdentificationOfFinancialInstrument = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'IdentificationOfFinancialInstrument'), 'IdentificationOfFinancialInstrument', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_httpwww_w3schools_comIdentificationOfFinancialInstrument', False, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1316, 3), )

    
    IdentificationOfFinancialInstrument = property(__IdentificationOfFinancialInstrument.value, __IdentificationOfFinancialInstrument.set, None, None)

    
    # Element {http://www.w3schools.com}SubsequenceB1a_FinancialInstrumentAttributes uses Python identifier SubsequenceB1a_FinancialInstrumentAttributes
    __SubsequenceB1a_FinancialInstrumentAttributes = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SubsequenceB1a_FinancialInstrumentAttributes'), 'SubsequenceB1a_FinancialInstrumentAttributes', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_httpwww_w3schools_comSubsequenceB1a_FinancialInstrumentAttributes', False, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1317, 3), )

    
    SubsequenceB1a_FinancialInstrumentAttributes = property(__SubsequenceB1a_FinancialInstrumentAttributes.value, __SubsequenceB1a_FinancialInstrumentAttributes.set, None, None)

    
    # Element {http://www.w3schools.com}CorporateActionOptionCodeIndicator uses Python identifier CorporateActionOptionCodeIndicator
    __CorporateActionOptionCodeIndicator = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'CorporateActionOptionCodeIndicator'), 'CorporateActionOptionCodeIndicator', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_httpwww_w3schools_comCorporateActionOptionCodeIndicator', False, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1318, 3), )

    
    CorporateActionOptionCodeIndicator = property(__CorporateActionOptionCodeIndicator.value, __CorporateActionOptionCodeIndicator.set, None, None)

    
    # Element {http://www.w3schools.com}Price_A uses Python identifier Price_A
    __Price_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Price_A'), 'Price_A', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_httpwww_w3schools_comPrice_A', False, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1320, 4), )

    
    Price_A = property(__Price_A.value, __Price_A.set, None, None)

    
    # Element {http://www.w3schools.com}Price_B uses Python identifier Price_B
    __Price_B = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Price_B'), 'Price_B', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_httpwww_w3schools_comPrice_B', False, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1321, 4), )

    
    Price_B = property(__Price_B.value, __Price_B.set, None, None)

    
    # Element {http://www.w3schools.com}Price_E uses Python identifier Price_E
    __Price_E = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Price_E'), 'Price_E', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_httpwww_w3schools_comPrice_E', False, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1322, 4), )

    
    Price_E = property(__Price_E.value, __Price_E.set, None, None)

    
    # Element {http://www.w3schools.com}SourceOfPrice uses Python identifier SourceOfPrice
    __SourceOfPrice = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SourceOfPrice'), 'SourceOfPrice', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_httpwww_w3schools_comSourceOfPrice', False, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1324, 3), )

    
    SourceOfPrice = property(__SourceOfPrice.value, __SourceOfPrice.set, None, None)

    
    # Element {http://www.w3schools.com}PriceQuotationDateTime_A uses Python identifier PriceQuotationDateTime_A
    __PriceQuotationDateTime_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PriceQuotationDateTime_A'), 'PriceQuotationDateTime_A', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_httpwww_w3schools_comPriceQuotationDateTime_A', False, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1326, 4), )

    
    PriceQuotationDateTime_A = property(__PriceQuotationDateTime_A.value, __PriceQuotationDateTime_A.set, None, None)

    
    # Element {http://www.w3schools.com}PriceQuotationDateTime_C uses Python identifier PriceQuotationDateTime_C
    __PriceQuotationDateTime_C = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PriceQuotationDateTime_C'), 'PriceQuotationDateTime_C', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_httpwww_w3schools_comPriceQuotationDateTime_C', False, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1327, 4), )

    
    PriceQuotationDateTime_C = property(__PriceQuotationDateTime_C.value, __PriceQuotationDateTime_C.set, None, None)

    
    # Element {http://www.w3schools.com}Balance uses Python identifier Balance
    __Balance = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Balance'), 'Balance', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_httpwww_w3schools_comBalance', True, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1329, 3), )

    
    Balance = property(__Balance.value, __Balance.set, None, None)

    
    # Element {http://www.w3schools.com}SubsequenceB1b_Subbalance uses Python identifier SubsequenceB1b_Subbalance
    __SubsequenceB1b_Subbalance = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SubsequenceB1b_Subbalance'), 'SubsequenceB1b_Subbalance', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_httpwww_w3schools_comSubsequenceB1b_Subbalance', True, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1330, 3), )

    
    SubsequenceB1b_Subbalance = property(__SubsequenceB1b_Subbalance.value, __SubsequenceB1b_Subbalance.set, None, None)

    
    # Element {http://www.w3schools.com}NumberofDaysAccrued uses Python identifier NumberofDaysAccrued
    __NumberofDaysAccrued = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'NumberofDaysAccrued'), 'NumberofDaysAccrued', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_httpwww_w3schools_comNumberofDaysAccrued', False, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1331, 3), )

    
    NumberofDaysAccrued = property(__NumberofDaysAccrued.value, __NumberofDaysAccrued.set, None, None)

    
    # Element {http://www.w3schools.com}Amount uses Python identifier Amount
    __Amount = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Amount'), 'Amount', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_httpwww_w3schools_comAmount', True, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1332, 3), )

    
    Amount = property(__Amount.value, __Amount.set, None, None)

    
    # Element {http://www.w3schools.com}ExchangeRate uses Python identifier ExchangeRate
    __ExchangeRate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ExchangeRate'), 'ExchangeRate', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_httpwww_w3schools_comExchangeRate', False, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1333, 3), )

    
    ExchangeRate = property(__ExchangeRate.value, __ExchangeRate.set, None, None)

    
    # Element {http://www.w3schools.com}HoldingsNarrative uses Python identifier HoldingsNarrative
    __HoldingsNarrative = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'HoldingsNarrative'), 'HoldingsNarrative', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_httpwww_w3schools_comHoldingsNarrative', False, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1334, 3), )

    
    HoldingsNarrative = property(__HoldingsNarrative.value, __HoldingsNarrative.set, None, None)

    
    # Element {http://www.w3schools.com}SubsequenceB1c_QuantityBreakdown uses Python identifier SubsequenceB1c_QuantityBreakdown
    __SubsequenceB1c_QuantityBreakdown = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SubsequenceB1c_QuantityBreakdown'), 'SubsequenceB1c_QuantityBreakdown', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_httpwww_w3schools_comSubsequenceB1c_QuantityBreakdown', True, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1335, 3), )

    
    SubsequenceB1c_QuantityBreakdown = property(__SubsequenceB1c_QuantityBreakdown.value, __SubsequenceB1c_QuantityBreakdown.set, None, None)

    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='16R')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1337, 2)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1337, 2)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1338, 2)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1338, 2)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    
    # Attribute formatTag uses Python identifier formatTag
    __formatTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'formatTag'), 'formatTag', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_formatTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='FIN')
    __formatTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1339, 2)
    __formatTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1339, 2)
    
    formatTag = property(__formatTag.value, __formatTag.set, None, None)

    _ElementMap.update({
        __IdentificationOfFinancialInstrument.name() : __IdentificationOfFinancialInstrument,
        __SubsequenceB1a_FinancialInstrumentAttributes.name() : __SubsequenceB1a_FinancialInstrumentAttributes,
        __CorporateActionOptionCodeIndicator.name() : __CorporateActionOptionCodeIndicator,
        __Price_A.name() : __Price_A,
        __Price_B.name() : __Price_B,
        __Price_E.name() : __Price_E,
        __SourceOfPrice.name() : __SourceOfPrice,
        __PriceQuotationDateTime_A.name() : __PriceQuotationDateTime_A,
        __PriceQuotationDateTime_C.name() : __PriceQuotationDateTime_C,
        __Balance.name() : __Balance,
        __SubsequenceB1b_Subbalance.name() : __SubsequenceB1b_Subbalance,
        __NumberofDaysAccrued.name() : __NumberofDaysAccrued,
        __Amount.name() : __Amount,
        __ExchangeRate.name() : __ExchangeRate,
        __HoldingsNarrative.name() : __HoldingsNarrative,
        __SubsequenceB1c_QuantityBreakdown.name() : __SubsequenceB1c_QuantityBreakdown
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory,
        __formatTag.name() : __formatTag
    })
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument)


# Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes with content type ELEMENT_ONLY
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1341, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}Place_B uses Python identifier Place_B
    __Place_B = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Place_B'), 'Place_B', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_httpwww_w3schools_comPlace_B', True, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1344, 4), )

    
    Place_B = property(__Place_B.value, __Place_B.set, None, None)

    
    # Element {http://www.w3schools.com}Place_D uses Python identifier Place_D
    __Place_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Place_D'), 'Place_D', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_httpwww_w3schools_comPlace_D', True, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1345, 4), )

    
    Place_D = property(__Place_D.value, __Place_D.set, None, None)

    
    # Element {http://www.w3schools.com}Indicator uses Python identifier Indicator
    __Indicator = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Indicator'), 'Indicator', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_httpwww_w3schools_comIndicator', True, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1347, 3), )

    
    Indicator = property(__Indicator.value, __Indicator.set, None, None)

    
    # Element {http://www.w3schools.com}TypeOfFinancialInstrument_A uses Python identifier TypeOfFinancialInstrument_A
    __TypeOfFinancialInstrument_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'TypeOfFinancialInstrument_A'), 'TypeOfFinancialInstrument_A', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_httpwww_w3schools_comTypeOfFinancialInstrument_A', True, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1349, 4), )

    
    TypeOfFinancialInstrument_A = property(__TypeOfFinancialInstrument_A.value, __TypeOfFinancialInstrument_A.set, None, None)

    
    # Element {http://www.w3schools.com}TypeOfFinancialInstrument_B uses Python identifier TypeOfFinancialInstrument_B
    __TypeOfFinancialInstrument_B = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'TypeOfFinancialInstrument_B'), 'TypeOfFinancialInstrument_B', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_httpwww_w3schools_comTypeOfFinancialInstrument_B', True, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1350, 4), )

    
    TypeOfFinancialInstrument_B = property(__TypeOfFinancialInstrument_B.value, __TypeOfFinancialInstrument_B.set, None, None)

    
    # Element {http://www.w3schools.com}TypeOfFinancialInstrument_C uses Python identifier TypeOfFinancialInstrument_C
    __TypeOfFinancialInstrument_C = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'TypeOfFinancialInstrument_C'), 'TypeOfFinancialInstrument_C', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_httpwww_w3schools_comTypeOfFinancialInstrument_C', True, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1351, 4), )

    
    TypeOfFinancialInstrument_C = property(__TypeOfFinancialInstrument_C.value, __TypeOfFinancialInstrument_C.set, None, None)

    
    # Element {http://www.w3schools.com}CurrencyOfDenomination uses Python identifier CurrencyOfDenomination
    __CurrencyOfDenomination = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'CurrencyOfDenomination'), 'CurrencyOfDenomination', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_httpwww_w3schools_comCurrencyOfDenomination', False, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1353, 3), )

    
    CurrencyOfDenomination = property(__CurrencyOfDenomination.value, __CurrencyOfDenomination.set, None, None)

    
    # Element {http://www.w3schools.com}DateTime uses Python identifier DateTime
    __DateTime = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'DateTime'), 'DateTime', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_httpwww_w3schools_comDateTime', True, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1354, 3), )

    
    DateTime = property(__DateTime.value, __DateTime.set, None, None)

    
    # Element {http://www.w3schools.com}Rate uses Python identifier Rate
    __Rate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Rate'), 'Rate', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_httpwww_w3schools_comRate', True, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1355, 3), )

    
    Rate = property(__Rate.value, __Rate.set, None, None)

    
    # Element {http://www.w3schools.com}NumberIdentification_A uses Python identifier NumberIdentification_A
    __NumberIdentification_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'NumberIdentification_A'), 'NumberIdentification_A', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_httpwww_w3schools_comNumberIdentification_A', True, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1357, 4), )

    
    NumberIdentification_A = property(__NumberIdentification_A.value, __NumberIdentification_A.set, None, None)

    
    # Element {http://www.w3schools.com}NumberIdentification_B uses Python identifier NumberIdentification_B
    __NumberIdentification_B = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'NumberIdentification_B'), 'NumberIdentification_B', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_httpwww_w3schools_comNumberIdentification_B', True, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1358, 4), )

    
    NumberIdentification_B = property(__NumberIdentification_B.value, __NumberIdentification_B.set, None, None)

    
    # Element {http://www.w3schools.com}NumberIdentification_K uses Python identifier NumberIdentification_K
    __NumberIdentification_K = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'NumberIdentification_K'), 'NumberIdentification_K', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_httpwww_w3schools_comNumberIdentification_K', True, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1359, 4), )

    
    NumberIdentification_K = property(__NumberIdentification_K.value, __NumberIdentification_K.set, None, None)

    
    # Element {http://www.w3schools.com}Flag uses Python identifier Flag
    __Flag = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Flag'), 'Flag', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_httpwww_w3schools_comFlag', True, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1361, 3), )

    
    Flag = property(__Flag.value, __Flag.set, None, None)

    
    # Element {http://www.w3schools.com}Price_A uses Python identifier Price_A
    __Price_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Price_A'), 'Price_A', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_httpwww_w3schools_comPrice_A', True, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1363, 4), )

    
    Price_A = property(__Price_A.value, __Price_A.set, None, None)

    
    # Element {http://www.w3schools.com}Price_B uses Python identifier Price_B
    __Price_B = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Price_B'), 'Price_B', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_httpwww_w3schools_comPrice_B', True, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1364, 4), )

    
    Price_B = property(__Price_B.value, __Price_B.set, None, None)

    
    # Element {http://www.w3schools.com}QuantityOfFinancialInstrument uses Python identifier QuantityOfFinancialInstrument
    __QuantityOfFinancialInstrument = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'QuantityOfFinancialInstrument'), 'QuantityOfFinancialInstrument', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_httpwww_w3schools_comQuantityOfFinancialInstrument', True, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1366, 3), )

    
    QuantityOfFinancialInstrument = property(__QuantityOfFinancialInstrument.value, __QuantityOfFinancialInstrument.set, None, None)

    
    # Element {http://www.w3schools.com}IdentificationOfFinancialInstrument uses Python identifier IdentificationOfFinancialInstrument
    __IdentificationOfFinancialInstrument = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'IdentificationOfFinancialInstrument'), 'IdentificationOfFinancialInstrument', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_httpwww_w3schools_comIdentificationOfFinancialInstrument', True, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1367, 3), )

    
    IdentificationOfFinancialInstrument = property(__IdentificationOfFinancialInstrument.value, __IdentificationOfFinancialInstrument.set, None, None)

    
    # Element {http://www.w3schools.com}FinancialInstrumentAttributeNarrative uses Python identifier FinancialInstrumentAttributeNarrative
    __FinancialInstrumentAttributeNarrative = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'FinancialInstrumentAttributeNarrative'), 'FinancialInstrumentAttributeNarrative', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_httpwww_w3schools_comFinancialInstrumentAttributeNarrative', False, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1368, 3), )

    
    FinancialInstrumentAttributeNarrative = property(__FinancialInstrumentAttributeNarrative.value, __FinancialInstrumentAttributeNarrative.set, None, None)

    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='16R')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1370, 2)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1370, 2)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1371, 2)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1371, 2)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    
    # Attribute formatTag uses Python identifier formatTag
    __formatTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'formatTag'), 'formatTag', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_formatTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='FIA')
    __formatTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1372, 2)
    __formatTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1372, 2)
    
    formatTag = property(__formatTag.value, __formatTag.set, None, None)

    _ElementMap.update({
        __Place_B.name() : __Place_B,
        __Place_D.name() : __Place_D,
        __Indicator.name() : __Indicator,
        __TypeOfFinancialInstrument_A.name() : __TypeOfFinancialInstrument_A,
        __TypeOfFinancialInstrument_B.name() : __TypeOfFinancialInstrument_B,
        __TypeOfFinancialInstrument_C.name() : __TypeOfFinancialInstrument_C,
        __CurrencyOfDenomination.name() : __CurrencyOfDenomination,
        __DateTime.name() : __DateTime,
        __Rate.name() : __Rate,
        __NumberIdentification_A.name() : __NumberIdentification_A,
        __NumberIdentification_B.name() : __NumberIdentification_B,
        __NumberIdentification_K.name() : __NumberIdentification_K,
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
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes)


# Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance with content type ELEMENT_ONLY
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1374, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}Balance_B uses Python identifier Balance_B
    __Balance_B = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Balance_B'), 'Balance_B', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_httpwww_w3schools_comBalance_B', True, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1377, 4), )

    
    Balance_B = property(__Balance_B.value, __Balance_B.set, None, None)

    
    # Element {http://www.w3schools.com}Balance_C uses Python identifier Balance_C
    __Balance_C = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Balance_C'), 'Balance_C', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_httpwww_w3schools_comBalance_C', True, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1378, 4), )

    
    Balance_C = property(__Balance_C.value, __Balance_C.set, None, None)

    
    # Element {http://www.w3schools.com}ExposureTypeIndicator_F uses Python identifier ExposureTypeIndicator_F
    __ExposureTypeIndicator_F = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ExposureTypeIndicator_F'), 'ExposureTypeIndicator_F', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_httpwww_w3schools_comExposureTypeIndicator_F', False, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1381, 4), )

    
    ExposureTypeIndicator_F = property(__ExposureTypeIndicator_F.value, __ExposureTypeIndicator_F.set, None, None)

    
    # Element {http://www.w3schools.com}ExposureTypeIndicator_H uses Python identifier ExposureTypeIndicator_H
    __ExposureTypeIndicator_H = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ExposureTypeIndicator_H'), 'ExposureTypeIndicator_H', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_httpwww_w3schools_comExposureTypeIndicator_H', False, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1382, 4), )

    
    ExposureTypeIndicator_H = property(__ExposureTypeIndicator_H.value, __ExposureTypeIndicator_H.set, None, None)

    
    # Element {http://www.w3schools.com}Place_B uses Python identifier Place_B
    __Place_B = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Place_B'), 'Place_B', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_httpwww_w3schools_comPlace_B', True, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1385, 4), )

    
    Place_B = property(__Place_B.value, __Place_B.set, None, None)

    
    # Element {http://www.w3schools.com}Place_C uses Python identifier Place_C
    __Place_C = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Place_C'), 'Place_C', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_httpwww_w3schools_comPlace_C', True, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1386, 4), )

    
    Place_C = property(__Place_C.value, __Place_C.set, None, None)

    
    # Element {http://www.w3schools.com}Place_F uses Python identifier Place_F
    __Place_F = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Place_F'), 'Place_F', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_httpwww_w3schools_comPlace_F', True, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1387, 4), )

    
    Place_F = property(__Place_F.value, __Place_F.set, None, None)

    
    # Element {http://www.w3schools.com}Place_L uses Python identifier Place_L
    __Place_L = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Place_L'), 'Place_L', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_httpwww_w3schools_comPlace_L', True, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1388, 4), )

    
    Place_L = property(__Place_L.value, __Place_L.set, None, None)

    
    # Element {http://www.w3schools.com}Price_A uses Python identifier Price_A
    __Price_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Price_A'), 'Price_A', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_httpwww_w3schools_comPrice_A', False, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1391, 4), )

    
    Price_A = property(__Price_A.value, __Price_A.set, None, None)

    
    # Element {http://www.w3schools.com}Price_B uses Python identifier Price_B
    __Price_B = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Price_B'), 'Price_B', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_httpwww_w3schools_comPrice_B', False, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1392, 4), )

    
    Price_B = property(__Price_B.value, __Price_B.set, None, None)

    
    # Element {http://www.w3schools.com}Price_E uses Python identifier Price_E
    __Price_E = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Price_E'), 'Price_E', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_httpwww_w3schools_comPrice_E', False, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1393, 4), )

    
    Price_E = property(__Price_E.value, __Price_E.set, None, None)

    
    # Element {http://www.w3schools.com}PriceQuotationDateTime_A uses Python identifier PriceQuotationDateTime_A
    __PriceQuotationDateTime_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PriceQuotationDateTime_A'), 'PriceQuotationDateTime_A', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_httpwww_w3schools_comPriceQuotationDateTime_A', False, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1396, 4), )

    
    PriceQuotationDateTime_A = property(__PriceQuotationDateTime_A.value, __PriceQuotationDateTime_A.set, None, None)

    
    # Element {http://www.w3schools.com}PriceQuotationDateTime_C uses Python identifier PriceQuotationDateTime_C
    __PriceQuotationDateTime_C = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PriceQuotationDateTime_C'), 'PriceQuotationDateTime_C', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_httpwww_w3schools_comPriceQuotationDateTime_C', False, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1397, 4), )

    
    PriceQuotationDateTime_C = property(__PriceQuotationDateTime_C.value, __PriceQuotationDateTime_C.set, None, None)

    
    # Element {http://www.w3schools.com}NumberOfDaysAccrued uses Python identifier NumberOfDaysAccrued
    __NumberOfDaysAccrued = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'NumberOfDaysAccrued'), 'NumberOfDaysAccrued', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_httpwww_w3schools_comNumberOfDaysAccrued', False, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1399, 3), )

    
    NumberOfDaysAccrued = property(__NumberOfDaysAccrued.value, __NumberOfDaysAccrued.set, None, None)

    
    # Element {http://www.w3schools.com}Amount uses Python identifier Amount
    __Amount = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Amount'), 'Amount', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_httpwww_w3schools_comAmount', True, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1400, 3), )

    
    Amount = property(__Amount.value, __Amount.set, None, None)

    
    # Element {http://www.w3schools.com}ExchangeRate uses Python identifier ExchangeRate
    __ExchangeRate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ExchangeRate'), 'ExchangeRate', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_httpwww_w3schools_comExchangeRate', False, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1401, 3), )

    
    ExchangeRate = property(__ExchangeRate.value, __ExchangeRate.set, None, None)

    
    # Element {http://www.w3schools.com}SubbalanceDetailsNarrative uses Python identifier SubbalanceDetailsNarrative
    __SubbalanceDetailsNarrative = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SubbalanceDetailsNarrative'), 'SubbalanceDetailsNarrative', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_httpwww_w3schools_comSubbalanceDetailsNarrative', False, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1402, 3), )

    
    SubbalanceDetailsNarrative = property(__SubbalanceDetailsNarrative.value, __SubbalanceDetailsNarrative.set, None, None)

    
    # Element {http://www.w3schools.com}SubsequenceB1b1_QuantityBreakdown uses Python identifier SubsequenceB1b1_QuantityBreakdown
    __SubsequenceB1b1_QuantityBreakdown = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SubsequenceB1b1_QuantityBreakdown'), 'SubsequenceB1b1_QuantityBreakdown', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_httpwww_w3schools_comSubsequenceB1b1_QuantityBreakdown', True, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1403, 3), )

    
    SubsequenceB1b1_QuantityBreakdown = property(__SubsequenceB1b1_QuantityBreakdown.value, __SubsequenceB1b1_QuantityBreakdown.set, None, None)

    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='16R')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1405, 2)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1405, 2)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1406, 2)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1406, 2)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    
    # Attribute formatTag uses Python identifier formatTag
    __formatTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'formatTag'), 'formatTag', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_formatTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='SUBBAL')
    __formatTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1407, 2)
    __formatTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1407, 2)
    
    formatTag = property(__formatTag.value, __formatTag.set, None, None)

    _ElementMap.update({
        __Balance_B.name() : __Balance_B,
        __Balance_C.name() : __Balance_C,
        __ExposureTypeIndicator_F.name() : __ExposureTypeIndicator_F,
        __ExposureTypeIndicator_H.name() : __ExposureTypeIndicator_H,
        __Place_B.name() : __Place_B,
        __Place_C.name() : __Place_C,
        __Place_F.name() : __Place_F,
        __Place_L.name() : __Place_L,
        __Price_A.name() : __Price_A,
        __Price_B.name() : __Price_B,
        __Price_E.name() : __Price_E,
        __PriceQuotationDateTime_A.name() : __PriceQuotationDateTime_A,
        __PriceQuotationDateTime_C.name() : __PriceQuotationDateTime_C,
        __NumberOfDaysAccrued.name() : __NumberOfDaysAccrued,
        __Amount.name() : __Amount,
        __ExchangeRate.name() : __ExchangeRate,
        __SubbalanceDetailsNarrative.name() : __SubbalanceDetailsNarrative,
        __SubsequenceB1b1_QuantityBreakdown.name() : __SubsequenceB1b1_QuantityBreakdown
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory,
        __formatTag.name() : __formatTag
    })
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance)


# Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown with content type ELEMENT_ONLY
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1409, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}LotNumber uses Python identifier LotNumber
    __LotNumber = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'LotNumber'), 'LotNumber', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_httpwww_w3schools_comLotNumber', False, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1411, 3), )

    
    LotNumber = property(__LotNumber.value, __LotNumber.set, None, None)

    
    # Element {http://www.w3schools.com}LotBalance uses Python identifier LotBalance
    __LotBalance = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'LotBalance'), 'LotBalance', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_httpwww_w3schools_comLotBalance', False, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1412, 3), )

    
    LotBalance = property(__LotBalance.value, __LotBalance.set, None, None)

    
    # Element {http://www.w3schools.com}LotDateTime_A uses Python identifier LotDateTime_A
    __LotDateTime_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'LotDateTime_A'), 'LotDateTime_A', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_httpwww_w3schools_comLotDateTime_A', False, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1414, 4), )

    
    LotDateTime_A = property(__LotDateTime_A.value, __LotDateTime_A.set, None, None)

    
    # Element {http://www.w3schools.com}LotDateTime_C uses Python identifier LotDateTime_C
    __LotDateTime_C = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'LotDateTime_C'), 'LotDateTime_C', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_httpwww_w3schools_comLotDateTime_C', False, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1415, 4), )

    
    LotDateTime_C = property(__LotDateTime_C.value, __LotDateTime_C.set, None, None)

    
    # Element {http://www.w3schools.com}LotDateTime_E uses Python identifier LotDateTime_E
    __LotDateTime_E = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'LotDateTime_E'), 'LotDateTime_E', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_httpwww_w3schools_comLotDateTime_E', False, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1416, 4), )

    
    LotDateTime_E = property(__LotDateTime_E.value, __LotDateTime_E.set, None, None)

    
    # Element {http://www.w3schools.com}BookLotPrice_A uses Python identifier BookLotPrice_A
    __BookLotPrice_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'BookLotPrice_A'), 'BookLotPrice_A', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_httpwww_w3schools_comBookLotPrice_A', False, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1419, 4), )

    
    BookLotPrice_A = property(__BookLotPrice_A.value, __BookLotPrice_A.set, None, None)

    
    # Element {http://www.w3schools.com}BookLotPrice_B uses Python identifier BookLotPrice_B
    __BookLotPrice_B = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'BookLotPrice_B'), 'BookLotPrice_B', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_httpwww_w3schools_comBookLotPrice_B', False, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1420, 4), )

    
    BookLotPrice_B = property(__BookLotPrice_B.value, __BookLotPrice_B.set, None, None)

    
    # Element {http://www.w3schools.com}TypeofPriceIndicator uses Python identifier TypeofPriceIndicator
    __TypeofPriceIndicator = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'TypeofPriceIndicator'), 'TypeofPriceIndicator', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_httpwww_w3schools_comTypeofPriceIndicator', False, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1422, 3), )

    
    TypeofPriceIndicator = property(__TypeofPriceIndicator.value, __TypeofPriceIndicator.set, None, None)

    
    # Element {http://www.w3schools.com}Amount uses Python identifier Amount
    __Amount = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Amount'), 'Amount', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_httpwww_w3schools_comAmount', True, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1423, 3), )

    
    Amount = property(__Amount.value, __Amount.set, None, None)

    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='16R')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1425, 2)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1425, 2)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1426, 2)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1426, 2)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    
    # Attribute formatTag uses Python identifier formatTag
    __formatTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'formatTag'), 'formatTag', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_formatTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='BREAK')
    __formatTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1427, 2)
    __formatTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1427, 2)
    
    formatTag = property(__formatTag.value, __formatTag.set, None, None)

    _ElementMap.update({
        __LotNumber.name() : __LotNumber,
        __LotBalance.name() : __LotBalance,
        __LotDateTime_A.name() : __LotDateTime_A,
        __LotDateTime_C.name() : __LotDateTime_C,
        __LotDateTime_E.name() : __LotDateTime_E,
        __BookLotPrice_A.name() : __BookLotPrice_A,
        __BookLotPrice_B.name() : __BookLotPrice_B,
        __TypeofPriceIndicator.name() : __TypeofPriceIndicator,
        __Amount.name() : __Amount
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory,
        __formatTag.name() : __formatTag
    })
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown)


# Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown with content type ELEMENT_ONLY
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1429, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}LotNumber uses Python identifier LotNumber
    __LotNumber = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'LotNumber'), 'LotNumber', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_httpwww_w3schools_comLotNumber', False, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1431, 3), )

    
    LotNumber = property(__LotNumber.value, __LotNumber.set, None, None)

    
    # Element {http://www.w3schools.com}LotBalance uses Python identifier LotBalance
    __LotBalance = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'LotBalance'), 'LotBalance', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_httpwww_w3schools_comLotBalance', False, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1432, 3), )

    
    LotBalance = property(__LotBalance.value, __LotBalance.set, None, None)

    
    # Element {http://www.w3schools.com}LotDateTime_A uses Python identifier LotDateTime_A
    __LotDateTime_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'LotDateTime_A'), 'LotDateTime_A', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_httpwww_w3schools_comLotDateTime_A', False, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1434, 4), )

    
    LotDateTime_A = property(__LotDateTime_A.value, __LotDateTime_A.set, None, None)

    
    # Element {http://www.w3schools.com}LotDateTime_C uses Python identifier LotDateTime_C
    __LotDateTime_C = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'LotDateTime_C'), 'LotDateTime_C', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_httpwww_w3schools_comLotDateTime_C', False, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1435, 4), )

    
    LotDateTime_C = property(__LotDateTime_C.value, __LotDateTime_C.set, None, None)

    
    # Element {http://www.w3schools.com}LotDateTime_E uses Python identifier LotDateTime_E
    __LotDateTime_E = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'LotDateTime_E'), 'LotDateTime_E', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_httpwww_w3schools_comLotDateTime_E', False, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1436, 4), )

    
    LotDateTime_E = property(__LotDateTime_E.value, __LotDateTime_E.set, None, None)

    
    # Element {http://www.w3schools.com}BookLotPrice_A uses Python identifier BookLotPrice_A
    __BookLotPrice_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'BookLotPrice_A'), 'BookLotPrice_A', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_httpwww_w3schools_comBookLotPrice_A', False, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1439, 4), )

    
    BookLotPrice_A = property(__BookLotPrice_A.value, __BookLotPrice_A.set, None, None)

    
    # Element {http://www.w3schools.com}BookLotPrice_B uses Python identifier BookLotPrice_B
    __BookLotPrice_B = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'BookLotPrice_B'), 'BookLotPrice_B', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_httpwww_w3schools_comBookLotPrice_B', False, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1440, 4), )

    
    BookLotPrice_B = property(__BookLotPrice_B.value, __BookLotPrice_B.set, None, None)

    
    # Element {http://www.w3schools.com}TypeofPriceIndicator uses Python identifier TypeofPriceIndicator
    __TypeofPriceIndicator = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'TypeofPriceIndicator'), 'TypeofPriceIndicator', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_httpwww_w3schools_comTypeofPriceIndicator', False, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1442, 3), )

    
    TypeofPriceIndicator = property(__TypeofPriceIndicator.value, __TypeofPriceIndicator.set, None, None)

    
    # Element {http://www.w3schools.com}Amount uses Python identifier Amount
    __Amount = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Amount'), 'Amount', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_httpwww_w3schools_comAmount', True, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1443, 3), )

    
    Amount = property(__Amount.value, __Amount.set, None, None)

    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='16R')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1445, 2)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1445, 2)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1446, 2)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1446, 2)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    
    # Attribute formatTag uses Python identifier formatTag
    __formatTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'formatTag'), 'formatTag', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_formatTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='BREAK')
    __formatTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1447, 2)
    __formatTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1447, 2)
    
    formatTag = property(__formatTag.value, __formatTag.set, None, None)

    _ElementMap.update({
        __LotNumber.name() : __LotNumber,
        __LotBalance.name() : __LotBalance,
        __LotDateTime_A.name() : __LotDateTime_A,
        __LotDateTime_C.name() : __LotDateTime_C,
        __LotDateTime_E.name() : __LotDateTime_E,
        __BookLotPrice_A.name() : __BookLotPrice_A,
        __BookLotPrice_B.name() : __BookLotPrice_B,
        __TypeofPriceIndicator.name() : __TypeofPriceIndicator,
        __Amount.name() : __Amount
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory,
        __formatTag.name() : __formatTag
    })
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown)


# Complex type {http://www.w3schools.com}MT535_SequenceC_AdditionalInformation with content type ELEMENT_ONLY
class MT535_SequenceC_AdditionalInformation (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT535_SequenceC_AdditionalInformation with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceC_AdditionalInformation')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1449, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}Party_P uses Python identifier Party_P
    __Party_P = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Party_P'), 'Party_P', '__httpwww_w3schools_com_MT535_SequenceC_AdditionalInformation_httpwww_w3schools_comParty_P', True, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1452, 4), )

    
    Party_P = property(__Party_P.value, __Party_P.set, None, None)

    
    # Element {http://www.w3schools.com}Party_Q uses Python identifier Party_Q
    __Party_Q = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Party_Q'), 'Party_Q', '__httpwww_w3schools_com_MT535_SequenceC_AdditionalInformation_httpwww_w3schools_comParty_Q', True, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1453, 4), )

    
    Party_Q = property(__Party_Q.value, __Party_Q.set, None, None)

    
    # Element {http://www.w3schools.com}Party_R uses Python identifier Party_R
    __Party_R = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Party_R'), 'Party_R', '__httpwww_w3schools_com_MT535_SequenceC_AdditionalInformation_httpwww_w3schools_comParty_R', True, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1454, 4), )

    
    Party_R = property(__Party_R.value, __Party_R.set, None, None)

    
    # Element {http://www.w3schools.com}Amount uses Python identifier Amount
    __Amount = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Amount'), 'Amount', '__httpwww_w3schools_com_MT535_SequenceC_AdditionalInformation_httpwww_w3schools_comAmount', True, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1456, 3), )

    
    Amount = property(__Amount.value, __Amount.set, None, None)

    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT535_SequenceC_AdditionalInformation_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='16R')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1458, 2)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1458, 2)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT535_SequenceC_AdditionalInformation_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1459, 2)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1459, 2)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    
    # Attribute formatTag uses Python identifier formatTag
    __formatTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'formatTag'), 'formatTag', '__httpwww_w3schools_com_MT535_SequenceC_AdditionalInformation_formatTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='ADDINFO')
    __formatTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1460, 2)
    __formatTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1460, 2)
    
    formatTag = property(__formatTag.value, __formatTag.set, None, None)

    _ElementMap.update({
        __Party_P.name() : __Party_P,
        __Party_Q.name() : __Party_Q,
        __Party_R.name() : __Party_R,
        __Amount.name() : __Amount
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory,
        __formatTag.name() : __formatTag
    })
_module_typeBindings.MT535_SequenceC_AdditionalInformation = MT535_SequenceC_AdditionalInformation
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceC_AdditionalInformation', MT535_SequenceC_AdditionalInformation)


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1463, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}SequenceA_GeneralInformation uses Python identifier SequenceA_GeneralInformation
    __SequenceA_GeneralInformation = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SequenceA_GeneralInformation'), 'SequenceA_GeneralInformation', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comSequenceA_GeneralInformation', False, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1465, 4), )

    
    SequenceA_GeneralInformation = property(__SequenceA_GeneralInformation.value, __SequenceA_GeneralInformation.set, None, None)

    
    # Element {http://www.w3schools.com}SequenceB_SubSafekeepingAccount uses Python identifier SequenceB_SubSafekeepingAccount
    __SequenceB_SubSafekeepingAccount = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SequenceB_SubSafekeepingAccount'), 'SequenceB_SubSafekeepingAccount', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comSequenceB_SubSafekeepingAccount', True, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1466, 4), )

    
    SequenceB_SubSafekeepingAccount = property(__SequenceB_SubSafekeepingAccount.value, __SequenceB_SubSafekeepingAccount.set, None, None)

    
    # Element {http://www.w3schools.com}SequenceC_AdditionalInformation uses Python identifier SequenceC_AdditionalInformation
    __SequenceC_AdditionalInformation = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SequenceC_AdditionalInformation'), 'SequenceC_AdditionalInformation', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comSequenceC_AdditionalInformation', True, pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1467, 4), )

    
    SequenceC_AdditionalInformation = property(__SequenceC_AdditionalInformation.value, __SequenceC_AdditionalInformation.set, None, None)

    _ElementMap.update({
        __SequenceA_GeneralInformation.name() : __SequenceA_GeneralInformation,
        __SequenceB_SubSafekeepingAccount.name() : __SequenceB_SubSafekeepingAccount,
        __SequenceC_AdditionalInformation.name() : __SequenceC_AdditionalInformation
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON = CTD_ANON


# Complex type {http://www.w3schools.com}MT535_SequenceA_GeneralInformation_28E_Type with content type SIMPLE
class MT535_SequenceA_GeneralInformation_28E_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT535_SequenceA_GeneralInformation_28E_Type with content type SIMPLE"""
    _TypeDefinition = MT535_SequenceA_GeneralInformation_28E_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceA_GeneralInformation_28E_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 8, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT535_SequenceA_GeneralInformation_28E_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT535_SequenceA_GeneralInformation_28E_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='28E')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 11, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 11, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT535_SequenceA_GeneralInformation_28E_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 12, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 12, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT535_SequenceA_GeneralInformation_28E_Type = MT535_SequenceA_GeneralInformation_28E_Type
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceA_GeneralInformation_28E_Type', MT535_SequenceA_GeneralInformation_28E_Type)


# Complex type {http://www.w3schools.com}MT535_SequenceA_GeneralInformation_13A_Type with content type SIMPLE
class MT535_SequenceA_GeneralInformation_13A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT535_SequenceA_GeneralInformation_13A_Type with content type SIMPLE"""
    _TypeDefinition = MT535_SequenceA_GeneralInformation_13A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceA_GeneralInformation_13A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 29, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT535_SequenceA_GeneralInformation_13A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT535_SequenceA_GeneralInformation_13A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='13A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 32, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 32, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT535_SequenceA_GeneralInformation_13A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 33, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 33, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT535_SequenceA_GeneralInformation_13A_Type = MT535_SequenceA_GeneralInformation_13A_Type
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceA_GeneralInformation_13A_Type', MT535_SequenceA_GeneralInformation_13A_Type)


# Complex type {http://www.w3schools.com}MT535_SequenceA_GeneralInformation_13J_Type with content type SIMPLE
class MT535_SequenceA_GeneralInformation_13J_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT535_SequenceA_GeneralInformation_13J_Type with content type SIMPLE"""
    _TypeDefinition = MT535_SequenceA_GeneralInformation_13J_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceA_GeneralInformation_13J_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 42, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT535_SequenceA_GeneralInformation_13J_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT535_SequenceA_GeneralInformation_13J_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='13J')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 45, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 45, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT535_SequenceA_GeneralInformation_13J_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 46, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 46, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT535_SequenceA_GeneralInformation_13J_Type = MT535_SequenceA_GeneralInformation_13J_Type
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceA_GeneralInformation_13J_Type', MT535_SequenceA_GeneralInformation_13J_Type)


# Complex type {http://www.w3schools.com}MT535_SequenceA_GeneralInformation_20C_Type with content type SIMPLE
class MT535_SequenceA_GeneralInformation_20C_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT535_SequenceA_GeneralInformation_20C_Type with content type SIMPLE"""
    _TypeDefinition = MT535_SequenceA_GeneralInformation_20C_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceA_GeneralInformation_20C_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 55, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT535_SequenceA_GeneralInformation_20C_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT535_SequenceA_GeneralInformation_20C_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='20C')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 58, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 58, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT535_SequenceA_GeneralInformation_20C_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 59, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 59, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT535_SequenceA_GeneralInformation_20C_Type = MT535_SequenceA_GeneralInformation_20C_Type
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceA_GeneralInformation_20C_Type', MT535_SequenceA_GeneralInformation_20C_Type)


# Complex type {http://www.w3schools.com}MT535_SequenceA_GeneralInformation_23G_Type with content type SIMPLE
class MT535_SequenceA_GeneralInformation_23G_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT535_SequenceA_GeneralInformation_23G_Type with content type SIMPLE"""
    _TypeDefinition = MT535_SequenceA_GeneralInformation_23G_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceA_GeneralInformation_23G_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 68, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT535_SequenceA_GeneralInformation_23G_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT535_SequenceA_GeneralInformation_23G_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='23G')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 71, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 71, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT535_SequenceA_GeneralInformation_23G_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 72, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 72, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT535_SequenceA_GeneralInformation_23G_Type = MT535_SequenceA_GeneralInformation_23G_Type
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceA_GeneralInformation_23G_Type', MT535_SequenceA_GeneralInformation_23G_Type)


# Complex type {http://www.w3schools.com}MT535_SequenceA_GeneralInformation_98A_Type with content type SIMPLE
class MT535_SequenceA_GeneralInformation_98A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT535_SequenceA_GeneralInformation_98A_Type with content type SIMPLE"""
    _TypeDefinition = MT535_SequenceA_GeneralInformation_98A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceA_GeneralInformation_98A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 81, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT535_SequenceA_GeneralInformation_98A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT535_SequenceA_GeneralInformation_98A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='98A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 84, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 84, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT535_SequenceA_GeneralInformation_98A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 85, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 85, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT535_SequenceA_GeneralInformation_98A_Type = MT535_SequenceA_GeneralInformation_98A_Type
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceA_GeneralInformation_98A_Type', MT535_SequenceA_GeneralInformation_98A_Type)


# Complex type {http://www.w3schools.com}MT535_SequenceA_GeneralInformation_98C_Type with content type SIMPLE
class MT535_SequenceA_GeneralInformation_98C_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT535_SequenceA_GeneralInformation_98C_Type with content type SIMPLE"""
    _TypeDefinition = MT535_SequenceA_GeneralInformation_98C_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceA_GeneralInformation_98C_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 94, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT535_SequenceA_GeneralInformation_98C_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT535_SequenceA_GeneralInformation_98C_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='98C')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 97, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 97, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT535_SequenceA_GeneralInformation_98C_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 98, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 98, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT535_SequenceA_GeneralInformation_98C_Type = MT535_SequenceA_GeneralInformation_98C_Type
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceA_GeneralInformation_98C_Type', MT535_SequenceA_GeneralInformation_98C_Type)


# Complex type {http://www.w3schools.com}MT535_SequenceA_GeneralInformation_98E_Type with content type SIMPLE
class MT535_SequenceA_GeneralInformation_98E_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT535_SequenceA_GeneralInformation_98E_Type with content type SIMPLE"""
    _TypeDefinition = MT535_SequenceA_GeneralInformation_98E_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceA_GeneralInformation_98E_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 107, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT535_SequenceA_GeneralInformation_98E_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT535_SequenceA_GeneralInformation_98E_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='98E')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 110, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 110, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT535_SequenceA_GeneralInformation_98E_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 111, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 111, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT535_SequenceA_GeneralInformation_98E_Type = MT535_SequenceA_GeneralInformation_98E_Type
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceA_GeneralInformation_98E_Type', MT535_SequenceA_GeneralInformation_98E_Type)


# Complex type {http://www.w3schools.com}MT535_SequenceA_GeneralInformation_22F_Type with content type SIMPLE
class MT535_SequenceA_GeneralInformation_22F_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT535_SequenceA_GeneralInformation_22F_Type with content type SIMPLE"""
    _TypeDefinition = MT535_SequenceA_GeneralInformation_22F_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceA_GeneralInformation_22F_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 120, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT535_SequenceA_GeneralInformation_22F_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT535_SequenceA_GeneralInformation_22F_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='22F')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 123, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 123, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT535_SequenceA_GeneralInformation_22F_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 124, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 124, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT535_SequenceA_GeneralInformation_22F_Type = MT535_SequenceA_GeneralInformation_22F_Type
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceA_GeneralInformation_22F_Type', MT535_SequenceA_GeneralInformation_22F_Type)


# Complex type {http://www.w3schools.com}MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages_13A_Type with content type SIMPLE
class MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages_13A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages_13A_Type with content type SIMPLE"""
    _TypeDefinition = MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages_13A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages_13A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 133, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages_13A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages_13A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='13A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 136, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 136, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages_13A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 137, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 137, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages_13A_Type = MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages_13A_Type
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages_13A_Type', MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages_13A_Type)


# Complex type {http://www.w3schools.com}MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages_13B_Type with content type SIMPLE
class MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages_13B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages_13B_Type with content type SIMPLE"""
    _TypeDefinition = MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages_13B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages_13B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 146, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages_13B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages_13B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='13B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 149, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 149, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages_13B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 150, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 150, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages_13B_Type = MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages_13B_Type
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages_13B_Type', MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages_13B_Type)


# Complex type {http://www.w3schools.com}MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages_20C_Type with content type SIMPLE
class MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages_20C_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages_20C_Type with content type SIMPLE"""
    _TypeDefinition = MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages_20C_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages_20C_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 159, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages_20C_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages_20C_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='20C')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 162, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 162, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages_20C_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 163, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 163, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages_20C_Type = MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages_20C_Type
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages_20C_Type', MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages_20C_Type)


# Complex type {http://www.w3schools.com}MT535_SequenceA_GeneralInformation_95L_Type with content type SIMPLE
class MT535_SequenceA_GeneralInformation_95L_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT535_SequenceA_GeneralInformation_95L_Type with content type SIMPLE"""
    _TypeDefinition = MT535_SequenceA_GeneralInformation_95L_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceA_GeneralInformation_95L_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 172, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT535_SequenceA_GeneralInformation_95L_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT535_SequenceA_GeneralInformation_95L_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='95L')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 175, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 175, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT535_SequenceA_GeneralInformation_95L_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 176, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 176, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT535_SequenceA_GeneralInformation_95L_Type = MT535_SequenceA_GeneralInformation_95L_Type
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceA_GeneralInformation_95L_Type', MT535_SequenceA_GeneralInformation_95L_Type)


# Complex type {http://www.w3schools.com}MT535_SequenceA_GeneralInformation_95P_Type with content type SIMPLE
class MT535_SequenceA_GeneralInformation_95P_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT535_SequenceA_GeneralInformation_95P_Type with content type SIMPLE"""
    _TypeDefinition = MT535_SequenceA_GeneralInformation_95P_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceA_GeneralInformation_95P_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 185, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT535_SequenceA_GeneralInformation_95P_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT535_SequenceA_GeneralInformation_95P_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='95P')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 188, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 188, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT535_SequenceA_GeneralInformation_95P_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 189, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 189, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT535_SequenceA_GeneralInformation_95P_Type = MT535_SequenceA_GeneralInformation_95P_Type
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceA_GeneralInformation_95P_Type', MT535_SequenceA_GeneralInformation_95P_Type)


# Complex type {http://www.w3schools.com}MT535_SequenceA_GeneralInformation_95R_Type with content type SIMPLE
class MT535_SequenceA_GeneralInformation_95R_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT535_SequenceA_GeneralInformation_95R_Type with content type SIMPLE"""
    _TypeDefinition = MT535_SequenceA_GeneralInformation_95R_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceA_GeneralInformation_95R_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 198, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT535_SequenceA_GeneralInformation_95R_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT535_SequenceA_GeneralInformation_95R_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='95R')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 201, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 201, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT535_SequenceA_GeneralInformation_95R_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 202, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 202, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT535_SequenceA_GeneralInformation_95R_Type = MT535_SequenceA_GeneralInformation_95R_Type
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceA_GeneralInformation_95R_Type', MT535_SequenceA_GeneralInformation_95R_Type)


# Complex type {http://www.w3schools.com}MT535_SequenceA_GeneralInformation_97A_Type with content type SIMPLE
class MT535_SequenceA_GeneralInformation_97A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT535_SequenceA_GeneralInformation_97A_Type with content type SIMPLE"""
    _TypeDefinition = MT535_SequenceA_GeneralInformation_97A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceA_GeneralInformation_97A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 211, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT535_SequenceA_GeneralInformation_97A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT535_SequenceA_GeneralInformation_97A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='97A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 214, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 214, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT535_SequenceA_GeneralInformation_97A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 215, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 215, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT535_SequenceA_GeneralInformation_97A_Type = MT535_SequenceA_GeneralInformation_97A_Type
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceA_GeneralInformation_97A_Type', MT535_SequenceA_GeneralInformation_97A_Type)


# Complex type {http://www.w3schools.com}MT535_SequenceA_GeneralInformation_97B_Type with content type SIMPLE
class MT535_SequenceA_GeneralInformation_97B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT535_SequenceA_GeneralInformation_97B_Type with content type SIMPLE"""
    _TypeDefinition = MT535_SequenceA_GeneralInformation_97B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceA_GeneralInformation_97B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 224, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT535_SequenceA_GeneralInformation_97B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT535_SequenceA_GeneralInformation_97B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='97B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 227, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 227, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT535_SequenceA_GeneralInformation_97B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 228, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 228, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT535_SequenceA_GeneralInformation_97B_Type = MT535_SequenceA_GeneralInformation_97B_Type
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceA_GeneralInformation_97B_Type', MT535_SequenceA_GeneralInformation_97B_Type)


# Complex type {http://www.w3schools.com}MT535_SequenceA_GeneralInformation_17B_Type with content type SIMPLE
class MT535_SequenceA_GeneralInformation_17B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT535_SequenceA_GeneralInformation_17B_Type with content type SIMPLE"""
    _TypeDefinition = MT535_SequenceA_GeneralInformation_17B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceA_GeneralInformation_17B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 237, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT535_SequenceA_GeneralInformation_17B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT535_SequenceA_GeneralInformation_17B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='17B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 240, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 240, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT535_SequenceA_GeneralInformation_17B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 241, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 241, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT535_SequenceA_GeneralInformation_17B_Type = MT535_SequenceA_GeneralInformation_17B_Type
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceA_GeneralInformation_17B_Type', MT535_SequenceA_GeneralInformation_17B_Type)


# Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_95P_Type with content type SIMPLE
class MT535_SequenceB_SubSafekeepingAccount_95P_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_95P_Type with content type SIMPLE"""
    _TypeDefinition = MT535_SequenceB_SubSafekeepingAccount_95P_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_95P_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 250, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT535_SequenceB_SubSafekeepingAccount_95P_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_95P_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='95P')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 253, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 253, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_95P_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 254, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 254, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_95P_Type = MT535_SequenceB_SubSafekeepingAccount_95P_Type
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_95P_Type', MT535_SequenceB_SubSafekeepingAccount_95P_Type)


# Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_95R_Type with content type SIMPLE
class MT535_SequenceB_SubSafekeepingAccount_95R_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_95R_Type with content type SIMPLE"""
    _TypeDefinition = MT535_SequenceB_SubSafekeepingAccount_95R_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_95R_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 263, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT535_SequenceB_SubSafekeepingAccount_95R_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_95R_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='95R')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 266, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 266, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_95R_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 267, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 267, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_95R_Type = MT535_SequenceB_SubSafekeepingAccount_95R_Type
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_95R_Type', MT535_SequenceB_SubSafekeepingAccount_95R_Type)


# Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_97A_Type with content type SIMPLE
class MT535_SequenceB_SubSafekeepingAccount_97A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_97A_Type with content type SIMPLE"""
    _TypeDefinition = MT535_SequenceB_SubSafekeepingAccount_97A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_97A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 276, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT535_SequenceB_SubSafekeepingAccount_97A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_97A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='97A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 279, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 279, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_97A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 280, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 280, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_97A_Type = MT535_SequenceB_SubSafekeepingAccount_97A_Type
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_97A_Type', MT535_SequenceB_SubSafekeepingAccount_97A_Type)


# Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_97B_Type with content type SIMPLE
class MT535_SequenceB_SubSafekeepingAccount_97B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_97B_Type with content type SIMPLE"""
    _TypeDefinition = MT535_SequenceB_SubSafekeepingAccount_97B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_97B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 289, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT535_SequenceB_SubSafekeepingAccount_97B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_97B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='97B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 292, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 292, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_97B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 293, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 293, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_97B_Type = MT535_SequenceB_SubSafekeepingAccount_97B_Type
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_97B_Type', MT535_SequenceB_SubSafekeepingAccount_97B_Type)


# Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_94B_Type with content type SIMPLE
class MT535_SequenceB_SubSafekeepingAccount_94B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_94B_Type with content type SIMPLE"""
    _TypeDefinition = MT535_SequenceB_SubSafekeepingAccount_94B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_94B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 302, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT535_SequenceB_SubSafekeepingAccount_94B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_94B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='94B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 305, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 305, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_94B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 306, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 306, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_94B_Type = MT535_SequenceB_SubSafekeepingAccount_94B_Type
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_94B_Type', MT535_SequenceB_SubSafekeepingAccount_94B_Type)


# Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_94C_Type with content type SIMPLE
class MT535_SequenceB_SubSafekeepingAccount_94C_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_94C_Type with content type SIMPLE"""
    _TypeDefinition = MT535_SequenceB_SubSafekeepingAccount_94C_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_94C_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 315, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT535_SequenceB_SubSafekeepingAccount_94C_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_94C_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='94C')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 318, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 318, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_94C_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 319, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 319, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_94C_Type = MT535_SequenceB_SubSafekeepingAccount_94C_Type
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_94C_Type', MT535_SequenceB_SubSafekeepingAccount_94C_Type)


# Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_94F_Type with content type SIMPLE
class MT535_SequenceB_SubSafekeepingAccount_94F_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_94F_Type with content type SIMPLE"""
    _TypeDefinition = MT535_SequenceB_SubSafekeepingAccount_94F_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_94F_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 328, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT535_SequenceB_SubSafekeepingAccount_94F_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_94F_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='94F')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 331, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 331, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_94F_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 332, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 332, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_94F_Type = MT535_SequenceB_SubSafekeepingAccount_94F_Type
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_94F_Type', MT535_SequenceB_SubSafekeepingAccount_94F_Type)


# Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_17B_Type with content type SIMPLE
class MT535_SequenceB_SubSafekeepingAccount_17B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_17B_Type with content type SIMPLE"""
    _TypeDefinition = MT535_SequenceB_SubSafekeepingAccount_17B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_17B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 341, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT535_SequenceB_SubSafekeepingAccount_17B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_17B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='17B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 344, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 344, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_17B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 345, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 345, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_17B_Type = MT535_SequenceB_SubSafekeepingAccount_17B_Type
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_17B_Type', MT535_SequenceB_SubSafekeepingAccount_17B_Type)


# Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_35B_Type with content type SIMPLE
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_35B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_35B_Type with content type SIMPLE"""
    _TypeDefinition = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_35B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_35B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 354, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_35B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_35B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='35B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 357, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 357, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_35B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 358, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 358, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_35B_Type = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_35B_Type
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_35B_Type', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_35B_Type)


# Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_94B_Type with content type SIMPLE
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_94B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_94B_Type with content type SIMPLE"""
    _TypeDefinition = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_94B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_94B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 367, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_94B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_94B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='94B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 370, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 370, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_94B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 371, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 371, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_94B_Type = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_94B_Type
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_94B_Type', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_94B_Type)


# Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_94D_Type with content type SIMPLE
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_94D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_94D_Type with content type SIMPLE"""
    _TypeDefinition = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_94D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_94D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 380, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_94D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_94D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='94D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 383, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 383, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_94D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 384, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 384, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_94D_Type = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_94D_Type
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_94D_Type', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_94D_Type)


# Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_22F_Type with content type SIMPLE
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_22F_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_22F_Type with content type SIMPLE"""
    _TypeDefinition = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_22F_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_22F_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 393, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_22F_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_22F_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='22F')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 396, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 396, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_22F_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 397, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 397, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_22F_Type = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_22F_Type
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_22F_Type', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_22F_Type)


# Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_12A_Type with content type SIMPLE
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_12A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_12A_Type with content type SIMPLE"""
    _TypeDefinition = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_12A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_12A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 406, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_12A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_12A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='12A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 409, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 409, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_12A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 410, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 410, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_12A_Type = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_12A_Type
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_12A_Type', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_12A_Type)


# Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_12B_Type with content type SIMPLE
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_12B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_12B_Type with content type SIMPLE"""
    _TypeDefinition = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_12B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_12B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 419, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_12B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_12B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='12B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 422, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 422, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_12B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 423, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 423, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_12B_Type = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_12B_Type
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_12B_Type', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_12B_Type)


# Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_12C_Type with content type SIMPLE
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_12C_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_12C_Type with content type SIMPLE"""
    _TypeDefinition = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_12C_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_12C_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 432, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_12C_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_12C_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='12C')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 435, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 435, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_12C_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 436, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 436, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_12C_Type = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_12C_Type
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_12C_Type', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_12C_Type)


# Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_11A_Type with content type SIMPLE
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_11A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_11A_Type with content type SIMPLE"""
    _TypeDefinition = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_11A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_11A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 445, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_11A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_11A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='11A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 448, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 448, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_11A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 449, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 449, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_11A_Type = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_11A_Type
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_11A_Type', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_11A_Type)


# Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_98A_Type with content type SIMPLE
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_98A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_98A_Type with content type SIMPLE"""
    _TypeDefinition = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_98A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_98A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 458, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_98A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_98A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='98A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 461, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 461, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_98A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 462, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 462, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_98A_Type = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_98A_Type
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_98A_Type', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_98A_Type)


# Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_92A_Type with content type SIMPLE
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_92A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_92A_Type with content type SIMPLE"""
    _TypeDefinition = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_92A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_92A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 471, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_92A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_92A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='92A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 474, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 474, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_92A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 475, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 475, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_92A_Type = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_92A_Type
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_92A_Type', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_92A_Type)


# Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_13A_Type with content type SIMPLE
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_13A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_13A_Type with content type SIMPLE"""
    _TypeDefinition = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_13A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_13A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 484, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_13A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_13A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='13A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 487, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 487, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_13A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 488, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 488, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_13A_Type = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_13A_Type
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_13A_Type', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_13A_Type)


# Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_13B_Type with content type SIMPLE
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_13B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_13B_Type with content type SIMPLE"""
    _TypeDefinition = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_13B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_13B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 497, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_13B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_13B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='13B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 500, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 500, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_13B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 501, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 501, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_13B_Type = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_13B_Type
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_13B_Type', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_13B_Type)


# Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_13K_Type with content type SIMPLE
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_13K_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_13K_Type with content type SIMPLE"""
    _TypeDefinition = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_13K_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_13K_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 510, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_13K_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_13K_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='13K')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 513, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 513, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_13K_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 514, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 514, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_13K_Type = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_13K_Type
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_13K_Type', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_13K_Type)


# Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_17B_Type with content type SIMPLE
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_17B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_17B_Type with content type SIMPLE"""
    _TypeDefinition = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_17B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_17B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 523, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_17B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_17B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='17B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 526, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 526, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_17B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 527, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 527, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_17B_Type = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_17B_Type
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_17B_Type', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_17B_Type)


# Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_90A_Type with content type SIMPLE
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_90A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_90A_Type with content type SIMPLE"""
    _TypeDefinition = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_90A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_90A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 536, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_90A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_90A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='90A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 539, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 539, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_90A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 540, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 540, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_90A_Type = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_90A_Type
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_90A_Type', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_90A_Type)


# Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_90B_Type with content type SIMPLE
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_90B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_90B_Type with content type SIMPLE"""
    _TypeDefinition = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_90B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_90B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 549, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_90B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_90B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='90B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 552, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 552, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_90B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 553, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 553, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_90B_Type = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_90B_Type
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_90B_Type', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_90B_Type)


# Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_36B_Type with content type SIMPLE
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_36B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_36B_Type with content type SIMPLE"""
    _TypeDefinition = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_36B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_36B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 562, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_36B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_36B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='36B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 565, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 565, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_36B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 566, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 566, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_36B_Type = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_36B_Type
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_36B_Type', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_36B_Type)


# Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_35B_Type with content type SIMPLE
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_35B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_35B_Type with content type SIMPLE"""
    _TypeDefinition = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_35B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_35B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 575, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_35B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_35B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='35B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 578, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 578, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_35B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 579, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 579, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_35B_Type = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_35B_Type
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_35B_Type', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_35B_Type)


# Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_70E_Type with content type SIMPLE
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_70E_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_70E_Type with content type SIMPLE"""
    _TypeDefinition = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_70E_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_70E_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 588, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_70E_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_70E_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='70E')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 591, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 591, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_70E_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 592, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 592, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_70E_Type = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_70E_Type
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_70E_Type', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_70E_Type)


# Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_22H_Type with content type SIMPLE
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_22H_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_22H_Type with content type SIMPLE"""
    _TypeDefinition = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_22H_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_22H_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 601, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_22H_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_22H_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='22H')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 604, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 604, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_22H_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 605, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 605, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_22H_Type = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_22H_Type
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_22H_Type', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_22H_Type)


# Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_90A_Type with content type SIMPLE
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_90A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_90A_Type with content type SIMPLE"""
    _TypeDefinition = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_90A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_90A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 614, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_90A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_90A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='90A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 617, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 617, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_90A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 618, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 618, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_90A_Type = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_90A_Type
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_90A_Type', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_90A_Type)


# Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_90B_Type with content type SIMPLE
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_90B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_90B_Type with content type SIMPLE"""
    _TypeDefinition = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_90B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_90B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 627, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_90B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_90B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='90B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 630, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 630, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_90B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 631, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 631, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_90B_Type = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_90B_Type
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_90B_Type', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_90B_Type)


# Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_90E_Type with content type SIMPLE
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_90E_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_90E_Type with content type SIMPLE"""
    _TypeDefinition = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_90E_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_90E_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 640, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_90E_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_90E_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='90E')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 643, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 643, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_90E_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 644, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 644, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_90E_Type = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_90E_Type
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_90E_Type', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_90E_Type)


# Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_94B_Type with content type SIMPLE
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_94B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_94B_Type with content type SIMPLE"""
    _TypeDefinition = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_94B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_94B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 653, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_94B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_94B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='94B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 656, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 656, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_94B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 657, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 657, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_94B_Type = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_94B_Type
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_94B_Type', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_94B_Type)


# Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_98A_Type with content type SIMPLE
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_98A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_98A_Type with content type SIMPLE"""
    _TypeDefinition = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_98A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_98A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 666, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_98A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_98A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='98A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 669, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 669, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_98A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 670, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 670, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_98A_Type = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_98A_Type
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_98A_Type', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_98A_Type)


# Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_98C_Type with content type SIMPLE
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_98C_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_98C_Type with content type SIMPLE"""
    _TypeDefinition = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_98C_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_98C_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 679, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_98C_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_98C_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='98C')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 682, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 682, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_98C_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 683, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 683, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_98C_Type = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_98C_Type
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_98C_Type', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_98C_Type)


# Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_93B_Type with content type SIMPLE
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_93B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_93B_Type with content type SIMPLE"""
    _TypeDefinition = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_93B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_93B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 692, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_93B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_93B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='93B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 695, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 695, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_93B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 696, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 696, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_93B_Type = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_93B_Type
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_93B_Type', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_93B_Type)


# Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_93B_Type with content type SIMPLE
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_93B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_93B_Type with content type SIMPLE"""
    _TypeDefinition = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_93B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_93B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 705, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_93B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_93B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='93B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 708, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 708, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_93B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 709, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 709, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_93B_Type = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_93B_Type
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_93B_Type', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_93B_Type)


# Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_93C_Type with content type SIMPLE
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_93C_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_93C_Type with content type SIMPLE"""
    _TypeDefinition = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_93C_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_93C_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 718, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_93C_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_93C_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='93C')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 721, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 721, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_93C_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 722, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 722, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_93C_Type = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_93C_Type
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_93C_Type', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_93C_Type)


# Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_22F_Type with content type SIMPLE
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_22F_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_22F_Type with content type SIMPLE"""
    _TypeDefinition = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_22F_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_22F_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 731, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_22F_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_22F_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='22F')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 734, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 734, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_22F_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 735, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 735, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_22F_Type = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_22F_Type
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_22F_Type', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_22F_Type)


# Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_22H_Type with content type SIMPLE
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_22H_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_22H_Type with content type SIMPLE"""
    _TypeDefinition = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_22H_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_22H_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 744, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_22H_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_22H_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='22H')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 747, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 747, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_22H_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 748, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 748, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_22H_Type = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_22H_Type
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_22H_Type', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_22H_Type)


# Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_94B_Type with content type SIMPLE
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_94B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_94B_Type with content type SIMPLE"""
    _TypeDefinition = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_94B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_94B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 757, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_94B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_94B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='94B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 760, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 760, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_94B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 761, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 761, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_94B_Type = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_94B_Type
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_94B_Type', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_94B_Type)


# Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_94C_Type with content type SIMPLE
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_94C_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_94C_Type with content type SIMPLE"""
    _TypeDefinition = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_94C_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_94C_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 770, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_94C_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_94C_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='94C')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 773, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 773, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_94C_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 774, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 774, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_94C_Type = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_94C_Type
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_94C_Type', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_94C_Type)


# Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_94F_Type with content type SIMPLE
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_94F_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_94F_Type with content type SIMPLE"""
    _TypeDefinition = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_94F_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_94F_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 783, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_94F_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_94F_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='94F')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 786, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 786, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_94F_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 787, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 787, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_94F_Type = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_94F_Type
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_94F_Type', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_94F_Type)


# Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_90A_Type with content type SIMPLE
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_90A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_90A_Type with content type SIMPLE"""
    _TypeDefinition = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_90A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_90A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 796, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_90A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_90A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='90A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 799, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 799, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_90A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 800, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 800, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_90A_Type = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_90A_Type
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_90A_Type', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_90A_Type)


# Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_90B_Type with content type SIMPLE
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_90B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_90B_Type with content type SIMPLE"""
    _TypeDefinition = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_90B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_90B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 809, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_90B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_90B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='90B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 812, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 812, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_90B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 813, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 813, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_90B_Type = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_90B_Type
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_90B_Type', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_90B_Type)


# Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_90E_Type with content type SIMPLE
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_90E_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_90E_Type with content type SIMPLE"""
    _TypeDefinition = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_90E_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_90E_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 822, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_90E_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_90E_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='90E')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 825, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 825, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_90E_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 826, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 826, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_90E_Type = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_90E_Type
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_90E_Type', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_90E_Type)


# Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_98A_Type with content type SIMPLE
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_98A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_98A_Type with content type SIMPLE"""
    _TypeDefinition = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_98A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_98A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 835, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_98A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_98A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='98A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 838, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 838, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_98A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 839, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 839, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_98A_Type = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_98A_Type
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_98A_Type', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_98A_Type)


# Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_98C_Type with content type SIMPLE
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_98C_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_98C_Type with content type SIMPLE"""
    _TypeDefinition = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_98C_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_98C_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 848, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_98C_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_98C_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='98C')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 851, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 851, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_98C_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 852, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 852, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_98C_Type = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_98C_Type
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_98C_Type', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_98C_Type)


# Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_99A_Type with content type SIMPLE
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_99A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_99A_Type with content type SIMPLE"""
    _TypeDefinition = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_99A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_99A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 861, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_99A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_99A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='99A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 864, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 864, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_99A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 865, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 865, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_99A_Type = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_99A_Type
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_99A_Type', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_99A_Type)


# Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_19A_Type with content type SIMPLE
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_19A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_19A_Type with content type SIMPLE"""
    _TypeDefinition = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_19A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_19A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 874, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_19A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_19A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='19A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 877, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 877, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_19A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 878, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 878, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_19A_Type = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_19A_Type
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_19A_Type', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_19A_Type)


# Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_92B_Type with content type SIMPLE
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_92B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_92B_Type with content type SIMPLE"""
    _TypeDefinition = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_92B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_92B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 887, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_92B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_92B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='92B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 890, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 890, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_92B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 891, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 891, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_92B_Type = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_92B_Type
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_92B_Type', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_92B_Type)


# Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_70C_Type with content type SIMPLE
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_70C_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_70C_Type with content type SIMPLE"""
    _TypeDefinition = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_70C_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_70C_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 900, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_70C_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_70C_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='70C')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 903, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 903, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_70C_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 904, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 904, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_70C_Type = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_70C_Type
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_70C_Type', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_70C_Type)


# Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_13B_Type with content type SIMPLE
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_13B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_13B_Type with content type SIMPLE"""
    _TypeDefinition = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_13B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_13B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 913, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_13B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_13B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='13B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 916, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 916, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_13B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 917, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 917, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_13B_Type = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_13B_Type
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_13B_Type', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_13B_Type)


# Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_93B_Type with content type SIMPLE
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_93B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_93B_Type with content type SIMPLE"""
    _TypeDefinition = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_93B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_93B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 926, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_93B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_93B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='93B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 929, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 929, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_93B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 930, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 930, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_93B_Type = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_93B_Type
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_93B_Type', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_93B_Type)


# Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_98A_Type with content type SIMPLE
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_98A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_98A_Type with content type SIMPLE"""
    _TypeDefinition = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_98A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_98A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 939, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_98A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_98A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='98A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 942, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 942, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_98A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 943, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 943, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_98A_Type = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_98A_Type
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_98A_Type', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_98A_Type)


# Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_98C_Type with content type SIMPLE
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_98C_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_98C_Type with content type SIMPLE"""
    _TypeDefinition = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_98C_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_98C_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 952, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_98C_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_98C_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='98C')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 955, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 955, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_98C_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 956, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 956, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_98C_Type = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_98C_Type
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_98C_Type', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_98C_Type)


# Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_98E_Type with content type SIMPLE
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_98E_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_98E_Type with content type SIMPLE"""
    _TypeDefinition = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_98E_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_98E_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 965, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_98E_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_98E_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='98E')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 968, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 968, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_98E_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 969, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 969, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_98E_Type = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_98E_Type
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_98E_Type', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_98E_Type)


# Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_90A_Type with content type SIMPLE
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_90A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_90A_Type with content type SIMPLE"""
    _TypeDefinition = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_90A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_90A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 978, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_90A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_90A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='90A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 981, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 981, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_90A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 982, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 982, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_90A_Type = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_90A_Type
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_90A_Type', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_90A_Type)


# Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_90B_Type with content type SIMPLE
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_90B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_90B_Type with content type SIMPLE"""
    _TypeDefinition = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_90B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_90B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 991, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_90B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_90B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='90B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 994, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 994, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_90B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 995, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 995, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_90B_Type = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_90B_Type
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_90B_Type', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_90B_Type)


# Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_22F_Type with content type SIMPLE
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_22F_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_22F_Type with content type SIMPLE"""
    _TypeDefinition = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_22F_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_22F_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1004, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_22F_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_22F_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='22F')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1007, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1007, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_22F_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1008, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1008, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_22F_Type = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_22F_Type
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_22F_Type', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_22F_Type)


# Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_19A_Type with content type SIMPLE
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_19A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_19A_Type with content type SIMPLE"""
    _TypeDefinition = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_19A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_19A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1017, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_19A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_19A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='19A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1020, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1020, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_19A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1021, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1021, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_19A_Type = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_19A_Type
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_19A_Type', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_19A_Type)


# Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_99A_Type with content type SIMPLE
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_99A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_99A_Type with content type SIMPLE"""
    _TypeDefinition = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_99A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_99A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1030, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_99A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_99A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='99A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1033, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1033, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_99A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1034, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1034, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_99A_Type = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_99A_Type
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_99A_Type', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_99A_Type)


# Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_19A_Type with content type SIMPLE
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_19A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_19A_Type with content type SIMPLE"""
    _TypeDefinition = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_19A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_19A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1043, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_19A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_19A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='19A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1046, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1046, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_19A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1047, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1047, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_19A_Type = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_19A_Type
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_19A_Type', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_19A_Type)


# Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_92B_Type with content type SIMPLE
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_92B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_92B_Type with content type SIMPLE"""
    _TypeDefinition = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_92B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_92B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1056, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_92B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_92B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='92B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1059, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1059, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_92B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1060, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1060, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_92B_Type = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_92B_Type
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_92B_Type', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_92B_Type)


# Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_70E_Type with content type SIMPLE
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_70E_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_70E_Type with content type SIMPLE"""
    _TypeDefinition = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_70E_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_70E_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1069, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_70E_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_70E_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='70E')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1072, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1072, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_70E_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1073, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1073, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_70E_Type = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_70E_Type
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_70E_Type', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_70E_Type)


# Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_13B_Type with content type SIMPLE
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_13B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_13B_Type with content type SIMPLE"""
    _TypeDefinition = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_13B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_13B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1082, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_13B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_13B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='13B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1085, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1085, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_13B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1086, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1086, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_13B_Type = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_13B_Type
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_13B_Type', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_13B_Type)


# Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_93B_Type with content type SIMPLE
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_93B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_93B_Type with content type SIMPLE"""
    _TypeDefinition = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_93B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_93B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1095, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_93B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_93B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='93B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1098, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1098, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_93B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1099, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1099, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_93B_Type = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_93B_Type
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_93B_Type', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_93B_Type)


# Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_98A_Type with content type SIMPLE
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_98A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_98A_Type with content type SIMPLE"""
    _TypeDefinition = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_98A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_98A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1108, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_98A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_98A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='98A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1111, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1111, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_98A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1112, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1112, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_98A_Type = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_98A_Type
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_98A_Type', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_98A_Type)


# Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_98C_Type with content type SIMPLE
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_98C_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_98C_Type with content type SIMPLE"""
    _TypeDefinition = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_98C_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_98C_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1121, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_98C_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_98C_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='98C')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1124, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1124, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_98C_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1125, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1125, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_98C_Type = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_98C_Type
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_98C_Type', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_98C_Type)


# Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_98E_Type with content type SIMPLE
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_98E_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_98E_Type with content type SIMPLE"""
    _TypeDefinition = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_98E_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_98E_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1134, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_98E_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_98E_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='98E')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1137, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1137, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_98E_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1138, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1138, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_98E_Type = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_98E_Type
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_98E_Type', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_98E_Type)


# Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_90A_Type with content type SIMPLE
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_90A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_90A_Type with content type SIMPLE"""
    _TypeDefinition = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_90A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_90A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1147, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_90A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_90A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='90A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1150, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1150, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_90A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1151, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1151, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_90A_Type = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_90A_Type
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_90A_Type', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_90A_Type)


# Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_90B_Type with content type SIMPLE
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_90B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_90B_Type with content type SIMPLE"""
    _TypeDefinition = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_90B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_90B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1160, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_90B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_90B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='90B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1163, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1163, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_90B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1164, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1164, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_90B_Type = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_90B_Type
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_90B_Type', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_90B_Type)


# Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_22F_Type with content type SIMPLE
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_22F_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_22F_Type with content type SIMPLE"""
    _TypeDefinition = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_22F_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_22F_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1173, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_22F_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_22F_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='22F')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1176, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1176, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_22F_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1177, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1177, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_22F_Type = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_22F_Type
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_22F_Type', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_22F_Type)


# Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_19A_Type with content type SIMPLE
class MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_19A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_19A_Type with content type SIMPLE"""
    _TypeDefinition = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_19A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_19A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1186, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_19A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_19A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='19A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1189, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1189, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_19A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1190, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1190, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_19A_Type = MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_19A_Type
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_19A_Type', MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_19A_Type)


# Complex type {http://www.w3schools.com}MT535_SequenceC_AdditionalInformation_95P_Type with content type SIMPLE
class MT535_SequenceC_AdditionalInformation_95P_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT535_SequenceC_AdditionalInformation_95P_Type with content type SIMPLE"""
    _TypeDefinition = MT535_SequenceC_AdditionalInformation_95P_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceC_AdditionalInformation_95P_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1199, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT535_SequenceC_AdditionalInformation_95P_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT535_SequenceC_AdditionalInformation_95P_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='95P')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1202, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1202, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT535_SequenceC_AdditionalInformation_95P_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1203, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1203, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT535_SequenceC_AdditionalInformation_95P_Type = MT535_SequenceC_AdditionalInformation_95P_Type
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceC_AdditionalInformation_95P_Type', MT535_SequenceC_AdditionalInformation_95P_Type)


# Complex type {http://www.w3schools.com}MT535_SequenceC_AdditionalInformation_95Q_Type with content type SIMPLE
class MT535_SequenceC_AdditionalInformation_95Q_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT535_SequenceC_AdditionalInformation_95Q_Type with content type SIMPLE"""
    _TypeDefinition = MT535_SequenceC_AdditionalInformation_95Q_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceC_AdditionalInformation_95Q_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1212, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT535_SequenceC_AdditionalInformation_95Q_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT535_SequenceC_AdditionalInformation_95Q_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='95Q')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1215, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1215, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT535_SequenceC_AdditionalInformation_95Q_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1216, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1216, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT535_SequenceC_AdditionalInformation_95Q_Type = MT535_SequenceC_AdditionalInformation_95Q_Type
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceC_AdditionalInformation_95Q_Type', MT535_SequenceC_AdditionalInformation_95Q_Type)


# Complex type {http://www.w3schools.com}MT535_SequenceC_AdditionalInformation_95R_Type with content type SIMPLE
class MT535_SequenceC_AdditionalInformation_95R_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT535_SequenceC_AdditionalInformation_95R_Type with content type SIMPLE"""
    _TypeDefinition = MT535_SequenceC_AdditionalInformation_95R_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceC_AdditionalInformation_95R_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1225, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT535_SequenceC_AdditionalInformation_95R_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT535_SequenceC_AdditionalInformation_95R_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='95R')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1228, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1228, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT535_SequenceC_AdditionalInformation_95R_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1229, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1229, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT535_SequenceC_AdditionalInformation_95R_Type = MT535_SequenceC_AdditionalInformation_95R_Type
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceC_AdditionalInformation_95R_Type', MT535_SequenceC_AdditionalInformation_95R_Type)


# Complex type {http://www.w3schools.com}MT535_SequenceC_AdditionalInformation_19A_Type with content type SIMPLE
class MT535_SequenceC_AdditionalInformation_19A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT535_SequenceC_AdditionalInformation_19A_Type with content type SIMPLE"""
    _TypeDefinition = MT535_SequenceC_AdditionalInformation_19A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT535_SequenceC_AdditionalInformation_19A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1238, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT535_SequenceC_AdditionalInformation_19A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT535_SequenceC_AdditionalInformation_19A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='19A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1241, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1241, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT535_SequenceC_AdditionalInformation_19A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1242, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1242, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT535_SequenceC_AdditionalInformation_19A_Type = MT535_SequenceC_AdditionalInformation_19A_Type
Namespace.addCategoryObject('typeBinding', 'MT535_SequenceC_AdditionalInformation_19A_Type', MT535_SequenceC_AdditionalInformation_19A_Type)


MT535 = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'MT535'), CTD_ANON, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1462, 1))
Namespace.addCategoryObject('elementBinding', MT535.name().localName(), MT535)



MT535_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PageNumber'), MT535_SequenceA_GeneralInformation_28E_Type, scope=MT535_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1248, 3)))

MT535_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'StatementNumber'), MT535_SequenceA_GeneralInformation_13a_Type, scope=MT535_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1249, 3)))

MT535_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'StatementNumber_A'), MT535_SequenceA_GeneralInformation_13A_Type, scope=MT535_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1251, 4)))

MT535_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'StatementNumber_J'), MT535_SequenceA_GeneralInformation_13J_Type, scope=MT535_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1252, 4)))

MT535_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SendersMessageReference'), MT535_SequenceA_GeneralInformation_20C_Type, scope=MT535_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1254, 3)))

MT535_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'FunctionOfMessage'), MT535_SequenceA_GeneralInformation_23G_Type, scope=MT535_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1255, 3)))

MT535_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DateTime_A'), MT535_SequenceA_GeneralInformation_98A_Type, scope=MT535_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1257, 4)))

MT535_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DateTime_C'), MT535_SequenceA_GeneralInformation_98C_Type, scope=MT535_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1258, 4)))

MT535_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DateTime_E'), MT535_SequenceA_GeneralInformation_98E_Type, scope=MT535_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1259, 4)))

MT535_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Indicator'), MT535_SequenceA_GeneralInformation_22F_Type, scope=MT535_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1261, 3)))

MT535_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SubsequenceA1_Linkages'), MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages, scope=MT535_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1262, 3)))

MT535_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Party_L'), MT535_SequenceA_GeneralInformation_95L_Type, scope=MT535_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1264, 4)))

MT535_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Party_P'), MT535_SequenceA_GeneralInformation_95P_Type, scope=MT535_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1265, 4)))

MT535_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Party_R'), MT535_SequenceA_GeneralInformation_95R_Type, scope=MT535_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1266, 4)))

MT535_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SafekeepingAccount_A'), MT535_SequenceA_GeneralInformation_97A_Type, scope=MT535_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1269, 4)))

MT535_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SafekeepingAccount_B'), MT535_SequenceA_GeneralInformation_97B_Type, scope=MT535_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1270, 4)))

MT535_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Flag'), MT535_SequenceA_GeneralInformation_17B_Type, scope=MT535_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1272, 3)))

def _BuildAutomaton ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1249, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1250, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1251, 4))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1252, 4))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1262, 3))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1263, 3))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1264, 4))
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1265, 4))
    counters.add(cc_7)
    cc_8 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1266, 4))
    counters.add(cc_8)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT535_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PageNumber')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1248, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT535_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'StatementNumber')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1249, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT535_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'StatementNumber_A')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1251, 4))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT535_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'StatementNumber_J')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1252, 4))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT535_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SendersMessageReference')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1254, 3))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT535_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'FunctionOfMessage')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1255, 3))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT535_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'DateTime_A')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1257, 4))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT535_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'DateTime_C')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1258, 4))
    st_7 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT535_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'DateTime_E')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1259, 4))
    st_8 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT535_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Indicator')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1261, 3))
    st_9 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT535_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SubsequenceA1_Linkages')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1262, 3))
    st_10 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_10)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT535_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Party_L')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1264, 4))
    st_11 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_11)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT535_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Party_P')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1265, 4))
    st_12 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_12)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT535_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Party_R')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1266, 4))
    st_13 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_13)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT535_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SafekeepingAccount_A')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1269, 4))
    st_14 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_14)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT535_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SafekeepingAccount_B')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1270, 4))
    st_15 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_15)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT535_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Flag')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1272, 3))
    st_16 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_16)
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
    st_8._set_transitionSet(transitions)
    transitions = []
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
    st_9._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_4, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_4, False) ]))
    st_10._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_5, True),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_6, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_5, True),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_5, True),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_5, False),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_5, False),
        fac.UpdateInstruction(cc_6, False) ]))
    st_11._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_5, True),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_5, True),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_7, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_5, True),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_5, False),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_5, False),
        fac.UpdateInstruction(cc_7, False) ]))
    st_12._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_5, True),
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_5, True),
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_5, True),
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_8, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_5, False),
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_5, False),
        fac.UpdateInstruction(cc_8, False) ]))
    st_13._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_16, [
         ]))
    st_14._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_16, [
         ]))
    st_15._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_16, [
         ]))
    st_16._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
MT535_SequenceA_GeneralInformation._Automaton = _BuildAutomaton()




MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'LinkedMessage_A'), MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages_13A_Type, scope=MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1281, 4)))

MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'LinkedMessage_B'), MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages_13B_Type, scope=MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1282, 4)))

MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Reference'), MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages_20C_Type, scope=MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1284, 3)))

def _BuildAutomaton_ ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_
    del _BuildAutomaton_
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1280, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1281, 4))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1282, 4))
    counters.add(cc_2)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'LinkedMessage_A')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1281, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'LinkedMessage_B')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1282, 4))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Reference')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1284, 3))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
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
    st_1._set_transitionSet(transitions)
    transitions = []
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
MT535_SequenceA_GeneralInformation_SubsequenceA1_Linkages._Automaton = _BuildAutomaton_()




MT535_SequenceB_SubSafekeepingAccount._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Party_L'), MT535_SequenceB_SubSafekeepingAccount_95P_Type, scope=MT535_SequenceB_SubSafekeepingAccount, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1293, 4)))

MT535_SequenceB_SubSafekeepingAccount._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Party_P'), MT535_SequenceB_SubSafekeepingAccount_95P_Type, scope=MT535_SequenceB_SubSafekeepingAccount, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1294, 4)))

MT535_SequenceB_SubSafekeepingAccount._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Party_R'), MT535_SequenceB_SubSafekeepingAccount_95R_Type, scope=MT535_SequenceB_SubSafekeepingAccount, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1295, 4)))

MT535_SequenceB_SubSafekeepingAccount._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SafekeepingAccount_A'), MT535_SequenceB_SubSafekeepingAccount_97A_Type, scope=MT535_SequenceB_SubSafekeepingAccount, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1298, 4)))

MT535_SequenceB_SubSafekeepingAccount._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SafekeepingAccount_B'), MT535_SequenceB_SubSafekeepingAccount_97B_Type, scope=MT535_SequenceB_SubSafekeepingAccount, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1299, 4)))

MT535_SequenceB_SubSafekeepingAccount._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PlaceOfSafekeeping_B'), MT535_SequenceB_SubSafekeepingAccount_94B_Type, scope=MT535_SequenceB_SubSafekeepingAccount, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1302, 4)))

MT535_SequenceB_SubSafekeepingAccount._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PlaceOfSafekeeping_C'), MT535_SequenceB_SubSafekeepingAccount_94C_Type, scope=MT535_SequenceB_SubSafekeepingAccount, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1303, 4)))

MT535_SequenceB_SubSafekeepingAccount._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PlaceOfSafekeeping_F'), MT535_SequenceB_SubSafekeepingAccount_94F_Type, scope=MT535_SequenceB_SubSafekeepingAccount, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1304, 4)))

MT535_SequenceB_SubSafekeepingAccount._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PlaceOfSafekeeping_L'), MT535_SequenceB_SubSafekeepingAccount_94F_Type, scope=MT535_SequenceB_SubSafekeepingAccount, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1305, 4)))

MT535_SequenceB_SubSafekeepingAccount._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ActivityFlag'), MT535_SequenceB_SubSafekeepingAccount_17B_Type, scope=MT535_SequenceB_SubSafekeepingAccount, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1307, 3)))

MT535_SequenceB_SubSafekeepingAccount._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SubsequenceB1_FinancialInstrument'), MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument, scope=MT535_SequenceB_SubSafekeepingAccount, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1308, 3)))

def _BuildAutomaton_2 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_2
    del _BuildAutomaton_2
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1292, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1293, 4))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1294, 4))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1295, 4))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1297, 3))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1298, 4))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1299, 4))
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1301, 3))
    counters.add(cc_7)
    cc_8 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1302, 4))
    counters.add(cc_8)
    cc_9 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1303, 4))
    counters.add(cc_9)
    cc_10 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1304, 4))
    counters.add(cc_10)
    cc_11 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1305, 4))
    counters.add(cc_11)
    cc_12 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1307, 3))
    counters.add(cc_12)
    cc_13 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1308, 3))
    counters.add(cc_13)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(MT535_SequenceB_SubSafekeepingAccount._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Party_L')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1293, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(MT535_SequenceB_SubSafekeepingAccount._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Party_P')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1294, 4))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(MT535_SequenceB_SubSafekeepingAccount._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Party_R')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1295, 4))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    final_update.add(fac.UpdateInstruction(cc_5, False))
    symbol = pyxb.binding.content.ElementUse(MT535_SequenceB_SubSafekeepingAccount._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SafekeepingAccount_A')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1298, 4))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    final_update.add(fac.UpdateInstruction(cc_6, False))
    symbol = pyxb.binding.content.ElementUse(MT535_SequenceB_SubSafekeepingAccount._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SafekeepingAccount_B')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1299, 4))
    st_4 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_7, False))
    final_update.add(fac.UpdateInstruction(cc_8, False))
    symbol = pyxb.binding.content.ElementUse(MT535_SequenceB_SubSafekeepingAccount._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PlaceOfSafekeeping_B')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1302, 4))
    st_5 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_7, False))
    final_update.add(fac.UpdateInstruction(cc_9, False))
    symbol = pyxb.binding.content.ElementUse(MT535_SequenceB_SubSafekeepingAccount._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PlaceOfSafekeeping_C')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1303, 4))
    st_6 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_7, False))
    final_update.add(fac.UpdateInstruction(cc_10, False))
    symbol = pyxb.binding.content.ElementUse(MT535_SequenceB_SubSafekeepingAccount._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PlaceOfSafekeeping_F')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1304, 4))
    st_7 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_7, False))
    final_update.add(fac.UpdateInstruction(cc_11, False))
    symbol = pyxb.binding.content.ElementUse(MT535_SequenceB_SubSafekeepingAccount._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PlaceOfSafekeeping_L')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1305, 4))
    st_8 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_12, False))
    symbol = pyxb.binding.content.ElementUse(MT535_SequenceB_SubSafekeepingAccount._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ActivityFlag')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1307, 3))
    st_9 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_13, False))
    symbol = pyxb.binding.content.ElementUse(MT535_SequenceB_SubSafekeepingAccount._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SubsequenceB1_FinancialInstrument')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1308, 3))
    st_10 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_10)
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
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_7, True),
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_8, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_7, True),
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_7, True),
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_7, True),
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_7, False),
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_7, False),
        fac.UpdateInstruction(cc_8, False) ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_7, True),
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_7, True),
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_9, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_7, True),
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_7, True),
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_7, False),
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_7, False),
        fac.UpdateInstruction(cc_9, False) ]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_7, True),
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_7, True),
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_7, True),
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_10, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_7, True),
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_7, False),
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_7, False),
        fac.UpdateInstruction(cc_10, False) ]))
    st_7._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_7, True),
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_7, True),
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_7, True),
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_7, True),
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_11, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_7, False),
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_7, False),
        fac.UpdateInstruction(cc_11, False) ]))
    st_8._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_12, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_12, False) ]))
    st_9._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_13, True) ]))
    st_10._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
MT535_SequenceB_SubSafekeepingAccount._Automaton = _BuildAutomaton_2()




MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'IdentificationOfFinancialInstrument'), MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_35B_Type, scope=MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1316, 3)))

MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SubsequenceB1a_FinancialInstrumentAttributes'), MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes, scope=MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1317, 3)))

MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'CorporateActionOptionCodeIndicator'), MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_22H_Type, scope=MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1318, 3)))

MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Price_A'), MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_90A_Type, scope=MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1320, 4)))

MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Price_B'), MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_90B_Type, scope=MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1321, 4)))

MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Price_E'), MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_90E_Type, scope=MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1322, 4)))

MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SourceOfPrice'), MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_94B_Type, scope=MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1324, 3)))

MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PriceQuotationDateTime_A'), MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_98A_Type, scope=MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1326, 4)))

MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PriceQuotationDateTime_C'), MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_98C_Type, scope=MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1327, 4)))

MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Balance'), MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_93B_Type, scope=MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1329, 3)))

MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SubsequenceB1b_Subbalance'), MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance, scope=MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1330, 3)))

MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'NumberofDaysAccrued'), MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_99A_Type, scope=MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1331, 3)))

MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Amount'), MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_19A_Type, scope=MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1332, 3)))

MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ExchangeRate'), MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_92B_Type, scope=MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1333, 3)))

MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'HoldingsNarrative'), MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_70E_Type, scope=MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1334, 3)))

MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SubsequenceB1c_QuantityBreakdown'), MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown, scope=MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1335, 3)))

def _BuildAutomaton_3 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_3
    del _BuildAutomaton_3
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1317, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1318, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1319, 3))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1320, 4))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1321, 4))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1322, 4))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1324, 3))
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1325, 3))
    counters.add(cc_7)
    cc_8 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1326, 4))
    counters.add(cc_8)
    cc_9 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1327, 4))
    counters.add(cc_9)
    cc_10 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1330, 3))
    counters.add(cc_10)
    cc_11 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1331, 3))
    counters.add(cc_11)
    cc_12 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1332, 3))
    counters.add(cc_12)
    cc_13 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1333, 3))
    counters.add(cc_13)
    cc_14 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1334, 3))
    counters.add(cc_14)
    cc_15 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1335, 3))
    counters.add(cc_15)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'IdentificationOfFinancialInstrument')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1316, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SubsequenceB1a_FinancialInstrumentAttributes')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1317, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'CorporateActionOptionCodeIndicator')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1318, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Price_A')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1320, 4))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Price_B')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1321, 4))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Price_E')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1322, 4))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SourceOfPrice')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1324, 3))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PriceQuotationDateTime_A')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1326, 4))
    st_7 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PriceQuotationDateTime_C')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1327, 4))
    st_8 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Balance')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1329, 3))
    st_9 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_10, False))
    symbol = pyxb.binding.content.ElementUse(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SubsequenceB1b_Subbalance')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1330, 3))
    st_10 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_10)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_11, False))
    symbol = pyxb.binding.content.ElementUse(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'NumberofDaysAccrued')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1331, 3))
    st_11 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_11)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_12, False))
    symbol = pyxb.binding.content.ElementUse(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Amount')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1332, 3))
    st_12 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_12)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_13, False))
    symbol = pyxb.binding.content.ElementUse(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ExchangeRate')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1333, 3))
    st_13 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_13)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_14, False))
    symbol = pyxb.binding.content.ElementUse(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'HoldingsNarrative')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1334, 3))
    st_14 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_14)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_15, False))
    symbol = pyxb.binding.content.ElementUse(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SubsequenceB1c_QuantityBreakdown')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1335, 3))
    st_15 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_15)
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
    transitions.append(fac.Transition(st_9, [
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
    transitions.append(fac.Transition(st_9, [
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
    transitions.append(fac.Transition(st_9, [
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
    transitions.append(fac.Transition(st_9, [
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
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_2, False),
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
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_7, False),
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
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_7, False),
        fac.UpdateInstruction(cc_9, False) ]))
    st_8._set_transitionSet(transitions)
    transitions = []
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
    st_9._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_10, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_10, False) ]))
    st_10._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_11, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_11, False) ]))
    st_11._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_12, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_12, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_12, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_12, False) ]))
    st_12._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_13, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_13, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_13, False) ]))
    st_13._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_14, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_14, False) ]))
    st_14._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_15, True) ]))
    st_15._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument._Automaton = _BuildAutomaton_3()




MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Place_B'), MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_94B_Type, scope=MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1344, 4)))

MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Place_D'), MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_94D_Type, scope=MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1345, 4)))

MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Indicator'), MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_22F_Type, scope=MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1347, 3)))

MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'TypeOfFinancialInstrument_A'), MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_12A_Type, scope=MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1349, 4)))

MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'TypeOfFinancialInstrument_B'), MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_12B_Type, scope=MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1350, 4)))

MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'TypeOfFinancialInstrument_C'), MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_12C_Type, scope=MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1351, 4)))

MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'CurrencyOfDenomination'), MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_11A_Type, scope=MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1353, 3)))

MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DateTime'), MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_98A_Type, scope=MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1354, 3)))

MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Rate'), MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_92A_Type, scope=MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1355, 3)))

MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'NumberIdentification_A'), MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_13A_Type, scope=MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1357, 4)))

MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'NumberIdentification_B'), MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_13B_Type, scope=MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1358, 4)))

MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'NumberIdentification_K'), MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_13K_Type, scope=MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1359, 4)))

MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Flag'), MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_17B_Type, scope=MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1361, 3)))

MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Price_A'), MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_90A_Type, scope=MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1363, 4)))

MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Price_B'), MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_90B_Type, scope=MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1364, 4)))

MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'QuantityOfFinancialInstrument'), MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_36B_Type, scope=MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1366, 3)))

MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'IdentificationOfFinancialInstrument'), MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_35B_Type, scope=MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1367, 3)))

MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'FinancialInstrumentAttributeNarrative'), MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes_70E_Type, scope=MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1368, 3)))

def _BuildAutomaton_4 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_4
    del _BuildAutomaton_4
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1343, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1344, 4))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1345, 4))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1347, 3))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1348, 3))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1349, 4))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1350, 4))
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1351, 4))
    counters.add(cc_7)
    cc_8 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1353, 3))
    counters.add(cc_8)
    cc_9 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1354, 3))
    counters.add(cc_9)
    cc_10 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1355, 3))
    counters.add(cc_10)
    cc_11 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1356, 3))
    counters.add(cc_11)
    cc_12 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1357, 4))
    counters.add(cc_12)
    cc_13 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1358, 4))
    counters.add(cc_13)
    cc_14 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1359, 4))
    counters.add(cc_14)
    cc_15 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1361, 3))
    counters.add(cc_15)
    cc_16 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1362, 3))
    counters.add(cc_16)
    cc_17 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1363, 4))
    counters.add(cc_17)
    cc_18 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1364, 4))
    counters.add(cc_18)
    cc_19 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1366, 3))
    counters.add(cc_19)
    cc_20 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1367, 3))
    counters.add(cc_20)
    cc_21 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1368, 3))
    counters.add(cc_21)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Place_B')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1344, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Place_D')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1345, 4))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Indicator')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1347, 3))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    final_update.add(fac.UpdateInstruction(cc_5, False))
    symbol = pyxb.binding.content.ElementUse(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'TypeOfFinancialInstrument_A')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1349, 4))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    final_update.add(fac.UpdateInstruction(cc_6, False))
    symbol = pyxb.binding.content.ElementUse(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'TypeOfFinancialInstrument_B')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1350, 4))
    st_4 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    final_update.add(fac.UpdateInstruction(cc_7, False))
    symbol = pyxb.binding.content.ElementUse(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'TypeOfFinancialInstrument_C')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1351, 4))
    st_5 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_8, False))
    symbol = pyxb.binding.content.ElementUse(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'CurrencyOfDenomination')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1353, 3))
    st_6 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_9, False))
    symbol = pyxb.binding.content.ElementUse(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'DateTime')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1354, 3))
    st_7 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_10, False))
    symbol = pyxb.binding.content.ElementUse(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Rate')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1355, 3))
    st_8 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_11, False))
    final_update.add(fac.UpdateInstruction(cc_12, False))
    symbol = pyxb.binding.content.ElementUse(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'NumberIdentification_A')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1357, 4))
    st_9 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_11, False))
    final_update.add(fac.UpdateInstruction(cc_13, False))
    symbol = pyxb.binding.content.ElementUse(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'NumberIdentification_B')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1358, 4))
    st_10 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_10)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_11, False))
    final_update.add(fac.UpdateInstruction(cc_14, False))
    symbol = pyxb.binding.content.ElementUse(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'NumberIdentification_K')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1359, 4))
    st_11 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_11)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_15, False))
    symbol = pyxb.binding.content.ElementUse(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Flag')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1361, 3))
    st_12 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_12)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_16, False))
    final_update.add(fac.UpdateInstruction(cc_17, False))
    symbol = pyxb.binding.content.ElementUse(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Price_A')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1363, 4))
    st_13 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_13)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_16, False))
    final_update.add(fac.UpdateInstruction(cc_18, False))
    symbol = pyxb.binding.content.ElementUse(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Price_B')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1364, 4))
    st_14 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_14)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_19, False))
    symbol = pyxb.binding.content.ElementUse(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'QuantityOfFinancialInstrument')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1366, 3))
    st_15 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_15)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_20, False))
    symbol = pyxb.binding.content.ElementUse(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'IdentificationOfFinancialInstrument')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1367, 3))
    st_16 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_16)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_21, False))
    symbol = pyxb.binding.content.ElementUse(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'FinancialInstrumentAttributeNarrative')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1368, 3))
    st_17 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_17)
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
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_17, [
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
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_2, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_3, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_3, False) ]))
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
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_17, [
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
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_8, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_8, False) ]))
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
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_8, False) ]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_9, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_9, False) ]))
    st_7._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_10, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_10, False) ]))
    st_8._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_11, True),
        fac.UpdateInstruction(cc_12, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_12, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_11, True),
        fac.UpdateInstruction(cc_12, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_11, True),
        fac.UpdateInstruction(cc_12, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_11, False),
        fac.UpdateInstruction(cc_12, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_11, False),
        fac.UpdateInstruction(cc_12, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_11, False),
        fac.UpdateInstruction(cc_12, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_11, False),
        fac.UpdateInstruction(cc_12, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_11, False),
        fac.UpdateInstruction(cc_12, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_11, False),
        fac.UpdateInstruction(cc_12, False) ]))
    st_9._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_11, True),
        fac.UpdateInstruction(cc_13, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_11, True),
        fac.UpdateInstruction(cc_13, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_13, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_11, True),
        fac.UpdateInstruction(cc_13, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_11, False),
        fac.UpdateInstruction(cc_13, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_11, False),
        fac.UpdateInstruction(cc_13, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_11, False),
        fac.UpdateInstruction(cc_13, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_11, False),
        fac.UpdateInstruction(cc_13, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_11, False),
        fac.UpdateInstruction(cc_13, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_11, False),
        fac.UpdateInstruction(cc_13, False) ]))
    st_10._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_11, True),
        fac.UpdateInstruction(cc_14, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_11, True),
        fac.UpdateInstruction(cc_14, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_11, True),
        fac.UpdateInstruction(cc_14, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_14, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_11, False),
        fac.UpdateInstruction(cc_14, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_11, False),
        fac.UpdateInstruction(cc_14, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_11, False),
        fac.UpdateInstruction(cc_14, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_11, False),
        fac.UpdateInstruction(cc_14, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_11, False),
        fac.UpdateInstruction(cc_14, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_11, False),
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
    st_12._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_16, True),
        fac.UpdateInstruction(cc_17, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_17, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_16, True),
        fac.UpdateInstruction(cc_17, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_16, False),
        fac.UpdateInstruction(cc_17, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_16, False),
        fac.UpdateInstruction(cc_17, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_16, False),
        fac.UpdateInstruction(cc_17, False) ]))
    st_13._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_16, True),
        fac.UpdateInstruction(cc_18, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_16, True),
        fac.UpdateInstruction(cc_18, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_18, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_16, False),
        fac.UpdateInstruction(cc_18, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_16, False),
        fac.UpdateInstruction(cc_18, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_16, False),
        fac.UpdateInstruction(cc_18, False) ]))
    st_14._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_19, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_19, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_19, False) ]))
    st_15._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_20, True) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_20, False) ]))
    st_16._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_21, True) ]))
    st_17._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1a_FinancialInstrumentAttributes._Automaton = _BuildAutomaton_4()




MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Balance_B'), MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_93B_Type, scope=MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1377, 4)))

MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Balance_C'), MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_93C_Type, scope=MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1378, 4)))

MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ExposureTypeIndicator_F'), MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_22F_Type, scope=MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1381, 4)))

MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ExposureTypeIndicator_H'), MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_22H_Type, scope=MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1382, 4)))

MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Place_B'), MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_94B_Type, scope=MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1385, 4)))

MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Place_C'), MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_94C_Type, scope=MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1386, 4)))

MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Place_F'), MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_94F_Type, scope=MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1387, 4)))

MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Place_L'), MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_94F_Type, scope=MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1388, 4)))

MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Price_A'), MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_90A_Type, scope=MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1391, 4)))

MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Price_B'), MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_90B_Type, scope=MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1392, 4)))

MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Price_E'), MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_90E_Type, scope=MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1393, 4)))

MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PriceQuotationDateTime_A'), MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_98A_Type, scope=MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1396, 4)))

MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PriceQuotationDateTime_C'), MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_98C_Type, scope=MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1397, 4)))

MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'NumberOfDaysAccrued'), MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_99A_Type, scope=MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1399, 3)))

MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Amount'), MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_19A_Type, scope=MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1400, 3)))

MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ExchangeRate'), MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_92B_Type, scope=MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1401, 3)))

MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SubbalanceDetailsNarrative'), MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_70C_Type, scope=MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1402, 3)))

MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SubsequenceB1b1_QuantityBreakdown'), MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown, scope=MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1403, 3)))

def _BuildAutomaton_5 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_5
    del _BuildAutomaton_5
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1380, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1381, 4))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1382, 4))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1384, 3))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1385, 4))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1386, 4))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1387, 4))
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1388, 4))
    counters.add(cc_7)
    cc_8 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1390, 3))
    counters.add(cc_8)
    cc_9 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1391, 4))
    counters.add(cc_9)
    cc_10 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1392, 4))
    counters.add(cc_10)
    cc_11 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1393, 4))
    counters.add(cc_11)
    cc_12 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1395, 3))
    counters.add(cc_12)
    cc_13 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1396, 4))
    counters.add(cc_13)
    cc_14 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1397, 4))
    counters.add(cc_14)
    cc_15 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1399, 3))
    counters.add(cc_15)
    cc_16 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1400, 3))
    counters.add(cc_16)
    cc_17 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1401, 3))
    counters.add(cc_17)
    cc_18 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1402, 3))
    counters.add(cc_18)
    cc_19 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1403, 3))
    counters.add(cc_19)
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Balance_B')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1377, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Balance_C')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1378, 4))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ExposureTypeIndicator_F')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1381, 4))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ExposureTypeIndicator_H')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1382, 4))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Place_B')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1385, 4))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    final_update.add(fac.UpdateInstruction(cc_5, False))
    symbol = pyxb.binding.content.ElementUse(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Place_C')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1386, 4))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    final_update.add(fac.UpdateInstruction(cc_6, False))
    symbol = pyxb.binding.content.ElementUse(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Place_F')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1387, 4))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    final_update.add(fac.UpdateInstruction(cc_7, False))
    symbol = pyxb.binding.content.ElementUse(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Place_L')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1388, 4))
    st_7 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_8, False))
    final_update.add(fac.UpdateInstruction(cc_9, False))
    symbol = pyxb.binding.content.ElementUse(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Price_A')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1391, 4))
    st_8 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_8, False))
    final_update.add(fac.UpdateInstruction(cc_10, False))
    symbol = pyxb.binding.content.ElementUse(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Price_B')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1392, 4))
    st_9 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_8, False))
    final_update.add(fac.UpdateInstruction(cc_11, False))
    symbol = pyxb.binding.content.ElementUse(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Price_E')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1393, 4))
    st_10 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_10)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_12, False))
    final_update.add(fac.UpdateInstruction(cc_13, False))
    symbol = pyxb.binding.content.ElementUse(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PriceQuotationDateTime_A')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1396, 4))
    st_11 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_11)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_12, False))
    final_update.add(fac.UpdateInstruction(cc_14, False))
    symbol = pyxb.binding.content.ElementUse(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PriceQuotationDateTime_C')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1397, 4))
    st_12 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_12)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_15, False))
    symbol = pyxb.binding.content.ElementUse(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'NumberOfDaysAccrued')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1399, 3))
    st_13 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_13)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_16, False))
    symbol = pyxb.binding.content.ElementUse(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Amount')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1400, 3))
    st_14 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_14)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_17, False))
    symbol = pyxb.binding.content.ElementUse(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ExchangeRate')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1401, 3))
    st_15 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_15)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_18, False))
    symbol = pyxb.binding.content.ElementUse(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SubbalanceDetailsNarrative')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1402, 3))
    st_16 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_16)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_19, False))
    symbol = pyxb.binding.content.ElementUse(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SubsequenceB1b1_QuantityBreakdown')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1403, 3))
    st_17 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_17)
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
    transitions.append(fac.Transition(st_14, [
         ]))
    transitions.append(fac.Transition(st_15, [
         ]))
    transitions.append(fac.Transition(st_16, [
         ]))
    transitions.append(fac.Transition(st_17, [
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
    transitions.append(fac.Transition(st_14, [
         ]))
    transitions.append(fac.Transition(st_15, [
         ]))
    transitions.append(fac.Transition(st_16, [
         ]))
    transitions.append(fac.Transition(st_17, [
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
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_17, [
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
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_0, False),
        fac.UpdateInstruction(cc_2, False) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_3, True),
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_4, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_3, True),
        fac.UpdateInstruction(cc_4, False) ]))
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
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_3, False),
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_3, False),
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_3, False),
        fac.UpdateInstruction(cc_4, False) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_3, True),
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_3, True),
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_5, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_3, True),
        fac.UpdateInstruction(cc_5, False) ]))
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
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_3, False),
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_3, False),
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_3, False),
        fac.UpdateInstruction(cc_5, False) ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_3, True),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_3, True),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_3, True),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_6, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_3, True),
        fac.UpdateInstruction(cc_6, False) ]))
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
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_3, False),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_3, False),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_3, False),
        fac.UpdateInstruction(cc_6, False) ]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_3, True),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_3, True),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_3, True),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_3, True),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_7, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_3, False),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_3, False),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_3, False),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_3, False),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_3, False),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_3, False),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_3, False),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_3, False),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_3, False),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_3, False),
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
    st_12._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_15, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_15, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_15, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_15, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_15, False) ]))
    st_13._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_16, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_16, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_16, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_16, False) ]))
    st_14._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_17, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_17, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_17, False) ]))
    st_15._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_18, True) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_18, False) ]))
    st_16._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_19, True) ]))
    st_17._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance._Automaton = _BuildAutomaton_5()




MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'LotNumber'), MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_13B_Type, scope=MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1411, 3)))

MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'LotBalance'), MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_93B_Type, scope=MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1412, 3)))

MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'LotDateTime_A'), MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_98A_Type, scope=MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1414, 4)))

MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'LotDateTime_C'), MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_98C_Type, scope=MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1415, 4)))

MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'LotDateTime_E'), MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_98E_Type, scope=MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1416, 4)))

MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'BookLotPrice_A'), MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_90A_Type, scope=MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1419, 4)))

MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'BookLotPrice_B'), MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_90B_Type, scope=MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1420, 4)))

MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'TypeofPriceIndicator'), MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_22F_Type, scope=MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1422, 3)))

MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Amount'), MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown_19A_Type, scope=MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1423, 3)))

def _BuildAutomaton_6 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_6
    del _BuildAutomaton_6
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1411, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1412, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1413, 3))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1414, 4))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1415, 4))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1416, 4))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1418, 3))
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1419, 4))
    counters.add(cc_7)
    cc_8 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1420, 4))
    counters.add(cc_8)
    cc_9 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1422, 3))
    counters.add(cc_9)
    cc_10 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1423, 3))
    counters.add(cc_10)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'LotNumber')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1411, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'LotBalance')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1412, 3))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'LotDateTime_A')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1414, 4))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'LotDateTime_C')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1415, 4))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    final_update.add(fac.UpdateInstruction(cc_5, False))
    symbol = pyxb.binding.content.ElementUse(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'LotDateTime_E')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1416, 4))
    st_4 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_6, False))
    final_update.add(fac.UpdateInstruction(cc_7, False))
    symbol = pyxb.binding.content.ElementUse(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'BookLotPrice_A')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1419, 4))
    st_5 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_6, False))
    final_update.add(fac.UpdateInstruction(cc_8, False))
    symbol = pyxb.binding.content.ElementUse(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'BookLotPrice_B')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1420, 4))
    st_6 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_9, False))
    symbol = pyxb.binding.content.ElementUse(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'TypeofPriceIndicator')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1422, 3))
    st_7 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_10, False))
    symbol = pyxb.binding.content.ElementUse(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Amount')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1423, 3))
    st_8 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
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
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_9, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_9, False) ]))
    st_7._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_10, True) ]))
    st_8._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1b_Subbalance_SubsequenceB1b1_QuantityBreakdown._Automaton = _BuildAutomaton_6()




MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'LotNumber'), MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_13B_Type, scope=MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1431, 3)))

MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'LotBalance'), MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_93B_Type, scope=MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1432, 3)))

MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'LotDateTime_A'), MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_98A_Type, scope=MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1434, 4)))

MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'LotDateTime_C'), MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_98C_Type, scope=MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1435, 4)))

MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'LotDateTime_E'), MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_98E_Type, scope=MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1436, 4)))

MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'BookLotPrice_A'), MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_90A_Type, scope=MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1439, 4)))

MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'BookLotPrice_B'), MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_90B_Type, scope=MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1440, 4)))

MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'TypeofPriceIndicator'), MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_22F_Type, scope=MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1442, 3)))

MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Amount'), MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown_19A_Type, scope=MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1443, 3)))

def _BuildAutomaton_7 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_7
    del _BuildAutomaton_7
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1431, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1432, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1433, 3))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1434, 4))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1435, 4))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1436, 4))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1438, 3))
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1439, 4))
    counters.add(cc_7)
    cc_8 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1440, 4))
    counters.add(cc_8)
    cc_9 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1442, 3))
    counters.add(cc_9)
    cc_10 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1443, 3))
    counters.add(cc_10)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'LotNumber')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1431, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'LotBalance')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1432, 3))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'LotDateTime_A')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1434, 4))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'LotDateTime_C')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1435, 4))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    final_update.add(fac.UpdateInstruction(cc_5, False))
    symbol = pyxb.binding.content.ElementUse(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'LotDateTime_E')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1436, 4))
    st_4 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_6, False))
    final_update.add(fac.UpdateInstruction(cc_7, False))
    symbol = pyxb.binding.content.ElementUse(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'BookLotPrice_A')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1439, 4))
    st_5 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_6, False))
    final_update.add(fac.UpdateInstruction(cc_8, False))
    symbol = pyxb.binding.content.ElementUse(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'BookLotPrice_B')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1440, 4))
    st_6 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_9, False))
    symbol = pyxb.binding.content.ElementUse(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'TypeofPriceIndicator')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1442, 3))
    st_7 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_10, False))
    symbol = pyxb.binding.content.ElementUse(MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Amount')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1443, 3))
    st_8 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
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
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_9, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_9, False) ]))
    st_7._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_10, True) ]))
    st_8._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
MT535_SequenceB_SubSafekeepingAccount_SubsequenceB1_FinancialInstrument_SubsequenceB1c_QuantityBreakdown._Automaton = _BuildAutomaton_7()




MT535_SequenceC_AdditionalInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Party_P'), MT535_SequenceC_AdditionalInformation_95P_Type, scope=MT535_SequenceC_AdditionalInformation, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1452, 4)))

MT535_SequenceC_AdditionalInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Party_Q'), MT535_SequenceC_AdditionalInformation_95Q_Type, scope=MT535_SequenceC_AdditionalInformation, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1453, 4)))

MT535_SequenceC_AdditionalInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Party_R'), MT535_SequenceC_AdditionalInformation_95R_Type, scope=MT535_SequenceC_AdditionalInformation, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1454, 4)))

MT535_SequenceC_AdditionalInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Amount'), MT535_SequenceC_AdditionalInformation_19A_Type, scope=MT535_SequenceC_AdditionalInformation, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1456, 3)))

def _BuildAutomaton_8 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_8
    del _BuildAutomaton_8
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1451, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1452, 4))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1453, 4))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1454, 4))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1456, 3))
    counters.add(cc_4)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(MT535_SequenceC_AdditionalInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Party_P')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1452, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(MT535_SequenceC_AdditionalInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Party_Q')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1453, 4))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(MT535_SequenceC_AdditionalInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Party_R')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1454, 4))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(MT535_SequenceC_AdditionalInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Amount')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1456, 3))
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
        fac.UpdateInstruction(cc_0, True),
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
        fac.UpdateInstruction(cc_0, True),
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_3, [
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
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_4, True) ]))
    st_3._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
MT535_SequenceC_AdditionalInformation._Automaton = _BuildAutomaton_8()




CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SequenceA_GeneralInformation'), MT535_SequenceA_GeneralInformation, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1465, 4)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SequenceB_SubSafekeepingAccount'), MT535_SequenceB_SubSafekeepingAccount, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1466, 4)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SequenceC_AdditionalInformation'), MT535_SequenceC_AdditionalInformation, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1467, 4)))

def _BuildAutomaton_9 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_9
    del _BuildAutomaton_9
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1466, 4))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1467, 4))
    counters.add(cc_1)
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SequenceA_GeneralInformation')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1465, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SequenceB_SubSafekeepingAccount')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1466, 4))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SequenceC_AdditionalInformation')), pyxb.utils.utility.Location('C:\\Swift\\Templates\\MT535.xsd', 1467, 4))
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
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, True) ]))
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON._Automaton = _BuildAutomaton_9()


