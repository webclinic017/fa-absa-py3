
# C:\SWIFT\SwiftReader\XSD\MT598_170.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:96afad3d20bbfe8d040a1a097fa388d9fecd10e3
# Generated 2017-02-16 17:33:58.957000 by PyXB version 1.2.2
# Namespace http://www.w3schools.com

import pyxb
import pyxb.binding
import pyxb.binding.saxer
import StringIO
import pyxb.utils.utility
import pyxb.utils.domutils
import sys

# Unique identifier for bindings created at the same time
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:ff7bf6cf-f43f-11e6-8f0e-180373dbbcdf')

# Version of PyXB used to generate the bindings
_PyXBVersion = '1.2.6'
# Generated bindings are not compatible across PyXB versions
if pyxb.__version__ != _PyXBVersion:
    raise pyxb.PyXBVersionError(_PyXBVersion)

# Import bindings for namespaces imported into schema
import pyxb.binding.datatypes

# NOTE: All namespace declarations are reserved within the binding
Namespace = pyxb.namespace.NamespaceForURI('http://www.w3schools.com', create_if_missing=True)
Namespace.configureCategories(['typeBinding', 'elementBinding'])

def CreateFromDocument (xml_text, default_namespace=None, location_base=None):
    """Parse the given XML and use the document element to create a
    Python instance.
    
    @kw default_namespace The L{pyxb.Namespace} instance to use as the
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
        return CreateFromDOM(dom.documentElement)
    if default_namespace is None:
        default_namespace = Namespace.fallbackNamespace()
    saxer = pyxb.binding.saxer.make_parser(fallback_namespace=default_namespace, location_base=location_base)
    handler = saxer.getContentHandler()
    saxer.parse(StringIO.StringIO(xml_text))
    instance = handler.rootObject()
    return instance

def CreateFromDOM (node, default_namespace=None):
    """Create a Python instance from the given DOM node.
    The node tag must correspond to an element declaration in this module.

    @deprecated: Forcing use of DOM interface is unnecessary; use L{CreateFromDocument}."""
    if default_namespace is None:
        default_namespace = Namespace.fallbackNamespace()
    return pyxb.binding.basis.element.AnyCreateFromDOM(node, default_namespace)


# Atomic simple type: {http://www.w3schools.com}MT598_170_TRADDET_ALLOCDTLS_97B-SAFE_Type_Pattern
class MT598_170_TRADDET_ALLOCDTLS_97B_SAFE_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_170_TRADDET_ALLOCDTLS_97B-SAFE_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 3, 1)
    _Documentation = None
MT598_170_TRADDET_ALLOCDTLS_97B_SAFE_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT598_170_TRADDET_ALLOCDTLS_97B_SAFE_Type_Pattern._CF_pattern.addPattern(pattern='(:SAFE/STRA/IORT/[0-9]{8})')
MT598_170_TRADDET_ALLOCDTLS_97B_SAFE_Type_Pattern._InitializeFacetMap(MT598_170_TRADDET_ALLOCDTLS_97B_SAFE_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT598_170_TRADDET_ALLOCDTLS_97B-SAFE_Type_Pattern', MT598_170_TRADDET_ALLOCDTLS_97B_SAFE_Type_Pattern)

# Atomic simple type: {http://www.w3schools.com}MT598_170_TRADDET_FIA_98A-MATU_Type_Pattern
class MT598_170_TRADDET_FIA_98A_MATU_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_170_TRADDET_FIA_98A-MATU_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 15, 1)
    _Documentation = None
MT598_170_TRADDET_FIA_98A_MATU_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT598_170_TRADDET_FIA_98A_MATU_Type_Pattern._CF_pattern.addPattern(pattern='(:MATU//[0-9]{8})')
MT598_170_TRADDET_FIA_98A_MATU_Type_Pattern._InitializeFacetMap(MT598_170_TRADDET_FIA_98A_MATU_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT598_170_TRADDET_FIA_98A-MATU_Type_Pattern', MT598_170_TRADDET_FIA_98A_MATU_Type_Pattern)

# Atomic simple type: {http://www.w3schools.com}MT598_170_TRADDET_FIA_98A-COUP_Type_Pattern
class MT598_170_TRADDET_FIA_98A_COUP_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_170_TRADDET_FIA_98A-COUP_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 27, 1)
    _Documentation = None
MT598_170_TRADDET_FIA_98A_COUP_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT598_170_TRADDET_FIA_98A_COUP_Type_Pattern._CF_pattern.addPattern(pattern='(:COUP//[0-9]{8})')
MT598_170_TRADDET_FIA_98A_COUP_Type_Pattern._InitializeFacetMap(MT598_170_TRADDET_FIA_98A_COUP_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT598_170_TRADDET_FIA_98A-COUP_Type_Pattern', MT598_170_TRADDET_FIA_98A_COUP_Type_Pattern)

# Atomic simple type: {http://www.w3schools.com}MT598_170_TRADDET_ALLOCDTLS_19A-SETT_Type_Pattern
class MT598_170_TRADDET_ALLOCDTLS_19A_SETT_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_170_TRADDET_ALLOCDTLS_19A-SETT_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 39, 1)
    _Documentation = None
MT598_170_TRADDET_ALLOCDTLS_19A_SETT_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT598_170_TRADDET_ALLOCDTLS_19A_SETT_Type_Pattern._CF_pattern.addPattern(pattern='(:SETT//(N)?[A-Z]{3}[0-9]{1,12},([0-9]{1,2})*)')
MT598_170_TRADDET_ALLOCDTLS_19A_SETT_Type_Pattern._InitializeFacetMap(MT598_170_TRADDET_ALLOCDTLS_19A_SETT_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT598_170_TRADDET_ALLOCDTLS_19A-SETT_Type_Pattern', MT598_170_TRADDET_ALLOCDTLS_19A_SETT_Type_Pattern)

# Atomic simple type: {http://www.w3schools.com}MT598_170_TRADDET_98A-SETT_Type_Pattern
class MT598_170_TRADDET_98A_SETT_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_170_TRADDET_98A-SETT_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 51, 1)
    _Documentation = None
MT598_170_TRADDET_98A_SETT_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT598_170_TRADDET_98A_SETT_Type_Pattern._CF_pattern.addPattern(pattern='(:SETT//[0-9]{8})')
MT598_170_TRADDET_98A_SETT_Type_Pattern._InitializeFacetMap(MT598_170_TRADDET_98A_SETT_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT598_170_TRADDET_98A-SETT_Type_Pattern', MT598_170_TRADDET_98A_SETT_Type_Pattern)

# Atomic simple type: {http://www.w3schools.com}MT598_170_TRADDET_SETDET_22F_Type_Pattern
class MT598_170_TRADDET_SETDET_22F_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_170_TRADDET_SETDET_22F_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 63, 1)
    _Documentation = None
MT598_170_TRADDET_SETDET_22F_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT598_170_TRADDET_SETDET_22F_Type_Pattern._CF_pattern.addPattern(pattern='(:SETR/STRA/(XRFP|XRVP|XDFP|XDVP))')
MT598_170_TRADDET_SETDET_22F_Type_Pattern._InitializeFacetMap(MT598_170_TRADDET_SETDET_22F_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT598_170_TRADDET_SETDET_22F_Type_Pattern', MT598_170_TRADDET_SETDET_22F_Type_Pattern)

# Atomic simple type: {http://www.w3schools.com}MT598_170_TRADDET_70E_Type_Pattern
class MT598_170_TRADDET_70E_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_170_TRADDET_70E_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 75, 1)
    _Documentation = None
MT598_170_TRADDET_70E_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT598_170_TRADDET_70E_Type_Pattern._CF_pattern.addPattern(pattern='(:SPRO//)')
MT598_170_TRADDET_70E_Type_Pattern._InitializeFacetMap(MT598_170_TRADDET_70E_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT598_170_TRADDET_70E_Type_Pattern', MT598_170_TRADDET_70E_Type_Pattern)

# Atomic simple type: {http://www.w3schools.com}MT598_170_12_Type_Pattern
class MT598_170_12_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_170_12_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 87, 1)
    _Documentation = None
MT598_170_12_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT598_170_12_Type_Pattern._CF_pattern.addPattern(pattern='([0-9]{3})')
MT598_170_12_Type_Pattern._InitializeFacetMap(MT598_170_12_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT598_170_12_Type_Pattern', MT598_170_12_Type_Pattern)

# Atomic simple type: {http://www.w3schools.com}MT598_170_TRADDET_SETDET_SETPRTY_95R_Type_Pattern
class MT598_170_TRADDET_SETDET_SETPRTY_95R_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_170_TRADDET_SETDET_SETPRTY_95R_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 99, 1)
    _Documentation = None
MT598_170_TRADDET_SETDET_SETPRTY_95R_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT598_170_TRADDET_SETDET_SETPRTY_95R_Type_Pattern._CF_pattern.addPattern(pattern='(:(REAG|DEAG)/STRA/[A-Z]{2}[0-9]{6})')
MT598_170_TRADDET_SETDET_SETPRTY_95R_Type_Pattern._InitializeFacetMap(MT598_170_TRADDET_SETDET_SETPRTY_95R_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT598_170_TRADDET_SETDET_SETPRTY_95R_Type_Pattern', MT598_170_TRADDET_SETDET_SETPRTY_95R_Type_Pattern)

# Atomic simple type: {http://www.w3schools.com}MT598_170_TRADDET_35B_Type_Pattern
class MT598_170_TRADDET_35B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_170_TRADDET_35B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 111, 1)
    _Documentation = None
MT598_170_TRADDET_35B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT598_170_TRADDET_35B_Type_Pattern._CF_pattern.addPattern(pattern='(ISIN {1}[A-Z0-9]{12}(\\n)?((.{1,35}\\n?){1,1})?(\\n)?((.{1,35}\\n?){1,3})?)')
MT598_170_TRADDET_35B_Type_Pattern._InitializeFacetMap(MT598_170_TRADDET_35B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT598_170_TRADDET_35B_Type_Pattern', MT598_170_TRADDET_35B_Type_Pattern)

# Atomic simple type: {http://www.w3schools.com}MT598_170_GENL_98C_Type_Pattern
class MT598_170_GENL_98C_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_170_GENL_98C_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 123, 1)
    _Documentation = None
MT598_170_GENL_98C_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT598_170_GENL_98C_Type_Pattern._CF_pattern.addPattern(pattern='(:PREP//[0-9]{8}[0-9]{6})')
MT598_170_GENL_98C_Type_Pattern._InitializeFacetMap(MT598_170_GENL_98C_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT598_170_GENL_98C_Type_Pattern', MT598_170_GENL_98C_Type_Pattern)

# Atomic simple type: {http://www.w3schools.com}MT598_170_TRADDET_20C-TRRF_Type_Pattern
class MT598_170_TRADDET_20C_TRRF_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_170_TRADDET_20C-TRRF_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 135, 1)
    _Documentation = None
MT598_170_TRADDET_20C_TRRF_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT598_170_TRADDET_20C_TRRF_Type_Pattern._CF_pattern.addPattern(pattern='(:TRRF//[A-Z]{2}[0-9]{6}/[0-9]{1,7})')
MT598_170_TRADDET_20C_TRRF_Type_Pattern._InitializeFacetMap(MT598_170_TRADDET_20C_TRRF_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT598_170_TRADDET_20C-TRRF_Type_Pattern', MT598_170_TRADDET_20C_TRRF_Type_Pattern)

# Atomic simple type: {http://www.w3schools.com}MT598_170_GENL_23G_Type_Pattern
class MT598_170_GENL_23G_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_170_GENL_23G_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 147, 1)
    _Documentation = None
MT598_170_GENL_23G_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT598_170_GENL_23G_Type_Pattern._CF_pattern.addPattern(pattern='((NEWM|CANC))')
MT598_170_GENL_23G_Type_Pattern._InitializeFacetMap(MT598_170_GENL_23G_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT598_170_GENL_23G_Type_Pattern', MT598_170_GENL_23G_Type_Pattern)

# Atomic simple type: {http://www.w3schools.com}MT598_170_TRADDET_FIA_92A_Type_Pattern
class MT598_170_TRADDET_FIA_92A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_170_TRADDET_FIA_92A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 159, 1)
    _Documentation = None
MT598_170_TRADDET_FIA_92A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT598_170_TRADDET_FIA_92A_Type_Pattern._CF_pattern.addPattern(pattern='(:INTR//(N)?[0-9]{1,12},([0-9]{1,2})*)')
MT598_170_TRADDET_FIA_92A_Type_Pattern._InitializeFacetMap(MT598_170_TRADDET_FIA_92A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT598_170_TRADDET_FIA_92A_Type_Pattern', MT598_170_TRADDET_FIA_92A_Type_Pattern)

# Atomic simple type: {http://www.w3schools.com}MT598_170_TRADDET_SETDET_AMT_19A_Type_Pattern
class MT598_170_TRADDET_SETDET_AMT_19A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_170_TRADDET_SETDET_AMT_19A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 171, 1)
    _Documentation = None
MT598_170_TRADDET_SETDET_AMT_19A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT598_170_TRADDET_SETDET_AMT_19A_Type_Pattern._CF_pattern.addPattern(pattern='(:BULK//(N)?[A-Z]{3}[0-9]{1,12},([0-9]{1,2})*)')
MT598_170_TRADDET_SETDET_AMT_19A_Type_Pattern._InitializeFacetMap(MT598_170_TRADDET_SETDET_AMT_19A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT598_170_TRADDET_SETDET_AMT_19A_Type_Pattern', MT598_170_TRADDET_SETDET_AMT_19A_Type_Pattern)

# Atomic simple type: {http://www.w3schools.com}MT598_170_TRADDET_ALLOCDTLS_36B_Type_Pattern
class MT598_170_TRADDET_ALLOCDTLS_36B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_170_TRADDET_ALLOCDTLS_36B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 183, 1)
    _Documentation = None
MT598_170_TRADDET_ALLOCDTLS_36B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT598_170_TRADDET_ALLOCDTLS_36B_Type_Pattern._CF_pattern.addPattern(pattern='(:SETT//FAMT/[0-9]{1,12},([0-9]{1,2})*)')
MT598_170_TRADDET_ALLOCDTLS_36B_Type_Pattern._InitializeFacetMap(MT598_170_TRADDET_ALLOCDTLS_36B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT598_170_TRADDET_ALLOCDTLS_36B_Type_Pattern', MT598_170_TRADDET_ALLOCDTLS_36B_Type_Pattern)

# Atomic simple type: {http://www.w3schools.com}MT598_170_20_Type_Pattern
class MT598_170_20_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_170_20_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 195, 1)
    _Documentation = None
MT598_170_20_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT598_170_20_Type_Pattern._CF_pattern.addPattern(pattern='(.{1,16})')
MT598_170_20_Type_Pattern._InitializeFacetMap(MT598_170_20_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT598_170_20_Type_Pattern', MT598_170_20_Type_Pattern)

# Atomic simple type: {http://www.w3schools.com}MT598_170_TRADDET_FIA_98A-FRNR_Type_Pattern
class MT598_170_TRADDET_FIA_98A_FRNR_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_170_TRADDET_FIA_98A-FRNR_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 207, 1)
    _Documentation = None
MT598_170_TRADDET_FIA_98A_FRNR_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT598_170_TRADDET_FIA_98A_FRNR_Type_Pattern._CF_pattern.addPattern(pattern='(:FRNR//[0-9]{8})')
MT598_170_TRADDET_FIA_98A_FRNR_Type_Pattern._InitializeFacetMap(MT598_170_TRADDET_FIA_98A_FRNR_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT598_170_TRADDET_FIA_98A-FRNR_Type_Pattern', MT598_170_TRADDET_FIA_98A_FRNR_Type_Pattern)

# Atomic simple type: {http://www.w3schools.com}MT598_170_TRADDET_SETDET_REPO_19A_Type_Pattern
class MT598_170_TRADDET_SETDET_REPO_19A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_170_TRADDET_SETDET_REPO_19A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 219, 1)
    _Documentation = None
MT598_170_TRADDET_SETDET_REPO_19A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT598_170_TRADDET_SETDET_REPO_19A_Type_Pattern._CF_pattern.addPattern(pattern='(:TRTE//[A-Z]{3}[0-9]{1,12},([0-9]{1,2})*)')
MT598_170_TRADDET_SETDET_REPO_19A_Type_Pattern._InitializeFacetMap(MT598_170_TRADDET_SETDET_REPO_19A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT598_170_TRADDET_SETDET_REPO_19A_Type_Pattern', MT598_170_TRADDET_SETDET_REPO_19A_Type_Pattern)

# Atomic simple type: {http://www.w3schools.com}MT598_170_TRADDET_ALLOCDTLS_19A-TRTE_Type_Pattern
class MT598_170_TRADDET_ALLOCDTLS_19A_TRTE_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_170_TRADDET_ALLOCDTLS_19A-TRTE_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 231, 1)
    _Documentation = None
MT598_170_TRADDET_ALLOCDTLS_19A_TRTE_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT598_170_TRADDET_ALLOCDTLS_19A_TRTE_Type_Pattern._CF_pattern.addPattern(pattern='(:TRTE//(N)?[A-Z]{3}[0-9]{1,12},([0-9]{1,2})*)')
MT598_170_TRADDET_ALLOCDTLS_19A_TRTE_Type_Pattern._InitializeFacetMap(MT598_170_TRADDET_ALLOCDTLS_19A_TRTE_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT598_170_TRADDET_ALLOCDTLS_19A-TRTE_Type_Pattern', MT598_170_TRADDET_ALLOCDTLS_19A_TRTE_Type_Pattern)

# Atomic simple type: {http://www.w3schools.com}MT598_170_TRADDET_98B-SETT_Type_Pattern
class MT598_170_TRADDET_98B_SETT_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_170_TRADDET_98B-SETT_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 243, 1)
    _Documentation = None
MT598_170_TRADDET_98B_SETT_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT598_170_TRADDET_98B_SETT_Type_Pattern._CF_pattern.addPattern(pattern='(:SETT//OPEN)')
MT598_170_TRADDET_98B_SETT_Type_Pattern._InitializeFacetMap(MT598_170_TRADDET_98B_SETT_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT598_170_TRADDET_98B-SETT_Type_Pattern', MT598_170_TRADDET_98B_SETT_Type_Pattern)

# Atomic simple type: {http://www.w3schools.com}MT598_170_TRADDET_98A-TRAD_Type_Pattern
class MT598_170_TRADDET_98A_TRAD_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_170_TRADDET_98A-TRAD_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 255, 1)
    _Documentation = None
MT598_170_TRADDET_98A_TRAD_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT598_170_TRADDET_98A_TRAD_Type_Pattern._CF_pattern.addPattern(pattern='(:TRAD//[0-9]{8})')
MT598_170_TRADDET_98A_TRAD_Type_Pattern._InitializeFacetMap(MT598_170_TRADDET_98A_TRAD_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT598_170_TRADDET_98A-TRAD_Type_Pattern', MT598_170_TRADDET_98A_TRAD_Type_Pattern)

# Atomic simple type: {http://www.w3schools.com}MT598_170_TRADDET_SETDET_AMT_36B_Type_Pattern
class MT598_170_TRADDET_SETDET_AMT_36B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_170_TRADDET_SETDET_AMT_36B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 267, 1)
    _Documentation = None
MT598_170_TRADDET_SETDET_AMT_36B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT598_170_TRADDET_SETDET_AMT_36B_Type_Pattern._CF_pattern.addPattern(pattern='(:BULK//FAMT/[0-9]{1,12},([0-9]{1,2})*)|(:TTUN//FAMT/[0-9]{1,12},([0-9]{1,2})*)')
MT598_170_TRADDET_SETDET_AMT_36B_Type_Pattern._InitializeFacetMap(MT598_170_TRADDET_SETDET_AMT_36B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT598_170_TRADDET_SETDET_AMT_36B_Type_Pattern', MT598_170_TRADDET_SETDET_AMT_36B_Type_Pattern)

# Atomic simple type: {http://www.w3schools.com}MT598_170_TRADDET_SETDET_REPO_98A-TERM_Type_Pattern
class MT598_170_TRADDET_SETDET_REPO_98A_TERM_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_170_TRADDET_SETDET_REPO_98A-TERM_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 286, 1)
    _Documentation = None
MT598_170_TRADDET_SETDET_REPO_98A_TERM_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT598_170_TRADDET_SETDET_REPO_98A_TERM_Type_Pattern._CF_pattern.addPattern(pattern='(:TERM//[0-9]{8})')
MT598_170_TRADDET_SETDET_REPO_98A_TERM_Type_Pattern._InitializeFacetMap(MT598_170_TRADDET_SETDET_REPO_98A_TERM_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT598_170_TRADDET_SETDET_REPO_98A-TERM_Type_Pattern', MT598_170_TRADDET_SETDET_REPO_98A_TERM_Type_Pattern)

# Atomic simple type: {http://www.w3schools.com}MT598_170_GENL_LINK_20C-RELA_Type_Pattern
class MT598_170_GENL_LINK_20C_RELA_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_170_GENL_LINK_20C-RELA_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 298, 1)
    _Documentation = None
MT598_170_GENL_LINK_20C_RELA_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT598_170_GENL_LINK_20C_RELA_Type_Pattern._CF_pattern.addPattern(pattern='(:RELA//[A-Z]{2}[0-9]{6}/[0-9]{1,7})')
MT598_170_GENL_LINK_20C_RELA_Type_Pattern._InitializeFacetMap(MT598_170_GENL_LINK_20C_RELA_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT598_170_GENL_LINK_20C-RELA_Type_Pattern', MT598_170_GENL_LINK_20C_RELA_Type_Pattern)

# Complex type {http://www.w3schools.com}MT598_170_TRADDET_SETDET_REPO_98B-TERM_Type with content type SIMPLE
class MT598_170_TRADDET_SETDET_REPO_98B_TERM_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_170_TRADDET_SETDET_REPO_98B-TERM_Type with content type SIMPLE"""
    _TypeDefinition = pyxb.binding.datatypes.string
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_170_TRADDET_SETDET_REPO_98B-TERM_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 279, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.string
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_170_TRADDET_SETDET_REPO_98B_TERM_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='98B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 282, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 282, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_170_TRADDET_SETDET_REPO_98B-TERM_Type', MT598_170_TRADDET_SETDET_REPO_98B_TERM_Type)


# Complex type {http://www.w3schools.com}MT598_170_TRADDET_25D_Type with content type SIMPLE
class MT598_170_TRADDET_25D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_170_TRADDET_25D_Type with content type SIMPLE"""
    _TypeDefinition = pyxb.binding.datatypes.string
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_170_TRADDET_25D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 310, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.string
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_170_TRADDET_25D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='25D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 313, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 313, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_170_TRADDET_25D_Type', MT598_170_TRADDET_25D_Type)


# Complex type {http://www.w3schools.com}MT598_170_77E_Type with content type SIMPLE
class MT598_170_77E_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_170_77E_Type with content type SIMPLE"""
    _TypeDefinition = pyxb.binding.datatypes.string
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_170_77E_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 317, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.string
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_170_77E_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='77E')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 320, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 320, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_170_77E_Type', MT598_170_77E_Type)


# Complex type {http://www.w3schools.com}MT598_170_TRADDET_SETDET_SETPRTY with content type ELEMENT_ONLY
class MT598_170_TRADDET_SETDET_SETPRTY (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_170_TRADDET_SETDET_SETPRTY with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_170_TRADDET_SETDET_SETPRTY')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 324, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}ReceivingorDeliveringTradersCSDBPID uses Python identifier ReceivingorDeliveringTradersCSDBPID
    __ReceivingorDeliveringTradersCSDBPID = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ReceivingorDeliveringTradersCSDBPID'), 'ReceivingorDeliveringTradersCSDBPID', '__httpwww_w3schools_com_MT598_170_TRADDET_SETDET_SETPRTY_httpwww_w3schools_comReceivingorDeliveringTradersCSDBPID', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 326, 3), )

    
    ReceivingorDeliveringTradersCSDBPID = property(__ReceivingorDeliveringTradersCSDBPID.value, __ReceivingorDeliveringTradersCSDBPID.set, None, None)

    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_170_TRADDET_SETDET_SETPRTY_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='16R')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 328, 2)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 328, 2)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        __ReceivingorDeliveringTradersCSDBPID.name() : __ReceivingorDeliveringTradersCSDBPID
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_170_TRADDET_SETDET_SETPRTY', MT598_170_TRADDET_SETDET_SETPRTY)


# Complex type {http://www.w3schools.com}MT598_170_TRADDET_SETDET_REPO with content type ELEMENT_ONLY
class MT598_170_TRADDET_SETDET_REPO (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_170_TRADDET_SETDET_REPO with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_170_TRADDET_SETDET_REPO')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 330, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}RepurchaseDateFixed uses Python identifier RepurchaseDateFixed
    __RepurchaseDateFixed = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'RepurchaseDateFixed'), 'RepurchaseDateFixed', '__httpwww_w3schools_com_MT598_170_TRADDET_SETDET_REPO_httpwww_w3schools_comRepurchaseDateFixed', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 332, 3), )

    
    RepurchaseDateFixed = property(__RepurchaseDateFixed.value, __RepurchaseDateFixed.set, None, None)

    
    # Element {http://www.w3schools.com}RepurchaseDateOpen uses Python identifier RepurchaseDateOpen
    __RepurchaseDateOpen = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'RepurchaseDateOpen'), 'RepurchaseDateOpen', '__httpwww_w3schools_com_MT598_170_TRADDET_SETDET_REPO_httpwww_w3schools_comRepurchaseDateOpen', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 333, 3), )

    
    RepurchaseDateOpen = property(__RepurchaseDateOpen.value, __RepurchaseDateOpen.set, None, None)

    
    # Element {http://www.w3schools.com}RepurchaseAmount uses Python identifier RepurchaseAmount
    __RepurchaseAmount = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'RepurchaseAmount'), 'RepurchaseAmount', '__httpwww_w3schools_com_MT598_170_TRADDET_SETDET_REPO_httpwww_w3schools_comRepurchaseAmount', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 334, 3), )

    
    RepurchaseAmount = property(__RepurchaseAmount.value, __RepurchaseAmount.set, None, None)

    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_170_TRADDET_SETDET_REPO_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='16R')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 336, 2)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 336, 2)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        __RepurchaseDateFixed.name() : __RepurchaseDateFixed,
        __RepurchaseDateOpen.name() : __RepurchaseDateOpen,
        __RepurchaseAmount.name() : __RepurchaseAmount
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_170_TRADDET_SETDET_REPO', MT598_170_TRADDET_SETDET_REPO)


# Complex type {http://www.w3schools.com}MT598_170_TRADDET_SETDET_AMT with content type ELEMENT_ONLY
class MT598_170_TRADDET_SETDET_AMT (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_170_TRADDET_SETDET_AMT with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_170_TRADDET_SETDET_AMT')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 338, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}NominalValue uses Python identifier NominalValue
    __NominalValue = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'NominalValue'), 'NominalValue', '__httpwww_w3schools_com_MT598_170_TRADDET_SETDET_AMT_httpwww_w3schools_comNominalValue', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 340, 3), )

    
    NominalValue = property(__NominalValue.value, __NominalValue.set, None, None)

    
    # Element {http://www.w3schools.com}SettlementAmount uses Python identifier SettlementAmount
    __SettlementAmount = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SettlementAmount'), 'SettlementAmount', '__httpwww_w3schools_com_MT598_170_TRADDET_SETDET_AMT_httpwww_w3schools_comSettlementAmount', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 341, 3), )

    
    SettlementAmount = property(__SettlementAmount.value, __SettlementAmount.set, None, None)

    
    # Element {http://www.w3schools.com}TapTonUpNominalValue uses Python identifier TapTonUpNominalValue
    __TapTonUpNominalValue = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'TapTonUpNominalValue'), 'TapTonUpNominalValue', '__httpwww_w3schools_com_MT598_170_TRADDET_SETDET_AMT_httpwww_w3schools_comTapTonUpNominalValue', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 342, 3), )

    
    TapTonUpNominalValue = property(__TapTonUpNominalValue.value, __TapTonUpNominalValue.set, None, None)

    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_170_TRADDET_SETDET_AMT_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='16R')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 344, 2)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 344, 2)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        __NominalValue.name() : __NominalValue,
        __SettlementAmount.name() : __SettlementAmount,
        __TapTonUpNominalValue.name() : __TapTonUpNominalValue
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_170_TRADDET_SETDET_AMT', MT598_170_TRADDET_SETDET_AMT)


# Complex type {http://www.w3schools.com}MT598_170_TRADDET_FIA with content type ELEMENT_ONLY
class MT598_170_TRADDET_FIA (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_170_TRADDET_FIA with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_170_TRADDET_FIA')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 346, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}CurrentInterestRate uses Python identifier CurrentInterestRate
    __CurrentInterestRate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'CurrentInterestRate'), 'CurrentInterestRate', '__httpwww_w3schools_com_MT598_170_TRADDET_FIA_httpwww_w3schools_comCurrentInterestRate', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 348, 3), )

    
    CurrentInterestRate = property(__CurrentInterestRate.value, __CurrentInterestRate.set, None, None)

    
    # Element {http://www.w3schools.com}NextResetDate uses Python identifier NextResetDate
    __NextResetDate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'NextResetDate'), 'NextResetDate', '__httpwww_w3schools_com_MT598_170_TRADDET_FIA_httpwww_w3schools_comNextResetDate', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 349, 3), )

    
    NextResetDate = property(__NextResetDate.value, __NextResetDate.set, None, None)

    
    # Element {http://www.w3schools.com}MaturityDate uses Python identifier MaturityDate
    __MaturityDate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'MaturityDate'), 'MaturityDate', '__httpwww_w3schools_com_MT598_170_TRADDET_FIA_httpwww_w3schools_comMaturityDate', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 350, 3), )

    
    MaturityDate = property(__MaturityDate.value, __MaturityDate.set, None, None)

    
    # Element {http://www.w3schools.com}NextPaymentDate uses Python identifier NextPaymentDate
    __NextPaymentDate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'NextPaymentDate'), 'NextPaymentDate', '__httpwww_w3schools_com_MT598_170_TRADDET_FIA_httpwww_w3schools_comNextPaymentDate', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 351, 3), )

    
    NextPaymentDate = property(__NextPaymentDate.value, __NextPaymentDate.set, None, None)

    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_170_TRADDET_FIA_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='16R')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 353, 2)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 353, 2)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        __CurrentInterestRate.name() : __CurrentInterestRate,
        __NextResetDate.name() : __NextResetDate,
        __MaturityDate.name() : __MaturityDate,
        __NextPaymentDate.name() : __NextPaymentDate
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_170_TRADDET_FIA', MT598_170_TRADDET_FIA)


# Complex type {http://www.w3schools.com}MT598_170_TRADDET_ALLOCDTLS with content type ELEMENT_ONLY
class MT598_170_TRADDET_ALLOCDTLS (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_170_TRADDET_ALLOCDTLS with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_170_TRADDET_ALLOCDTLS')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 355, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}SORAccount uses Python identifier SORAccount
    __SORAccount = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SORAccount'), 'SORAccount', '__httpwww_w3schools_com_MT598_170_TRADDET_ALLOCDTLS_httpwww_w3schools_comSORAccount', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 357, 3), )

    
    SORAccount = property(__SORAccount.value, __SORAccount.set, None, None)

    
    # Element {http://www.w3schools.com}NominalValue uses Python identifier NominalValue
    __NominalValue = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'NominalValue'), 'NominalValue', '__httpwww_w3schools_com_MT598_170_TRADDET_ALLOCDTLS_httpwww_w3schools_comNominalValue', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 358, 3), )

    
    NominalValue = property(__NominalValue.value, __NominalValue.set, None, None)

    
    # Element {http://www.w3schools.com}SettlementAmount uses Python identifier SettlementAmount
    __SettlementAmount = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SettlementAmount'), 'SettlementAmount', '__httpwww_w3schools_com_MT598_170_TRADDET_ALLOCDTLS_httpwww_w3schools_comSettlementAmount', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 359, 3), )

    
    SettlementAmount = property(__SettlementAmount.value, __SettlementAmount.set, None, None)

    
    # Element {http://www.w3schools.com}RepurchaseAmount uses Python identifier RepurchaseAmount
    __RepurchaseAmount = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'RepurchaseAmount'), 'RepurchaseAmount', '__httpwww_w3schools_com_MT598_170_TRADDET_ALLOCDTLS_httpwww_w3schools_comRepurchaseAmount', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 360, 3), )

    
    RepurchaseAmount = property(__RepurchaseAmount.value, __RepurchaseAmount.set, None, None)

    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_170_TRADDET_ALLOCDTLS_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='16R')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 362, 2)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 362, 2)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        __SORAccount.name() : __SORAccount,
        __NominalValue.name() : __NominalValue,
        __SettlementAmount.name() : __SettlementAmount,
        __RepurchaseAmount.name() : __RepurchaseAmount
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_170_TRADDET_ALLOCDTLS', MT598_170_TRADDET_ALLOCDTLS)


# Complex type {http://www.w3schools.com}MT598_170_GENL_LINK with content type ELEMENT_ONLY
class MT598_170_GENL_LINK (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_170_GENL_LINK with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_170_GENL_LINK')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 364, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}InternalTradeReference uses Python identifier InternalTradeReference
    __InternalTradeReference = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'InternalTradeReference'), 'InternalTradeReference', '__httpwww_w3schools_com_MT598_170_GENL_LINK_httpwww_w3schools_comInternalTradeReference', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 366, 3), )

    
    InternalTradeReference = property(__InternalTradeReference.value, __InternalTradeReference.set, None, None)

    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_170_GENL_LINK_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='16R')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 368, 2)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 368, 2)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        __InternalTradeReference.name() : __InternalTradeReference
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_170_GENL_LINK', MT598_170_GENL_LINK)


# Complex type {http://www.w3schools.com}MT598_170_GENL with content type ELEMENT_ONLY
class MT598_170_GENL (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_170_GENL with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_170_GENL')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 370, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}FunctionOfMessage uses Python identifier FunctionOfMessage
    __FunctionOfMessage = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'FunctionOfMessage'), 'FunctionOfMessage', '__httpwww_w3schools_com_MT598_170_GENL_httpwww_w3schools_comFunctionOfMessage', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 372, 3), )

    
    FunctionOfMessage = property(__FunctionOfMessage.value, __FunctionOfMessage.set, None, None)

    
    # Element {http://www.w3schools.com}PreparationDateAndTime uses Python identifier PreparationDateAndTime
    __PreparationDateAndTime = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PreparationDateAndTime'), 'PreparationDateAndTime', '__httpwww_w3schools_com_MT598_170_GENL_httpwww_w3schools_comPreparationDateAndTime', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 373, 3), )

    
    PreparationDateAndTime = property(__PreparationDateAndTime.value, __PreparationDateAndTime.set, None, None)

    
    # Element {http://www.w3schools.com}LINK uses Python identifier LINK
    __LINK = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'LINK'), 'LINK', '__httpwww_w3schools_com_MT598_170_GENL_httpwww_w3schools_comLINK', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 374, 3), )

    
    LINK = property(__LINK.value, __LINK.set, None, None)

    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_170_GENL_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='16R')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 376, 2)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 376, 2)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        __FunctionOfMessage.name() : __FunctionOfMessage,
        __PreparationDateAndTime.name() : __PreparationDateAndTime,
        __LINK.name() : __LINK
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_170_GENL', MT598_170_GENL)


# Complex type {http://www.w3schools.com}MT598_170_TRADDET_SETDET with content type ELEMENT_ONLY
class MT598_170_TRADDET_SETDET (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_170_TRADDET_SETDET with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_170_TRADDET_SETDET')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 378, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}SettlementTransactionType uses Python identifier SettlementTransactionType
    __SettlementTransactionType = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SettlementTransactionType'), 'SettlementTransactionType', '__httpwww_w3schools_com_MT598_170_TRADDET_SETDET_httpwww_w3schools_comSettlementTransactionType', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 380, 3), )

    
    SettlementTransactionType = property(__SettlementTransactionType.value, __SettlementTransactionType.set, None, None)

    
    # Element {http://www.w3schools.com}SETPRTY uses Python identifier SETPRTY
    __SETPRTY = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SETPRTY'), 'SETPRTY', '__httpwww_w3schools_com_MT598_170_TRADDET_SETDET_httpwww_w3schools_comSETPRTY', True, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 381, 3), )

    
    SETPRTY = property(__SETPRTY.value, __SETPRTY.set, None, None)

    
    # Element {http://www.w3schools.com}AMT uses Python identifier AMT
    __AMT = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'AMT'), 'AMT', '__httpwww_w3schools_com_MT598_170_TRADDET_SETDET_httpwww_w3schools_comAMT', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 382, 3), )

    
    AMT = property(__AMT.value, __AMT.set, None, None)

    
    # Element {http://www.w3schools.com}REPO uses Python identifier REPO
    __REPO = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'REPO'), 'REPO', '__httpwww_w3schools_com_MT598_170_TRADDET_SETDET_httpwww_w3schools_comREPO', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 383, 3), )

    
    REPO = property(__REPO.value, __REPO.set, None, None)

    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_170_TRADDET_SETDET_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='16R')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 385, 2)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 385, 2)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        __SettlementTransactionType.name() : __SettlementTransactionType,
        __SETPRTY.name() : __SETPRTY,
        __AMT.name() : __AMT,
        __REPO.name() : __REPO
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_170_TRADDET_SETDET', MT598_170_TRADDET_SETDET)


# Complex type {http://www.w3schools.com}MT598_170_TRADDET with content type ELEMENT_ONLY
class MT598_170_TRADDET (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_170_TRADDET with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_170_TRADDET')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 387, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}InternalTradeReference uses Python identifier InternalTradeReference
    __InternalTradeReference = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'InternalTradeReference'), 'InternalTradeReference', '__httpwww_w3schools_com_MT598_170_TRADDET_httpwww_w3schools_comInternalTradeReference', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 389, 3), )

    
    InternalTradeReference = property(__InternalTradeReference.value, __InternalTradeReference.set, None, None)

    
    # Element {http://www.w3schools.com}TradeDate uses Python identifier TradeDate
    __TradeDate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'TradeDate'), 'TradeDate', '__httpwww_w3schools_com_MT598_170_TRADDET_httpwww_w3schools_comTradeDate', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 390, 3), )

    
    TradeDate = property(__TradeDate.value, __TradeDate.set, None, None)

    
    # Element {http://www.w3schools.com}SettlementDate uses Python identifier SettlementDate
    __SettlementDate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SettlementDate'), 'SettlementDate', '__httpwww_w3schools_com_MT598_170_TRADDET_httpwww_w3schools_comSettlementDate', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 391, 3), )

    
    SettlementDate = property(__SettlementDate.value, __SettlementDate.set, None, None)

    
    # Element {http://www.w3schools.com}SettlementDateOpen uses Python identifier SettlementDateOpen
    __SettlementDateOpen = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SettlementDateOpen'), 'SettlementDateOpen', '__httpwww_w3schools_com_MT598_170_TRADDET_httpwww_w3schools_comSettlementDateOpen', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 392, 3), )

    
    SettlementDateOpen = property(__SettlementDateOpen.value, __SettlementDateOpen.set, None, None)

    
    # Element {http://www.w3schools.com}IdentificationOfSecurities uses Python identifier IdentificationOfSecurities
    __IdentificationOfSecurities = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'IdentificationOfSecurities'), 'IdentificationOfSecurities', '__httpwww_w3schools_com_MT598_170_TRADDET_httpwww_w3schools_comIdentificationOfSecurities', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 393, 3), )

    
    IdentificationOfSecurities = property(__IdentificationOfSecurities.value, __IdentificationOfSecurities.set, None, None)

    
    # Element {http://www.w3schools.com}FIA uses Python identifier FIA
    __FIA = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'FIA'), 'FIA', '__httpwww_w3schools_com_MT598_170_TRADDET_httpwww_w3schools_comFIA', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 394, 3), )

    
    FIA = property(__FIA.value, __FIA.set, None, None)

    
    # Element {http://www.w3schools.com}AffirmationIndicator uses Python identifier AffirmationIndicator
    __AffirmationIndicator = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'AffirmationIndicator'), 'AffirmationIndicator', '__httpwww_w3schools_com_MT598_170_TRADDET_httpwww_w3schools_comAffirmationIndicator', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 395, 3), )

    
    AffirmationIndicator = property(__AffirmationIndicator.value, __AffirmationIndicator.set, None, None)

    
    # Element {http://www.w3schools.com}SettlementInstuctionProcessingNarrative uses Python identifier SettlementInstuctionProcessingNarrative
    __SettlementInstuctionProcessingNarrative = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SettlementInstuctionProcessingNarrative'), 'SettlementInstuctionProcessingNarrative', '__httpwww_w3schools_com_MT598_170_TRADDET_httpwww_w3schools_comSettlementInstuctionProcessingNarrative', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 396, 3), )

    
    SettlementInstuctionProcessingNarrative = property(__SettlementInstuctionProcessingNarrative.value, __SettlementInstuctionProcessingNarrative.set, None, None)

    
    # Element {http://www.w3schools.com}SETDET uses Python identifier SETDET
    __SETDET = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SETDET'), 'SETDET', '__httpwww_w3schools_com_MT598_170_TRADDET_httpwww_w3schools_comSETDET', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 397, 3), )

    
    SETDET = property(__SETDET.value, __SETDET.set, None, None)

    
    # Element {http://www.w3schools.com}ALLOCDTLS uses Python identifier ALLOCDTLS
    __ALLOCDTLS = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ALLOCDTLS'), 'ALLOCDTLS', '__httpwww_w3schools_com_MT598_170_TRADDET_httpwww_w3schools_comALLOCDTLS', True, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 398, 3), )

    
    ALLOCDTLS = property(__ALLOCDTLS.value, __ALLOCDTLS.set, None, None)

    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_170_TRADDET_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='16R')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 400, 2)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 400, 2)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        __InternalTradeReference.name() : __InternalTradeReference,
        __TradeDate.name() : __TradeDate,
        __SettlementDate.name() : __SettlementDate,
        __SettlementDateOpen.name() : __SettlementDateOpen,
        __IdentificationOfSecurities.name() : __IdentificationOfSecurities,
        __FIA.name() : __FIA,
        __AffirmationIndicator.name() : __AffirmationIndicator,
        __SettlementInstuctionProcessingNarrative.name() : __SettlementInstuctionProcessingNarrative,
        __SETDET.name() : __SETDET,
        __ALLOCDTLS.name() : __ALLOCDTLS
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_170_TRADDET', MT598_170_TRADDET)


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 403, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}TransactionReference uses Python identifier TransactionReference
    __TransactionReference = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'TransactionReference'), 'TransactionReference', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comTransactionReference', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 405, 4), )

    
    TransactionReference = property(__TransactionReference.value, __TransactionReference.set, None, None)

    
    # Element {http://www.w3schools.com}SubMessageType uses Python identifier SubMessageType
    __SubMessageType = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SubMessageType'), 'SubMessageType', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comSubMessageType', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 406, 4), )

    
    SubMessageType = property(__SubMessageType.value, __SubMessageType.set, None, None)

    
    # Element {http://www.w3schools.com}ProprietaryMessage uses Python identifier ProprietaryMessage
    __ProprietaryMessage = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ProprietaryMessage'), 'ProprietaryMessage', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comProprietaryMessage', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 407, 4), )

    
    ProprietaryMessage = property(__ProprietaryMessage.value, __ProprietaryMessage.set, None, None)

    
    # Element {http://www.w3schools.com}GENL uses Python identifier GENL
    __GENL = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'GENL'), 'GENL', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comGENL', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 408, 4), )

    
    GENL = property(__GENL.value, __GENL.set, None, None)

    
    # Element {http://www.w3schools.com}TRADDET uses Python identifier TRADDET
    __TRADDET = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'TRADDET'), 'TRADDET', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comTRADDET', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 409, 4), )

    
    TRADDET = property(__TRADDET.value, __TRADDET.set, None, None)

    _ElementMap.update({
        __TransactionReference.name() : __TransactionReference,
        __SubMessageType.name() : __SubMessageType,
        __ProprietaryMessage.name() : __ProprietaryMessage,
        __GENL.name() : __GENL,
        __TRADDET.name() : __TRADDET
    })
    _AttributeMap.update({
        
    })



# Complex type {http://www.w3schools.com}MT598_170_TRADDET_ALLOCDTLS_97B-SAFE_Type with content type SIMPLE
class MT598_170_TRADDET_ALLOCDTLS_97B_SAFE_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_170_TRADDET_ALLOCDTLS_97B-SAFE_Type with content type SIMPLE"""
    _TypeDefinition = MT598_170_TRADDET_ALLOCDTLS_97B_SAFE_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_170_TRADDET_ALLOCDTLS_97B-SAFE_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 8, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT598_170_TRADDET_ALLOCDTLS_97B_SAFE_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_170_TRADDET_ALLOCDTLS_97B_SAFE_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='97B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 11, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 11, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_170_TRADDET_ALLOCDTLS_97B-SAFE_Type', MT598_170_TRADDET_ALLOCDTLS_97B_SAFE_Type)


# Complex type {http://www.w3schools.com}MT598_170_TRADDET_FIA_98A-MATU_Type with content type SIMPLE
class MT598_170_TRADDET_FIA_98A_MATU_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_170_TRADDET_FIA_98A-MATU_Type with content type SIMPLE"""
    _TypeDefinition = MT598_170_TRADDET_FIA_98A_MATU_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_170_TRADDET_FIA_98A-MATU_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 20, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT598_170_TRADDET_FIA_98A_MATU_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_170_TRADDET_FIA_98A_MATU_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='98A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 23, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 23, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_170_TRADDET_FIA_98A-MATU_Type', MT598_170_TRADDET_FIA_98A_MATU_Type)


# Complex type {http://www.w3schools.com}MT598_170_TRADDET_FIA_98A-COUP_Type with content type SIMPLE
class MT598_170_TRADDET_FIA_98A_COUP_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_170_TRADDET_FIA_98A-COUP_Type with content type SIMPLE"""
    _TypeDefinition = MT598_170_TRADDET_FIA_98A_COUP_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_170_TRADDET_FIA_98A-COUP_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 32, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT598_170_TRADDET_FIA_98A_COUP_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_170_TRADDET_FIA_98A_COUP_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='98A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 35, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 35, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_170_TRADDET_FIA_98A-COUP_Type', MT598_170_TRADDET_FIA_98A_COUP_Type)


# Complex type {http://www.w3schools.com}MT598_170_TRADDET_ALLOCDTLS_19A-SETT_Type with content type SIMPLE
class MT598_170_TRADDET_ALLOCDTLS_19A_SETT_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_170_TRADDET_ALLOCDTLS_19A-SETT_Type with content type SIMPLE"""
    _TypeDefinition = MT598_170_TRADDET_ALLOCDTLS_19A_SETT_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_170_TRADDET_ALLOCDTLS_19A-SETT_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 44, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT598_170_TRADDET_ALLOCDTLS_19A_SETT_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_170_TRADDET_ALLOCDTLS_19A_SETT_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='19A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 47, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 47, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_170_TRADDET_ALLOCDTLS_19A-SETT_Type', MT598_170_TRADDET_ALLOCDTLS_19A_SETT_Type)


# Complex type {http://www.w3schools.com}MT598_170_TRADDET_98A-SETT_Type with content type SIMPLE
class MT598_170_TRADDET_98A_SETT_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_170_TRADDET_98A-SETT_Type with content type SIMPLE"""
    _TypeDefinition = MT598_170_TRADDET_98A_SETT_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_170_TRADDET_98A-SETT_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 56, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT598_170_TRADDET_98A_SETT_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_170_TRADDET_98A_SETT_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='98A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 59, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 59, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_170_TRADDET_98A-SETT_Type', MT598_170_TRADDET_98A_SETT_Type)


# Complex type {http://www.w3schools.com}MT598_170_TRADDET_SETDET_22F_Type with content type SIMPLE
class MT598_170_TRADDET_SETDET_22F_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_170_TRADDET_SETDET_22F_Type with content type SIMPLE"""
    _TypeDefinition = MT598_170_TRADDET_SETDET_22F_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_170_TRADDET_SETDET_22F_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 68, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT598_170_TRADDET_SETDET_22F_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_170_TRADDET_SETDET_22F_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='22F')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 71, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 71, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_170_TRADDET_SETDET_22F_Type', MT598_170_TRADDET_SETDET_22F_Type)


# Complex type {http://www.w3schools.com}MT598_170_TRADDET_70E_Type with content type SIMPLE
class MT598_170_TRADDET_70E_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_170_TRADDET_70E_Type with content type SIMPLE"""
    _TypeDefinition = MT598_170_TRADDET_70E_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_170_TRADDET_70E_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 80, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT598_170_TRADDET_70E_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_170_TRADDET_70E_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='70E')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 83, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 83, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_170_TRADDET_70E_Type', MT598_170_TRADDET_70E_Type)


# Complex type {http://www.w3schools.com}MT598_170_12_Type with content type SIMPLE
class MT598_170_12_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_170_12_Type with content type SIMPLE"""
    _TypeDefinition = MT598_170_12_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_170_12_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 92, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT598_170_12_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_170_12_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='12')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 95, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 95, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_170_12_Type', MT598_170_12_Type)


# Complex type {http://www.w3schools.com}MT598_170_TRADDET_SETDET_SETPRTY_95R_Type with content type SIMPLE
class MT598_170_TRADDET_SETDET_SETPRTY_95R_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_170_TRADDET_SETDET_SETPRTY_95R_Type with content type SIMPLE"""
    _TypeDefinition = MT598_170_TRADDET_SETDET_SETPRTY_95R_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_170_TRADDET_SETDET_SETPRTY_95R_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 104, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT598_170_TRADDET_SETDET_SETPRTY_95R_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_170_TRADDET_SETDET_SETPRTY_95R_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='95R')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 107, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 107, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_170_TRADDET_SETDET_SETPRTY_95R_Type', MT598_170_TRADDET_SETDET_SETPRTY_95R_Type)


# Complex type {http://www.w3schools.com}MT598_170_TRADDET_35B_Type with content type SIMPLE
class MT598_170_TRADDET_35B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_170_TRADDET_35B_Type with content type SIMPLE"""
    _TypeDefinition = MT598_170_TRADDET_35B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_170_TRADDET_35B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 116, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT598_170_TRADDET_35B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_170_TRADDET_35B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='35B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 119, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 119, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_170_TRADDET_35B_Type', MT598_170_TRADDET_35B_Type)


# Complex type {http://www.w3schools.com}MT598_170_GENL_98C_Type with content type SIMPLE
class MT598_170_GENL_98C_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_170_GENL_98C_Type with content type SIMPLE"""
    _TypeDefinition = MT598_170_GENL_98C_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_170_GENL_98C_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 128, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT598_170_GENL_98C_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_170_GENL_98C_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='98C')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 131, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 131, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_170_GENL_98C_Type', MT598_170_GENL_98C_Type)


# Complex type {http://www.w3schools.com}MT598_170_TRADDET_20C-TRRF_Type with content type SIMPLE
class MT598_170_TRADDET_20C_TRRF_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_170_TRADDET_20C-TRRF_Type with content type SIMPLE"""
    _TypeDefinition = MT598_170_TRADDET_20C_TRRF_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_170_TRADDET_20C-TRRF_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 140, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT598_170_TRADDET_20C_TRRF_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_170_TRADDET_20C_TRRF_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='20C')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 143, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 143, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_170_TRADDET_20C-TRRF_Type', MT598_170_TRADDET_20C_TRRF_Type)


# Complex type {http://www.w3schools.com}MT598_170_GENL_23G_Type with content type SIMPLE
class MT598_170_GENL_23G_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_170_GENL_23G_Type with content type SIMPLE"""
    _TypeDefinition = MT598_170_GENL_23G_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_170_GENL_23G_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 152, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT598_170_GENL_23G_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_170_GENL_23G_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='23G')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 155, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 155, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_170_GENL_23G_Type', MT598_170_GENL_23G_Type)


# Complex type {http://www.w3schools.com}MT598_170_TRADDET_FIA_92A_Type with content type SIMPLE
class MT598_170_TRADDET_FIA_92A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_170_TRADDET_FIA_92A_Type with content type SIMPLE"""
    _TypeDefinition = MT598_170_TRADDET_FIA_92A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_170_TRADDET_FIA_92A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 164, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT598_170_TRADDET_FIA_92A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_170_TRADDET_FIA_92A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='92A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 167, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 167, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_170_TRADDET_FIA_92A_Type', MT598_170_TRADDET_FIA_92A_Type)


# Complex type {http://www.w3schools.com}MT598_170_TRADDET_SETDET_AMT_19A_Type with content type SIMPLE
class MT598_170_TRADDET_SETDET_AMT_19A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_170_TRADDET_SETDET_AMT_19A_Type with content type SIMPLE"""
    _TypeDefinition = MT598_170_TRADDET_SETDET_AMT_19A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_170_TRADDET_SETDET_AMT_19A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 176, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT598_170_TRADDET_SETDET_AMT_19A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_170_TRADDET_SETDET_AMT_19A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='19A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 179, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 179, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_170_TRADDET_SETDET_AMT_19A_Type', MT598_170_TRADDET_SETDET_AMT_19A_Type)


# Complex type {http://www.w3schools.com}MT598_170_TRADDET_ALLOCDTLS_36B_Type with content type SIMPLE
class MT598_170_TRADDET_ALLOCDTLS_36B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_170_TRADDET_ALLOCDTLS_36B_Type with content type SIMPLE"""
    _TypeDefinition = MT598_170_TRADDET_ALLOCDTLS_36B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_170_TRADDET_ALLOCDTLS_36B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 188, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT598_170_TRADDET_ALLOCDTLS_36B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_170_TRADDET_ALLOCDTLS_36B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='36B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 191, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 191, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_170_TRADDET_ALLOCDTLS_36B_Type', MT598_170_TRADDET_ALLOCDTLS_36B_Type)


# Complex type {http://www.w3schools.com}MT598_170_20_Type with content type SIMPLE
class MT598_170_20_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_170_20_Type with content type SIMPLE"""
    _TypeDefinition = MT598_170_20_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_170_20_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 200, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT598_170_20_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_170_20_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='20')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 203, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 203, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_170_20_Type', MT598_170_20_Type)


# Complex type {http://www.w3schools.com}MT598_170_TRADDET_FIA_98A-FRNR_Type with content type SIMPLE
class MT598_170_TRADDET_FIA_98A_FRNR_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_170_TRADDET_FIA_98A-FRNR_Type with content type SIMPLE"""
    _TypeDefinition = MT598_170_TRADDET_FIA_98A_FRNR_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_170_TRADDET_FIA_98A-FRNR_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 212, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT598_170_TRADDET_FIA_98A_FRNR_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_170_TRADDET_FIA_98A_FRNR_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='98A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 215, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 215, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_170_TRADDET_FIA_98A-FRNR_Type', MT598_170_TRADDET_FIA_98A_FRNR_Type)


# Complex type {http://www.w3schools.com}MT598_170_TRADDET_SETDET_REPO_19A_Type with content type SIMPLE
class MT598_170_TRADDET_SETDET_REPO_19A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_170_TRADDET_SETDET_REPO_19A_Type with content type SIMPLE"""
    _TypeDefinition = MT598_170_TRADDET_SETDET_REPO_19A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_170_TRADDET_SETDET_REPO_19A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 224, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT598_170_TRADDET_SETDET_REPO_19A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_170_TRADDET_SETDET_REPO_19A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='19A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 227, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 227, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_170_TRADDET_SETDET_REPO_19A_Type', MT598_170_TRADDET_SETDET_REPO_19A_Type)


# Complex type {http://www.w3schools.com}MT598_170_TRADDET_ALLOCDTLS_19A-TRTE_Type with content type SIMPLE
class MT598_170_TRADDET_ALLOCDTLS_19A_TRTE_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_170_TRADDET_ALLOCDTLS_19A-TRTE_Type with content type SIMPLE"""
    _TypeDefinition = MT598_170_TRADDET_ALLOCDTLS_19A_TRTE_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_170_TRADDET_ALLOCDTLS_19A-TRTE_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 236, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT598_170_TRADDET_ALLOCDTLS_19A_TRTE_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_170_TRADDET_ALLOCDTLS_19A_TRTE_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='19A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 239, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 239, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_170_TRADDET_ALLOCDTLS_19A-TRTE_Type', MT598_170_TRADDET_ALLOCDTLS_19A_TRTE_Type)


# Complex type {http://www.w3schools.com}MT598_170_TRADDET_98B-SETT_Type with content type SIMPLE
class MT598_170_TRADDET_98B_SETT_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_170_TRADDET_98B-SETT_Type with content type SIMPLE"""
    _TypeDefinition = MT598_170_TRADDET_98B_SETT_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_170_TRADDET_98B-SETT_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 248, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT598_170_TRADDET_98B_SETT_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_170_TRADDET_98B_SETT_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='98B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 251, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 251, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_170_TRADDET_98B-SETT_Type', MT598_170_TRADDET_98B_SETT_Type)


# Complex type {http://www.w3schools.com}MT598_170_TRADDET_98A-TRAD_Type with content type SIMPLE
class MT598_170_TRADDET_98A_TRAD_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_170_TRADDET_98A-TRAD_Type with content type SIMPLE"""
    _TypeDefinition = MT598_170_TRADDET_98A_TRAD_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_170_TRADDET_98A-TRAD_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 260, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT598_170_TRADDET_98A_TRAD_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_170_TRADDET_98A_TRAD_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='98A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 263, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 263, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_170_TRADDET_98A-TRAD_Type', MT598_170_TRADDET_98A_TRAD_Type)


# Complex type {http://www.w3schools.com}MT598_170_TRADDET_SETDET_AMT_36B_Type with content type SIMPLE
class MT598_170_TRADDET_SETDET_AMT_36B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_170_TRADDET_SETDET_AMT_36B_Type with content type SIMPLE"""
    _TypeDefinition = MT598_170_TRADDET_SETDET_AMT_36B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_170_TRADDET_SETDET_AMT_36B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 272, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT598_170_TRADDET_SETDET_AMT_36B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_170_TRADDET_SETDET_AMT_36B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='36B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 275, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 275, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_170_TRADDET_SETDET_AMT_36B_Type', MT598_170_TRADDET_SETDET_AMT_36B_Type)


# Complex type {http://www.w3schools.com}MT598_170_TRADDET_SETDET_REPO_98A-TERM_Type with content type SIMPLE
class MT598_170_TRADDET_SETDET_REPO_98A_TERM_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_170_TRADDET_SETDET_REPO_98A-TERM_Type with content type SIMPLE"""
    _TypeDefinition = MT598_170_TRADDET_SETDET_REPO_98A_TERM_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_170_TRADDET_SETDET_REPO_98A-TERM_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 291, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT598_170_TRADDET_SETDET_REPO_98A_TERM_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_170_TRADDET_SETDET_REPO_98A_TERM_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='98A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 294, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 294, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_170_TRADDET_SETDET_REPO_98A-TERM_Type', MT598_170_TRADDET_SETDET_REPO_98A_TERM_Type)


# Complex type {http://www.w3schools.com}MT598_170_GENL_LINK_20C-RELA_Type with content type SIMPLE
class MT598_170_GENL_LINK_20C_RELA_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_170_GENL_LINK_20C-RELA_Type with content type SIMPLE"""
    _TypeDefinition = MT598_170_GENL_LINK_20C_RELA_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_170_GENL_LINK_20C-RELA_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 303, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT598_170_GENL_LINK_20C_RELA_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_170_GENL_LINK_20C_RELA_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='20C')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 306, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 306, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_170_GENL_LINK_20C-RELA_Type', MT598_170_GENL_LINK_20C_RELA_Type)


MT598_170 = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'MT598_170'), CTD_ANON, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 402, 1))
Namespace.addCategoryObject('elementBinding', MT598_170.name().localName(), MT598_170)



MT598_170_TRADDET_SETDET_SETPRTY._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ReceivingorDeliveringTradersCSDBPID'), MT598_170_TRADDET_SETDET_SETPRTY_95R_Type, scope=MT598_170_TRADDET_SETDET_SETPRTY, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 326, 3)))

def _BuildAutomaton ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT598_170_TRADDET_SETDET_SETPRTY._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ReceivingorDeliveringTradersCSDBPID')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 326, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
MT598_170_TRADDET_SETDET_SETPRTY._Automaton = _BuildAutomaton()




MT598_170_TRADDET_SETDET_REPO._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'RepurchaseDateFixed'), MT598_170_TRADDET_SETDET_REPO_98A_TERM_Type, scope=MT598_170_TRADDET_SETDET_REPO, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 332, 3)))

MT598_170_TRADDET_SETDET_REPO._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'RepurchaseDateOpen'), MT598_170_TRADDET_SETDET_REPO_98B_TERM_Type, scope=MT598_170_TRADDET_SETDET_REPO, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 333, 3)))

MT598_170_TRADDET_SETDET_REPO._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'RepurchaseAmount'), MT598_170_TRADDET_SETDET_REPO_19A_Type, scope=MT598_170_TRADDET_SETDET_REPO, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 334, 3)))

def _BuildAutomaton_ ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_
    del _BuildAutomaton_
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 332, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 333, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 334, 3))
    counters.add(cc_2)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(MT598_170_TRADDET_SETDET_REPO._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'RepurchaseDateFixed')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 332, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(MT598_170_TRADDET_SETDET_REPO._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'RepurchaseDateOpen')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 333, 3))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(MT598_170_TRADDET_SETDET_REPO._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'RepurchaseAmount')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 334, 3))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_2, True) ]))
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
MT598_170_TRADDET_SETDET_REPO._Automaton = _BuildAutomaton_()




MT598_170_TRADDET_SETDET_AMT._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'NominalValue'), MT598_170_TRADDET_SETDET_AMT_36B_Type, scope=MT598_170_TRADDET_SETDET_AMT, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 340, 3)))

MT598_170_TRADDET_SETDET_AMT._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SettlementAmount'), MT598_170_TRADDET_SETDET_AMT_19A_Type, scope=MT598_170_TRADDET_SETDET_AMT, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 341, 3)))

MT598_170_TRADDET_SETDET_AMT._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'TapTonUpNominalValue'), MT598_170_TRADDET_SETDET_AMT_36B_Type, scope=MT598_170_TRADDET_SETDET_AMT, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 342, 3)))

def _BuildAutomaton_2 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_2
    del _BuildAutomaton_2
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 341, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 342, 3))
    counters.add(cc_1)
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT598_170_TRADDET_SETDET_AMT._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'NominalValue')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 340, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(MT598_170_TRADDET_SETDET_AMT._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SettlementAmount')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 341, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(MT598_170_TRADDET_SETDET_AMT._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'TapTonUpNominalValue')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 342, 3))
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
MT598_170_TRADDET_SETDET_AMT._Automaton = _BuildAutomaton_2()




MT598_170_TRADDET_FIA._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'CurrentInterestRate'), MT598_170_TRADDET_FIA_92A_Type, scope=MT598_170_TRADDET_FIA, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 348, 3)))

MT598_170_TRADDET_FIA._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'NextResetDate'), MT598_170_TRADDET_FIA_98A_FRNR_Type, scope=MT598_170_TRADDET_FIA, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 349, 3)))

MT598_170_TRADDET_FIA._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'MaturityDate'), MT598_170_TRADDET_FIA_98A_MATU_Type, scope=MT598_170_TRADDET_FIA, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 350, 3)))

MT598_170_TRADDET_FIA._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'NextPaymentDate'), MT598_170_TRADDET_FIA_98A_COUP_Type, scope=MT598_170_TRADDET_FIA, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 351, 3)))

def _BuildAutomaton_3 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_3
    del _BuildAutomaton_3
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 348, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 349, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 350, 3))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 351, 3))
    counters.add(cc_3)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(MT598_170_TRADDET_FIA._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'CurrentInterestRate')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 348, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(MT598_170_TRADDET_FIA._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'NextResetDate')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 349, 3))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(MT598_170_TRADDET_FIA._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'MaturityDate')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 350, 3))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(MT598_170_TRADDET_FIA._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'NextPaymentDate')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 351, 3))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_3, True) ]))
    st_3._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
MT598_170_TRADDET_FIA._Automaton = _BuildAutomaton_3()




MT598_170_TRADDET_ALLOCDTLS._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SORAccount'), MT598_170_TRADDET_ALLOCDTLS_97B_SAFE_Type, scope=MT598_170_TRADDET_ALLOCDTLS, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 357, 3)))

MT598_170_TRADDET_ALLOCDTLS._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'NominalValue'), MT598_170_TRADDET_ALLOCDTLS_36B_Type, scope=MT598_170_TRADDET_ALLOCDTLS, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 358, 3)))

MT598_170_TRADDET_ALLOCDTLS._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SettlementAmount'), MT598_170_TRADDET_ALLOCDTLS_19A_SETT_Type, scope=MT598_170_TRADDET_ALLOCDTLS, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 359, 3)))

MT598_170_TRADDET_ALLOCDTLS._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'RepurchaseAmount'), MT598_170_TRADDET_ALLOCDTLS_19A_TRTE_Type, scope=MT598_170_TRADDET_ALLOCDTLS, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 360, 3)))

def _BuildAutomaton_4 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_4
    del _BuildAutomaton_4
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 359, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 360, 3))
    counters.add(cc_1)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT598_170_TRADDET_ALLOCDTLS._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SORAccount')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 357, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT598_170_TRADDET_ALLOCDTLS._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'NominalValue')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 358, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(MT598_170_TRADDET_ALLOCDTLS._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SettlementAmount')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 359, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(MT598_170_TRADDET_ALLOCDTLS._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'RepurchaseAmount')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 360, 3))
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
MT598_170_TRADDET_ALLOCDTLS._Automaton = _BuildAutomaton_4()




MT598_170_GENL_LINK._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'InternalTradeReference'), MT598_170_GENL_LINK_20C_RELA_Type, scope=MT598_170_GENL_LINK, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 366, 3)))

def _BuildAutomaton_5 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_5
    del _BuildAutomaton_5
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT598_170_GENL_LINK._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'InternalTradeReference')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 366, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
MT598_170_GENL_LINK._Automaton = _BuildAutomaton_5()




MT598_170_GENL._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'FunctionOfMessage'), MT598_170_GENL_23G_Type, scope=MT598_170_GENL, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 372, 3)))

MT598_170_GENL._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PreparationDateAndTime'), MT598_170_GENL_98C_Type, scope=MT598_170_GENL, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 373, 3)))

MT598_170_GENL._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'LINK'), MT598_170_GENL_LINK, scope=MT598_170_GENL, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 374, 3)))

def _BuildAutomaton_6 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_6
    del _BuildAutomaton_6
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 373, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 374, 3))
    counters.add(cc_1)
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT598_170_GENL._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'FunctionOfMessage')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 372, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(MT598_170_GENL._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PreparationDateAndTime')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 373, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(MT598_170_GENL._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'LINK')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 374, 3))
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
MT598_170_GENL._Automaton = _BuildAutomaton_6()




MT598_170_TRADDET_SETDET._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SettlementTransactionType'), MT598_170_TRADDET_SETDET_22F_Type, scope=MT598_170_TRADDET_SETDET, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 380, 3)))

MT598_170_TRADDET_SETDET._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SETPRTY'), MT598_170_TRADDET_SETDET_SETPRTY, scope=MT598_170_TRADDET_SETDET, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 381, 3)))

MT598_170_TRADDET_SETDET._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'AMT'), MT598_170_TRADDET_SETDET_AMT, scope=MT598_170_TRADDET_SETDET, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 382, 3)))

MT598_170_TRADDET_SETDET._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'REPO'), MT598_170_TRADDET_SETDET_REPO, scope=MT598_170_TRADDET_SETDET, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 383, 3)))

def _BuildAutomaton_7 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_7
    del _BuildAutomaton_7
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 383, 3))
    counters.add(cc_0)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT598_170_TRADDET_SETDET._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SettlementTransactionType')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 380, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT598_170_TRADDET_SETDET._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SETPRTY')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 381, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT598_170_TRADDET_SETDET._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'AMT')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 382, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(MT598_170_TRADDET_SETDET._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'REPO')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 383, 3))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
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
MT598_170_TRADDET_SETDET._Automaton = _BuildAutomaton_7()




MT598_170_TRADDET._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'InternalTradeReference'), MT598_170_TRADDET_20C_TRRF_Type, scope=MT598_170_TRADDET, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 389, 3)))

MT598_170_TRADDET._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'TradeDate'), MT598_170_TRADDET_98A_TRAD_Type, scope=MT598_170_TRADDET, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 390, 3)))

MT598_170_TRADDET._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SettlementDate'), MT598_170_TRADDET_98A_SETT_Type, scope=MT598_170_TRADDET, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 391, 3)))

MT598_170_TRADDET._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SettlementDateOpen'), MT598_170_TRADDET_98B_SETT_Type, scope=MT598_170_TRADDET, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 392, 3)))

MT598_170_TRADDET._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'IdentificationOfSecurities'), MT598_170_TRADDET_35B_Type, scope=MT598_170_TRADDET, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 393, 3)))

MT598_170_TRADDET._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'FIA'), MT598_170_TRADDET_FIA, scope=MT598_170_TRADDET, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 394, 3)))

MT598_170_TRADDET._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'AffirmationIndicator'), MT598_170_TRADDET_25D_Type, scope=MT598_170_TRADDET, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 395, 3)))

MT598_170_TRADDET._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SettlementInstuctionProcessingNarrative'), MT598_170_TRADDET_70E_Type, scope=MT598_170_TRADDET, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 396, 3)))

MT598_170_TRADDET._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SETDET'), MT598_170_TRADDET_SETDET, scope=MT598_170_TRADDET, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 397, 3)))

MT598_170_TRADDET._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ALLOCDTLS'), MT598_170_TRADDET_ALLOCDTLS, scope=MT598_170_TRADDET, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 398, 3)))

def _BuildAutomaton_8 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_8
    del _BuildAutomaton_8
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 391, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 392, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 394, 3))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 396, 3))
    counters.add(cc_3)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT598_170_TRADDET._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'InternalTradeReference')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 389, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT598_170_TRADDET._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'TradeDate')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 390, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT598_170_TRADDET._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SettlementDate')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 391, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT598_170_TRADDET._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SettlementDateOpen')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 392, 3))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT598_170_TRADDET._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'IdentificationOfSecurities')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 393, 3))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT598_170_TRADDET._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'FIA')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 394, 3))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT598_170_TRADDET._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'AffirmationIndicator')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 395, 3))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT598_170_TRADDET._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SettlementInstuctionProcessingNarrative')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 396, 3))
    st_7 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT598_170_TRADDET._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SETDET')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 397, 3))
    st_8 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT598_170_TRADDET._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ALLOCDTLS')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 398, 3))
    st_9 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
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
    transitions.append(fac.Transition(st_5, [
         ]))
    transitions.append(fac.Transition(st_6, [
         ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
         ]))
    transitions.append(fac.Transition(st_8, [
         ]))
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
    transitions.append(fac.Transition(st_9, [
         ]))
    st_9._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
MT598_170_TRADDET._Automaton = _BuildAutomaton_8()




CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'TransactionReference'), MT598_170_20_Type, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 405, 4)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SubMessageType'), MT598_170_12_Type, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 406, 4)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ProprietaryMessage'), MT598_170_77E_Type, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 407, 4)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'GENL'), MT598_170_GENL, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 408, 4)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'TRADDET'), MT598_170_TRADDET, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 409, 4)))

def _BuildAutomaton_9 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_9
    del _BuildAutomaton_9
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'TransactionReference')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 405, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SubMessageType')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 406, 4))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ProprietaryMessage')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 407, 4))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'GENL')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 408, 4))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'TRADDET')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_170.xsd', 409, 4))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
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
    st_4._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON._Automaton = _BuildAutomaton_9()

