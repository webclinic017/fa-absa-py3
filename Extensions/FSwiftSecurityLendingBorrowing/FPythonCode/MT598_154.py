
# C:\SWIFT\SwiftReader\XSD\MT598_154.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:96afad3d20bbfe8d040a1a097fa388d9fecd10e3
# Generated 2017-02-16 17:32:49.661000 by PyXB version 1.2.2
# Namespace http://www.w3schools.com

import pyxb
import pyxb.binding
import pyxb.binding.saxer
import StringIO
import pyxb.utils.utility
import pyxb.utils.domutils
import sys

# Unique identifier for bindings created at the same time
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:d627d330-f43f-11e6-a9da-180373dbbcdf')

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


# Atomic simple type: {http://www.w3schools.com}MT598_154_MMID_FIA_22F-CCFR_Type_Pattern
class MT598_154_MMID_FIA_22F_CCFR_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_154_MMID_FIA_22F-CCFR_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 3, 1)
    _Documentation = None
MT598_154_MMID_FIA_22F_CCFR_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT598_154_MMID_FIA_22F_CCFR_Type_Pattern._CF_pattern.addPattern(pattern='(:(CCFR)/STRA/(WEEK|MNTH|QUTR|SEMI|ANNU|NONE))')
MT598_154_MMID_FIA_22F_CCFR_Type_Pattern._InitializeFacetMap(MT598_154_MMID_FIA_22F_CCFR_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT598_154_MMID_FIA_22F-CCFR_Type_Pattern', MT598_154_MMID_FIA_22F_CCFR_Type_Pattern)

# Atomic simple type: {http://www.w3schools.com}MT598_154_MMID_95R-ISSA_Type_Pattern
class MT598_154_MMID_95R_ISSA_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_154_MMID_95R-ISSA_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 15, 1)
    _Documentation = None
MT598_154_MMID_95R_ISSA_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT598_154_MMID_95R_ISSA_Type_Pattern._CF_pattern.addPattern(pattern='(:(ISSA)/STRA/[A-Z]{2}[0-9]{6})')
MT598_154_MMID_95R_ISSA_Type_Pattern._InitializeFacetMap(MT598_154_MMID_95R_ISSA_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT598_154_MMID_95R-ISSA_Type_Pattern', MT598_154_MMID_95R_ISSA_Type_Pattern)

# Atomic simple type: {http://www.w3schools.com}MT598_154_MMID_FIA_17B-CPMI_Type_Pattern
class MT598_154_MMID_FIA_17B_CPMI_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_154_MMID_FIA_17B-CPMI_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 34, 1)
    _Documentation = None
MT598_154_MMID_FIA_17B_CPMI_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT598_154_MMID_FIA_17B_CPMI_Type_Pattern._CF_pattern.addPattern(pattern='(:(CPMI)//(Y|N))')
MT598_154_MMID_FIA_17B_CPMI_Type_Pattern._InitializeFacetMap(MT598_154_MMID_FIA_17B_CPMI_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT598_154_MMID_FIA_17B-CPMI_Type_Pattern', MT598_154_MMID_FIA_17B_CPMI_Type_Pattern)

# Atomic simple type: {http://www.w3schools.com}MT598_154_MMID_FIA_13B-CPYD_Type_Pattern
class MT598_154_MMID_FIA_13B_CPYD_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_154_MMID_FIA_13B-CPYD_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 46, 1)
    _Documentation = None
MT598_154_MMID_FIA_13B_CPYD_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT598_154_MMID_FIA_13B_CPYD_Type_Pattern._CF_pattern.addPattern(pattern='(:(CPYD)/STRA/[0-9]{2})')
MT598_154_MMID_FIA_13B_CPYD_Type_Pattern._InitializeFacetMap(MT598_154_MMID_FIA_13B_CPYD_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT598_154_MMID_FIA_13B-CPYD_Type_Pattern', MT598_154_MMID_FIA_13B_CPYD_Type_Pattern)

# Atomic simple type: {http://www.w3schools.com}MT598_154_MMID_FIA_CPDDET_98A_Type_Pattern
class MT598_154_MMID_FIA_CPDDET_98A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_154_MMID_FIA_CPDDET_98A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 58, 1)
    _Documentation = None
MT598_154_MMID_FIA_CPDDET_98A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT598_154_MMID_FIA_CPDDET_98A_Type_Pattern._CF_pattern.addPattern(pattern='(:(PAYD)//[0-9]{8})')
MT598_154_MMID_FIA_CPDDET_98A_Type_Pattern._InitializeFacetMap(MT598_154_MMID_FIA_CPDDET_98A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT598_154_MMID_FIA_CPDDET_98A_Type_Pattern', MT598_154_MMID_FIA_CPDDET_98A_Type_Pattern)

# Atomic simple type: {http://www.w3schools.com}MT598_154_MMID_FIA_36B-AUTH_Type_Pattern
class MT598_154_MMID_FIA_36B_AUTH_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_154_MMID_FIA_36B-AUTH_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 70, 1)
    _Documentation = None
MT598_154_MMID_FIA_36B_AUTH_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT598_154_MMID_FIA_36B_AUTH_Type_Pattern._CF_pattern.addPattern(pattern='(:(AUTH)//FAMT/[0-9]{1,12},([0-9]{1,2})*)')
MT598_154_MMID_FIA_36B_AUTH_Type_Pattern._InitializeFacetMap(MT598_154_MMID_FIA_36B_AUTH_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT598_154_MMID_FIA_36B-AUTH_Type_Pattern', MT598_154_MMID_FIA_36B_AUTH_Type_Pattern)

# Atomic simple type: {http://www.w3schools.com}MT598_154_MMID_FIA_98A-CRSD_Type_Pattern
class MT598_154_MMID_FIA_98A_CRSD_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_154_MMID_FIA_98A-CRSD_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 82, 1)
    _Documentation = None
MT598_154_MMID_FIA_98A_CRSD_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT598_154_MMID_FIA_98A_CRSD_Type_Pattern._CF_pattern.addPattern(pattern='(:(CRSD)//[0-9]{8})')
MT598_154_MMID_FIA_98A_CRSD_Type_Pattern._InitializeFacetMap(MT598_154_MMID_FIA_98A_CRSD_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT598_154_MMID_FIA_98A-CRSD_Type_Pattern', MT598_154_MMID_FIA_98A_CRSD_Type_Pattern)

# Atomic simple type: {http://www.w3schools.com}MT598_154_MMID_FIA_36B-MINI_Type_Pattern
class MT598_154_MMID_FIA_36B_MINI_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_154_MMID_FIA_36B-MINI_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 94, 1)
    _Documentation = None
MT598_154_MMID_FIA_36B_MINI_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT598_154_MMID_FIA_36B_MINI_Type_Pattern._CF_pattern.addPattern(pattern='(:(MINI)//FAMT/[0-9]{1,12},([0-9]{1,2})*)')
MT598_154_MMID_FIA_36B_MINI_Type_Pattern._InitializeFacetMap(MT598_154_MMID_FIA_36B_MINI_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT598_154_MMID_FIA_36B-MINI_Type_Pattern', MT598_154_MMID_FIA_36B_MINI_Type_Pattern)

# Atomic simple type: {http://www.w3schools.com}MT598_154_MMID_FIA_92A-TAXR_Type_Pattern
class MT598_154_MMID_FIA_92A_TAXR_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_154_MMID_FIA_92A-TAXR_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 106, 1)
    _Documentation = None
MT598_154_MMID_FIA_92A_TAXR_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT598_154_MMID_FIA_92A_TAXR_Type_Pattern._CF_pattern.addPattern(pattern='(:(TAXR)//(N)?[0-9]{1,12},([0-9]{1,2})*)')
MT598_154_MMID_FIA_92A_TAXR_Type_Pattern._InitializeFacetMap(MT598_154_MMID_FIA_92A_TAXR_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT598_154_MMID_FIA_92A-TAXR_Type_Pattern', MT598_154_MMID_FIA_92A_TAXR_Type_Pattern)

# Atomic simple type: {http://www.w3schools.com}MT598_154_MMID_FIA_22F-CPDI_Type_Pattern
class MT598_154_MMID_FIA_22F_CPDI_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_154_MMID_FIA_22F-CPDI_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 118, 1)
    _Documentation = None
MT598_154_MMID_FIA_22F_CPDI_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT598_154_MMID_FIA_22F_CPDI_Type_Pattern._CF_pattern.addPattern(pattern='(:(CPDI)/STRA/(CLDT|ISDT))')
MT598_154_MMID_FIA_22F_CPDI_Type_Pattern._InitializeFacetMap(MT598_154_MMID_FIA_22F_CPDI_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT598_154_MMID_FIA_22F-CPDI_Type_Pattern', MT598_154_MMID_FIA_22F_CPDI_Type_Pattern)

# Atomic simple type: {http://www.w3schools.com}MT598_154_20_Type_Pattern
class MT598_154_20_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_154_20_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 130, 1)
    _Documentation = None
MT598_154_20_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT598_154_20_Type_Pattern._CF_pattern.addPattern(pattern='(.{1,16})')
MT598_154_20_Type_Pattern._InitializeFacetMap(MT598_154_20_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT598_154_20_Type_Pattern', MT598_154_20_Type_Pattern)

# Atomic simple type: {http://www.w3schools.com}MT598_154_MMID_35B_Type_Pattern
class MT598_154_MMID_35B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_154_MMID_35B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 142, 1)
    _Documentation = None
MT598_154_MMID_35B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT598_154_MMID_35B_Type_Pattern._CF_pattern.addPattern(pattern='((ISIN {1}[A-Z0-9]{12})?(\\n)?((.{1,35}\\n?){1,4})?)')
MT598_154_MMID_35B_Type_Pattern._InitializeFacetMap(MT598_154_MMID_35B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT598_154_MMID_35B_Type_Pattern', MT598_154_MMID_35B_Type_Pattern)

# Atomic simple type: {http://www.w3schools.com}MT598_154_MMID_FIA_14F_Type_Pattern
class MT598_154_MMID_FIA_14F_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_154_MMID_FIA_14F_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 154, 1)
    _Documentation = None
MT598_154_MMID_FIA_14F_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT598_154_MMID_FIA_14F_Type_Pattern._CF_pattern.addPattern(pattern='(ZAR-(JIBAR1|JIBAR3|JIBAR6|JIBAR9|JIBAR12|CPI|PRIME|SREPO|SABOR)(-[A-Z0-9]{4})?)')
MT598_154_MMID_FIA_14F_Type_Pattern._InitializeFacetMap(MT598_154_MMID_FIA_14F_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT598_154_MMID_FIA_14F_Type_Pattern', MT598_154_MMID_FIA_14F_Type_Pattern)

# Atomic simple type: {http://www.w3schools.com}MT598_154_MMID_FIA_CRDDET_98A_Type_Pattern
class MT598_154_MMID_FIA_CRDDET_98A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_154_MMID_FIA_CRDDET_98A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 166, 1)
    _Documentation = None
MT598_154_MMID_FIA_CRDDET_98A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT598_154_MMID_FIA_CRDDET_98A_Type_Pattern._CF_pattern.addPattern(pattern='(:(RESD)//[0-9]{8})')
MT598_154_MMID_FIA_CRDDET_98A_Type_Pattern._InitializeFacetMap(MT598_154_MMID_FIA_CRDDET_98A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT598_154_MMID_FIA_CRDDET_98A_Type_Pattern', MT598_154_MMID_FIA_CRDDET_98A_Type_Pattern)

# Atomic simple type: {http://www.w3schools.com}MT598_154_MMID_FIA_25_Type_Pattern
class MT598_154_MMID_FIA_25_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_154_MMID_FIA_25_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 178, 1)
    _Documentation = None
MT598_154_MMID_FIA_25_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT598_154_MMID_FIA_25_Type_Pattern._CF_pattern.addPattern(pattern='((PLUS|MINUS|GT|LT|EQUAL|NONE|OF)(-[0-9]{1,12},([0-9]{1,2})*)?(-(PRCT))?)')
MT598_154_MMID_FIA_25_Type_Pattern._InitializeFacetMap(MT598_154_MMID_FIA_25_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT598_154_MMID_FIA_25_Type_Pattern', MT598_154_MMID_FIA_25_Type_Pattern)

# Atomic simple type: {http://www.w3schools.com}MT598_154_MMID_FIA_98A-MATU_Type_Pattern
class MT598_154_MMID_FIA_98A_MATU_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_154_MMID_FIA_98A-MATU_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 190, 1)
    _Documentation = None
MT598_154_MMID_FIA_98A_MATU_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT598_154_MMID_FIA_98A_MATU_Type_Pattern._CF_pattern.addPattern(pattern='(:(MATU)//[0-9]{8})')
MT598_154_MMID_FIA_98A_MATU_Type_Pattern._InitializeFacetMap(MT598_154_MMID_FIA_98A_MATU_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT598_154_MMID_FIA_98A-MATU_Type_Pattern', MT598_154_MMID_FIA_98A_MATU_Type_Pattern)

# Atomic simple type: {http://www.w3schools.com}MT598_154_MMID_36B-QISS_Type_Pattern
class MT598_154_MMID_36B_QISS_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_154_MMID_36B-QISS_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 202, 1)
    _Documentation = None
MT598_154_MMID_36B_QISS_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT598_154_MMID_36B_QISS_Type_Pattern._CF_pattern.addPattern(pattern='(:(QISS)//FAMT/[0-9]{1,12},([0-9]{1,2})*)')
MT598_154_MMID_36B_QISS_Type_Pattern._InitializeFacetMap(MT598_154_MMID_36B_QISS_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT598_154_MMID_36B-QISS_Type_Pattern', MT598_154_MMID_36B_QISS_Type_Pattern)

# Atomic simple type: {http://www.w3schools.com}MT598_154_MMID_FIA_36B-MINO_Type_Pattern
class MT598_154_MMID_FIA_36B_MINO_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_154_MMID_FIA_36B-MINO_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 221, 1)
    _Documentation = None
MT598_154_MMID_FIA_36B_MINO_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT598_154_MMID_FIA_36B_MINO_Type_Pattern._CF_pattern.addPattern(pattern='(:(MINO)//FAMT/[0-9]{1,12},([0-9]{1,2})*)')
MT598_154_MMID_FIA_36B_MINO_Type_Pattern._InitializeFacetMap(MT598_154_MMID_FIA_36B_MINO_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT598_154_MMID_FIA_36B-MINO_Type_Pattern', MT598_154_MMID_FIA_36B_MINO_Type_Pattern)

# Atomic simple type: {http://www.w3schools.com}MT598_154_MMID_FIA_13B-CPCM_Type_Pattern
class MT598_154_MMID_FIA_13B_CPCM_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_154_MMID_FIA_13B-CPCM_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 233, 1)
    _Documentation = None
MT598_154_MMID_FIA_13B_CPCM_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT598_154_MMID_FIA_13B_CPCM_Type_Pattern._CF_pattern.addPattern(pattern='(:(CPCM)/STRA/(1|2|3))')
MT598_154_MMID_FIA_13B_CPCM_Type_Pattern._InitializeFacetMap(MT598_154_MMID_FIA_13B_CPCM_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT598_154_MMID_FIA_13B-CPCM_Type_Pattern', MT598_154_MMID_FIA_13B_CPCM_Type_Pattern)

# Atomic simple type: {http://www.w3schools.com}MT598_154_MMID_FIA_12A_Type_Pattern
class MT598_154_MMID_FIA_12A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_154_MMID_FIA_12A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 245, 1)
    _Documentation = None
MT598_154_MMID_FIA_12A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT598_154_MMID_FIA_12A_Type_Pattern._CF_pattern.addPattern(pattern='(:(CATG)//(1|2|3))')
MT598_154_MMID_FIA_12A_Type_Pattern._InitializeFacetMap(MT598_154_MMID_FIA_12A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT598_154_MMID_FIA_12A_Type_Pattern', MT598_154_MMID_FIA_12A_Type_Pattern)

# Atomic simple type: {http://www.w3schools.com}MT598_154_MMID_FIA_98A-ISSU_Type_Pattern
class MT598_154_MMID_FIA_98A_ISSU_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_154_MMID_FIA_98A-ISSU_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 257, 1)
    _Documentation = None
MT598_154_MMID_FIA_98A_ISSU_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT598_154_MMID_FIA_98A_ISSU_Type_Pattern._CF_pattern.addPattern(pattern='(:(ISSU)//[0-9]{8})')
MT598_154_MMID_FIA_98A_ISSU_Type_Pattern._InitializeFacetMap(MT598_154_MMID_FIA_98A_ISSU_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT598_154_MMID_FIA_98A-ISSU_Type_Pattern', MT598_154_MMID_FIA_98A_ISSU_Type_Pattern)

# Atomic simple type: {http://www.w3schools.com}MT598_154_MMID_FIA_17B-ACPC_Type_Pattern
class MT598_154_MMID_FIA_17B_ACPC_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_154_MMID_FIA_17B-ACPC_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 269, 1)
    _Documentation = None
MT598_154_MMID_FIA_17B_ACPC_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT598_154_MMID_FIA_17B_ACPC_Type_Pattern._CF_pattern.addPattern(pattern='(:(ACPC)//(Y|N))')
MT598_154_MMID_FIA_17B_ACPC_Type_Pattern._InitializeFacetMap(MT598_154_MMID_FIA_17B_ACPC_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT598_154_MMID_FIA_17B-ACPC_Type_Pattern', MT598_154_MMID_FIA_17B_ACPC_Type_Pattern)

# Atomic simple type: {http://www.w3schools.com}MT598_154_GENL_20C_Type_Pattern
class MT598_154_GENL_20C_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_154_GENL_20C_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 281, 1)
    _Documentation = None
MT598_154_GENL_20C_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT598_154_GENL_20C_Type_Pattern._CF_pattern.addPattern(pattern='(:(RELA)//.{1,16})')
MT598_154_GENL_20C_Type_Pattern._InitializeFacetMap(MT598_154_GENL_20C_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT598_154_GENL_20C_Type_Pattern', MT598_154_GENL_20C_Type_Pattern)

# Atomic simple type: {http://www.w3schools.com}MT598_154_MMID_FIA_22F-RESF_Type_Pattern
class MT598_154_MMID_FIA_22F_RESF_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_154_MMID_FIA_22F-RESF_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 293, 1)
    _Documentation = None
MT598_154_MMID_FIA_22F_RESF_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT598_154_MMID_FIA_22F_RESF_Type_Pattern._CF_pattern.addPattern(pattern='(:(RESF)/STRA/(WEEK|MNTH|QUTR|SEMI|ANNU|DALY|ISDF|ADHC))')
MT598_154_MMID_FIA_22F_RESF_Type_Pattern._InitializeFacetMap(MT598_154_MMID_FIA_22F_RESF_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT598_154_MMID_FIA_22F-RESF_Type_Pattern', MT598_154_MMID_FIA_22F_RESF_Type_Pattern)

# Atomic simple type: {http://www.w3schools.com}MT598_154_MMID_97B_Type_Pattern
class MT598_154_MMID_97B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_154_MMID_97B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 305, 1)
    _Documentation = None
MT598_154_MMID_97B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT598_154_MMID_97B_Type_Pattern._CF_pattern.addPattern(pattern='(:(SAFE)/STRA/IORT/[0-9]{8})')
MT598_154_MMID_97B_Type_Pattern._InitializeFacetMap(MT598_154_MMID_97B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT598_154_MMID_97B_Type_Pattern', MT598_154_MMID_97B_Type_Pattern)

# Atomic simple type: {http://www.w3schools.com}MT598_154_MMID_FIA_92A-INTR_Type_Pattern
class MT598_154_MMID_FIA_92A_INTR_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_154_MMID_FIA_92A-INTR_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 317, 1)
    _Documentation = None
MT598_154_MMID_FIA_92A_INTR_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT598_154_MMID_FIA_92A_INTR_Type_Pattern._CF_pattern.addPattern(pattern='(:(INTR)//(N)?[0-9]{1,12},([0-9]{1,2})*)')
MT598_154_MMID_FIA_92A_INTR_Type_Pattern._InitializeFacetMap(MT598_154_MMID_FIA_92A_INTR_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT598_154_MMID_FIA_92A-INTR_Type_Pattern', MT598_154_MMID_FIA_92A_INTR_Type_Pattern)

# Atomic simple type: {http://www.w3schools.com}MT598_154_MMID_FIA_17B-FCPM_Type_Pattern
class MT598_154_MMID_FIA_17B_FCPM_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_154_MMID_FIA_17B-FCPM_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 329, 1)
    _Documentation = None
MT598_154_MMID_FIA_17B_FCPM_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT598_154_MMID_FIA_17B_FCPM_Type_Pattern._CF_pattern.addPattern(pattern='(:(FCPM)//(Y|N))')
MT598_154_MMID_FIA_17B_FCPM_Type_Pattern._InitializeFacetMap(MT598_154_MMID_FIA_17B_FCPM_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT598_154_MMID_FIA_17B-FCPM_Type_Pattern', MT598_154_MMID_FIA_17B_FCPM_Type_Pattern)

# Atomic simple type: {http://www.w3schools.com}MT598_154_MMID_FIA_17B-OVER_Type_Pattern
class MT598_154_MMID_FIA_17B_OVER_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_154_MMID_FIA_17B-OVER_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 341, 1)
    _Documentation = None
MT598_154_MMID_FIA_17B_OVER_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT598_154_MMID_FIA_17B_OVER_Type_Pattern._CF_pattern.addPattern(pattern='(:(OVER)//(Y|N))')
MT598_154_MMID_FIA_17B_OVER_Type_Pattern._InitializeFacetMap(MT598_154_MMID_FIA_17B_OVER_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT598_154_MMID_FIA_17B-OVER_Type_Pattern', MT598_154_MMID_FIA_17B_OVER_Type_Pattern)

# Atomic simple type: {http://www.w3schools.com}MT598_154_MMID_FIA_17B-ACPO_Type_Pattern
class MT598_154_MMID_FIA_17B_ACPO_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_154_MMID_FIA_17B-ACPO_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 353, 1)
    _Documentation = None
MT598_154_MMID_FIA_17B_ACPO_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT598_154_MMID_FIA_17B_ACPO_Type_Pattern._CF_pattern.addPattern(pattern='(:(ACPO)//(Y|N))')
MT598_154_MMID_FIA_17B_ACPO_Type_Pattern._InitializeFacetMap(MT598_154_MMID_FIA_17B_ACPO_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT598_154_MMID_FIA_17B-ACPO_Type_Pattern', MT598_154_MMID_FIA_17B_ACPO_Type_Pattern)

# Atomic simple type: {http://www.w3schools.com}MT598_154_MMID_95R-CSDP_Type_Pattern
class MT598_154_MMID_95R_CSDP_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_154_MMID_95R-CSDP_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 365, 1)
    _Documentation = None
MT598_154_MMID_95R_CSDP_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT598_154_MMID_95R_CSDP_Type_Pattern._CF_pattern.addPattern(pattern='(:(CSDP)/STRA/[A-Z]{2}[0-9]{6})')
MT598_154_MMID_95R_CSDP_Type_Pattern._InitializeFacetMap(MT598_154_MMID_95R_CSDP_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT598_154_MMID_95R-CSDP_Type_Pattern', MT598_154_MMID_95R_CSDP_Type_Pattern)

# Atomic simple type: {http://www.w3schools.com}MT598_154_MMID_FIA_77B_Type_Pattern
class MT598_154_MMID_FIA_77B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_154_MMID_FIA_77B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 377, 1)
    _Documentation = None
MT598_154_MMID_FIA_77B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT598_154_MMID_FIA_77B_Type_Pattern._CF_pattern.addPattern(pattern='((.{1,35}\\n?){1,3})')
MT598_154_MMID_FIA_77B_Type_Pattern._InitializeFacetMap(MT598_154_MMID_FIA_77B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT598_154_MMID_FIA_77B_Type_Pattern', MT598_154_MMID_FIA_77B_Type_Pattern)

# Atomic simple type: {http://www.w3schools.com}MT598_154_MMID_FIA_17B-WITI_Type_Pattern
class MT598_154_MMID_FIA_17B_WITI_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_154_MMID_FIA_17B-WITI_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 389, 1)
    _Documentation = None
MT598_154_MMID_FIA_17B_WITI_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT598_154_MMID_FIA_17B_WITI_Type_Pattern._CF_pattern.addPattern(pattern='(:(WITI)//(Y|N))')
MT598_154_MMID_FIA_17B_WITI_Type_Pattern._InitializeFacetMap(MT598_154_MMID_FIA_17B_WITI_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT598_154_MMID_FIA_17B-WITI_Type_Pattern', MT598_154_MMID_FIA_17B_WITI_Type_Pattern)

# Atomic simple type: {http://www.w3schools.com}MT598_154_MMID_FIA_95R_Type_Pattern
class MT598_154_MMID_FIA_95R_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_154_MMID_FIA_95R_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 401, 1)
    _Documentation = None
MT598_154_MMID_FIA_95R_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT598_154_MMID_FIA_95R_Type_Pattern._CF_pattern.addPattern(pattern='(:(ACCP)/STRA/[A-Z]{2}[0-9]{6})')
MT598_154_MMID_FIA_95R_Type_Pattern._InitializeFacetMap(MT598_154_MMID_FIA_95R_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT598_154_MMID_FIA_95R_Type_Pattern', MT598_154_MMID_FIA_95R_Type_Pattern)

# Atomic simple type: {http://www.w3schools.com}MT598_154_MMID_95R-ISSR_Type_Pattern
class MT598_154_MMID_95R_ISSR_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_154_MMID_95R-ISSR_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 413, 1)
    _Documentation = None
MT598_154_MMID_95R_ISSR_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT598_154_MMID_95R_ISSR_Type_Pattern._CF_pattern.addPattern(pattern='(:(ISSR)/STRA/[A-Z]{2}[0-9]{6})')
MT598_154_MMID_95R_ISSR_Type_Pattern._InitializeFacetMap(MT598_154_MMID_95R_ISSR_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT598_154_MMID_95R-ISSR_Type_Pattern', MT598_154_MMID_95R_ISSR_Type_Pattern)

# Atomic simple type: {http://www.w3schools.com}MT598_154_MMID_FIA_22F-PFRE_Type_Pattern
class MT598_154_MMID_FIA_22F_PFRE_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_154_MMID_FIA_22F-PFRE_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 425, 1)
    _Documentation = None
MT598_154_MMID_FIA_22F_PFRE_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT598_154_MMID_FIA_22F_PFRE_Type_Pattern._CF_pattern.addPattern(pattern='(:(PFRE)/STRA/(DAYC|ANNU|MNTH|QUTR|SEMI|TERM|ISDF))')
MT598_154_MMID_FIA_22F_PFRE_Type_Pattern._InitializeFacetMap(MT598_154_MMID_FIA_22F_PFRE_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT598_154_MMID_FIA_22F-PFRE_Type_Pattern', MT598_154_MMID_FIA_22F_PFRE_Type_Pattern)

# Atomic simple type: {http://www.w3schools.com}MT598_154_MMID_FIA_13B-CCYC_Type_Pattern
class MT598_154_MMID_FIA_13B_CCYC_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_154_MMID_FIA_13B-CCYC_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 437, 1)
    _Documentation = None
MT598_154_MMID_FIA_13B_CCYC_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT598_154_MMID_FIA_13B_CCYC_Type_Pattern._CF_pattern.addPattern(pattern='(:(CCYC)/STRA/[0-9]{1,3})')
MT598_154_MMID_FIA_13B_CCYC_Type_Pattern._InitializeFacetMap(MT598_154_MMID_FIA_13B_CCYC_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT598_154_MMID_FIA_13B-CCYC_Type_Pattern', MT598_154_MMID_FIA_13B_CCYC_Type_Pattern)

# Atomic simple type: {http://www.w3schools.com}MT598_154_MMID_FIA_22F-RTYP_Type_Pattern
class MT598_154_MMID_FIA_22F_RTYP_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_154_MMID_FIA_22F-RTYP_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 449, 1)
    _Documentation = None
MT598_154_MMID_FIA_22F_RTYP_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT598_154_MMID_FIA_22F_RTYP_Type_Pattern._CF_pattern.addPattern(pattern='(:(RTYP)/STRA/(FIXD|VLIN|VLDY|VNDY))')
MT598_154_MMID_FIA_22F_RTYP_Type_Pattern._InitializeFacetMap(MT598_154_MMID_FIA_22F_RTYP_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT598_154_MMID_FIA_22F-RTYP_Type_Pattern', MT598_154_MMID_FIA_22F_RTYP_Type_Pattern)

# Atomic simple type: {http://www.w3schools.com}MT598_154_MMID_FIA_22H_Type_Pattern
class MT598_154_MMID_FIA_22H_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_154_MMID_FIA_22H_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 461, 1)
    _Documentation = None
MT598_154_MMID_FIA_22H_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT598_154_MMID_FIA_22H_Type_Pattern._CF_pattern.addPattern(pattern='(:(TYPE)//(BA|BL|CPB|PN|TB|ZB|BB|DEB|NCD|LNCD|FRN))')
MT598_154_MMID_FIA_22H_Type_Pattern._InitializeFacetMap(MT598_154_MMID_FIA_22H_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT598_154_MMID_FIA_22H_Type_Pattern', MT598_154_MMID_FIA_22H_Type_Pattern)

# Atomic simple type: {http://www.w3schools.com}MT598_154_GENL_22F-CONF_Type_Pattern
class MT598_154_GENL_22F_CONF_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_154_GENL_22F-CONF_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 473, 1)
    _Documentation = None
MT598_154_GENL_22F_CONF_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT598_154_GENL_22F_CONF_Type_Pattern._CF_pattern.addPattern(pattern='(:(CONF)/STRA/(ISSU|DISS|TOPU|REDU|TAPU|DUPL|TAPR))')
MT598_154_GENL_22F_CONF_Type_Pattern._InitializeFacetMap(MT598_154_GENL_22F_CONF_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT598_154_GENL_22F-CONF_Type_Pattern', MT598_154_GENL_22F_CONF_Type_Pattern)

# Atomic simple type: {http://www.w3schools.com}MT598_154_MMID_FIA_92D_Type_Pattern
class MT598_154_MMID_FIA_92D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_154_MMID_FIA_92D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 485, 1)
    _Documentation = None
MT598_154_MMID_FIA_92D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT598_154_MMID_FIA_92D_Type_Pattern._CF_pattern.addPattern(pattern='(:(FLCP)//[0-9]{1,12},([0-9]{1,2})*/[0-9]{1,12},([0-9]{1,2})*)')
MT598_154_MMID_FIA_92D_Type_Pattern._InitializeFacetMap(MT598_154_MMID_FIA_92D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT598_154_MMID_FIA_92D_Type_Pattern', MT598_154_MMID_FIA_92D_Type_Pattern)

# Atomic simple type: {http://www.w3schools.com}MT598_154_16R_Type
class MT598_154_16R_Type (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_154_16R_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 497, 1)
    _Documentation = None
MT598_154_16R_Type._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'MT598_154_16R_Type', MT598_154_16R_Type)

# Complex type {http://www.w3schools.com}MT598_154_12_Type with content type SIMPLE
class MT598_154_12_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_154_12_Type with content type SIMPLE"""
    _TypeDefinition = pyxb.binding.datatypes.string
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_154_12_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 27, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.string
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_154_12_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='12')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 30, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 30, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_154_12_Type', MT598_154_12_Type)


# Complex type {http://www.w3schools.com}MT598_154_77E_Type with content type SIMPLE
class MT598_154_77E_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_154_77E_Type with content type SIMPLE"""
    _TypeDefinition = pyxb.binding.datatypes.string
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_154_77E_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 214, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.string
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_154_77E_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='77E')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 217, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 217, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_154_77E_Type', MT598_154_77E_Type)


# Complex type {http://www.w3schools.com}MT598_154_MMID_FIA_CRDDET with content type ELEMENT_ONLY
class MT598_154_MMID_FIA_CRDDET (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_154_MMID_FIA_CRDDET with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_154_MMID_FIA_CRDDET')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 500, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}ResetDate uses Python identifier ResetDate
    __ResetDate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ResetDate'), 'ResetDate', '__httpwww_w3schools_com_MT598_154_MMID_FIA_CRDDET_httpwww_w3schools_comResetDate', True, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 502, 3), )

    
    ResetDate = property(__ResetDate.value, __ResetDate.set, None, None)

    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_154_MMID_FIA_CRDDET_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='16R')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 504, 2)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 504, 2)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        __ResetDate.name() : __ResetDate
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_154_MMID_FIA_CRDDET', MT598_154_MMID_FIA_CRDDET)


# Complex type {http://www.w3schools.com}MT598_154_GENL with content type ELEMENT_ONLY
class MT598_154_GENL (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_154_GENL with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_154_GENL')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 506, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}RelatedReference uses Python identifier RelatedReference
    __RelatedReference = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'RelatedReference'), 'RelatedReference', '__httpwww_w3schools_com_MT598_154_GENL_httpwww_w3schools_comRelatedReference', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 508, 3), )

    
    RelatedReference = property(__RelatedReference.value, __RelatedReference.set, None, None)

    
    # Element {http://www.w3schools.com}TypeOfConfirmationIndicator uses Python identifier TypeOfConfirmationIndicator
    __TypeOfConfirmationIndicator = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'TypeOfConfirmationIndicator'), 'TypeOfConfirmationIndicator', '__httpwww_w3schools_com_MT598_154_GENL_httpwww_w3schools_comTypeOfConfirmationIndicator', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 509, 3), )

    
    TypeOfConfirmationIndicator = property(__TypeOfConfirmationIndicator.value, __TypeOfConfirmationIndicator.set, None, None)

    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_154_GENL_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='16R')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 511, 2)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 511, 2)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        __RelatedReference.name() : __RelatedReference,
        __TypeOfConfirmationIndicator.name() : __TypeOfConfirmationIndicator
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_154_GENL', MT598_154_GENL)


# Complex type {http://www.w3schools.com}MT598_154_MMID_FIA with content type ELEMENT_ONLY
class MT598_154_MMID_FIA (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_154_MMID_FIA with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_154_MMID_FIA')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 513, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}CouponPaymentFrequency uses Python identifier CouponPaymentFrequency
    __CouponPaymentFrequency = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'CouponPaymentFrequency'), 'CouponPaymentFrequency', '__httpwww_w3schools_com_MT598_154_MMID_FIA_httpwww_w3schools_comCouponPaymentFrequency', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 515, 3), )

    
    CouponPaymentFrequency = property(__CouponPaymentFrequency.value, __CouponPaymentFrequency.set, None, None)

    
    # Element {http://www.w3schools.com}CouponPaymentDay uses Python identifier CouponPaymentDay
    __CouponPaymentDay = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'CouponPaymentDay'), 'CouponPaymentDay', '__httpwww_w3schools_com_MT598_154_MMID_FIA_httpwww_w3schools_comCouponPaymentDay', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 516, 3), )

    
    CouponPaymentDay = property(__CouponPaymentDay.value, __CouponPaymentDay.set, None, None)

    
    # Element {http://www.w3schools.com}CouponPaymentCycle uses Python identifier CouponPaymentCycle
    __CouponPaymentCycle = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'CouponPaymentCycle'), 'CouponPaymentCycle', '__httpwww_w3schools_com_MT598_154_MMID_FIA_httpwww_w3schools_comCouponPaymentCycle', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 517, 3), )

    
    CouponPaymentCycle = property(__CouponPaymentCycle.value, __CouponPaymentCycle.set, None, None)

    
    # Element {http://www.w3schools.com}GenericCategory uses Python identifier GenericCategory
    __GenericCategory = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'GenericCategory'), 'GenericCategory', '__httpwww_w3schools_com_MT598_154_MMID_FIA_httpwww_w3schools_comGenericCategory', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 518, 3), )

    
    GenericCategory = property(__GenericCategory.value, __GenericCategory.set, None, None)

    
    # Element {http://www.w3schools.com}MMSecurityType uses Python identifier MMSecurityType
    __MMSecurityType = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'MMSecurityType'), 'MMSecurityType', '__httpwww_w3schools_com_MT598_154_MMID_FIA_httpwww_w3schools_comMMSecurityType', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 519, 3), )

    
    MMSecurityType = property(__MMSecurityType.value, __MMSecurityType.set, None, None)

    
    # Element {http://www.w3schools.com}MaturityDate uses Python identifier MaturityDate
    __MaturityDate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'MaturityDate'), 'MaturityDate', '__httpwww_w3schools_com_MT598_154_MMID_FIA_httpwww_w3schools_comMaturityDate', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 520, 3), )

    
    MaturityDate = property(__MaturityDate.value, __MaturityDate.set, None, None)

    
    # Element {http://www.w3schools.com}IssueDate uses Python identifier IssueDate
    __IssueDate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'IssueDate'), 'IssueDate', '__httpwww_w3schools_com_MT598_154_MMID_FIA_httpwww_w3schools_comIssueDate', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 521, 3), )

    
    IssueDate = property(__IssueDate.value, __IssueDate.set, None, None)

    
    # Element {http://www.w3schools.com}InterestRate uses Python identifier InterestRate
    __InterestRate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'InterestRate'), 'InterestRate', '__httpwww_w3schools_com_MT598_154_MMID_FIA_httpwww_w3schools_comInterestRate', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 522, 3), )

    
    InterestRate = property(__InterestRate.value, __InterestRate.set, None, None)

    
    # Element {http://www.w3schools.com}CouponRateTypeIndicator uses Python identifier CouponRateTypeIndicator
    __CouponRateTypeIndicator = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'CouponRateTypeIndicator'), 'CouponRateTypeIndicator', '__httpwww_w3schools_com_MT598_154_MMID_FIA_httpwww_w3schools_comCouponRateTypeIndicator', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 523, 3), )

    
    CouponRateTypeIndicator = property(__CouponRateTypeIndicator.value, __CouponRateTypeIndicator.set, None, None)

    
    # Element {http://www.w3schools.com}MiniumNominalValue uses Python identifier MiniumNominalValue
    __MiniumNominalValue = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'MiniumNominalValue'), 'MiniumNominalValue', '__httpwww_w3schools_com_MT598_154_MMID_FIA_httpwww_w3schools_comMiniumNominalValue', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 524, 3), )

    
    MiniumNominalValue = property(__MiniumNominalValue.value, __MiniumNominalValue.set, None, None)

    
    # Element {http://www.w3schools.com}AuthorisedAmount uses Python identifier AuthorisedAmount
    __AuthorisedAmount = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'AuthorisedAmount'), 'AuthorisedAmount', '__httpwww_w3schools_com_MT598_154_MMID_FIA_httpwww_w3schools_comAuthorisedAmount', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 525, 3), )

    
    AuthorisedAmount = property(__AuthorisedAmount.value, __AuthorisedAmount.set, None, None)

    
    # Element {http://www.w3schools.com}AcceptorOfMMSecurity uses Python identifier AcceptorOfMMSecurity
    __AcceptorOfMMSecurity = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'AcceptorOfMMSecurity'), 'AcceptorOfMMSecurity', '__httpwww_w3schools_com_MT598_154_MMID_FIA_httpwww_w3schools_comAcceptorOfMMSecurity', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 526, 3), )

    
    AcceptorOfMMSecurity = property(__AcceptorOfMMSecurity.value, __AcceptorOfMMSecurity.set, None, None)

    
    # Element {http://www.w3schools.com}MinimumIssuerDenomination uses Python identifier MinimumIssuerDenomination
    __MinimumIssuerDenomination = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'MinimumIssuerDenomination'), 'MinimumIssuerDenomination', '__httpwww_w3schools_com_MT598_154_MMID_FIA_httpwww_w3schools_comMinimumIssuerDenomination', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 527, 3), )

    
    MinimumIssuerDenomination = property(__MinimumIssuerDenomination.value, __MinimumIssuerDenomination.set, None, None)

    
    # Element {http://www.w3schools.com}FloorCapRate uses Python identifier FloorCapRate
    __FloorCapRate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'FloorCapRate'), 'FloorCapRate', '__httpwww_w3schools_com_MT598_154_MMID_FIA_httpwww_w3schools_comFloorCapRate', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 528, 3), )

    
    FloorCapRate = property(__FloorCapRate.value, __FloorCapRate.set, None, None)

    
    # Element {http://www.w3schools.com}CouponPaymentDayIndicator uses Python identifier CouponPaymentDayIndicator
    __CouponPaymentDayIndicator = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'CouponPaymentDayIndicator'), 'CouponPaymentDayIndicator', '__httpwww_w3schools_com_MT598_154_MMID_FIA_httpwww_w3schools_comCouponPaymentDayIndicator', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 529, 3), )

    
    CouponPaymentDayIndicator = property(__CouponPaymentDayIndicator.value, __CouponPaymentDayIndicator.set, None, None)

    
    # Element {http://www.w3schools.com}WITI uses Python identifier WITI
    __WITI = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'WITI'), 'WITI', '__httpwww_w3schools_com_MT598_154_MMID_FIA_httpwww_w3schools_comWITI', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 530, 3), )

    
    WITI = property(__WITI.value, __WITI.set, None, None)

    
    # Element {http://www.w3schools.com}WithholdingTaxOnInterestRate uses Python identifier WithholdingTaxOnInterestRate
    __WithholdingTaxOnInterestRate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'WithholdingTaxOnInterestRate'), 'WithholdingTaxOnInterestRate', '__httpwww_w3schools_com_MT598_154_MMID_FIA_httpwww_w3schools_comWithholdingTaxOnInterestRate', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 531, 3), )

    
    WithholdingTaxOnInterestRate = property(__WithholdingTaxOnInterestRate.value, __WithholdingTaxOnInterestRate.set, None, None)

    
    # Element {http://www.w3schools.com}FinalCouponPaymentOnMaturity uses Python identifier FinalCouponPaymentOnMaturity
    __FinalCouponPaymentOnMaturity = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'FinalCouponPaymentOnMaturity'), 'FinalCouponPaymentOnMaturity', '__httpwww_w3schools_com_MT598_154_MMID_FIA_httpwww_w3schools_comFinalCouponPaymentOnMaturity', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 532, 3), )

    
    FinalCouponPaymentOnMaturity = property(__FinalCouponPaymentOnMaturity.value, __FinalCouponPaymentOnMaturity.set, None, None)

    
    # Element {http://www.w3schools.com}CouponPaymentIndicator uses Python identifier CouponPaymentIndicator
    __CouponPaymentIndicator = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'CouponPaymentIndicator'), 'CouponPaymentIndicator', '__httpwww_w3schools_com_MT598_154_MMID_FIA_httpwww_w3schools_comCouponPaymentIndicator', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 533, 3), )

    
    CouponPaymentIndicator = property(__CouponPaymentIndicator.value, __CouponPaymentIndicator.set, None, None)

    
    # Element {http://www.w3schools.com}AutomatedCouponPaymentCalculation uses Python identifier AutomatedCouponPaymentCalculation
    __AutomatedCouponPaymentCalculation = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'AutomatedCouponPaymentCalculation'), 'AutomatedCouponPaymentCalculation', '__httpwww_w3schools_com_MT598_154_MMID_FIA_httpwww_w3schools_comAutomatedCouponPaymentCalculation', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 534, 3), )

    
    AutomatedCouponPaymentCalculation = property(__AutomatedCouponPaymentCalculation.value, __AutomatedCouponPaymentCalculation.set, None, None)

    
    # Element {http://www.w3schools.com}AutomatedCouponPaymentOnly uses Python identifier AutomatedCouponPaymentOnly
    __AutomatedCouponPaymentOnly = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'AutomatedCouponPaymentOnly'), 'AutomatedCouponPaymentOnly', '__httpwww_w3schools_com_MT598_154_MMID_FIA_httpwww_w3schools_comAutomatedCouponPaymentOnly', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 535, 3), )

    
    AutomatedCouponPaymentOnly = property(__AutomatedCouponPaymentOnly.value, __AutomatedCouponPaymentOnly.set, None, None)

    
    # Element {http://www.w3schools.com}CouponRateCalculationDescription uses Python identifier CouponRateCalculationDescription
    __CouponRateCalculationDescription = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'CouponRateCalculationDescription'), 'CouponRateCalculationDescription', '__httpwww_w3schools_com_MT598_154_MMID_FIA_httpwww_w3schools_comCouponRateCalculationDescription', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 536, 3), )

    
    CouponRateCalculationDescription = property(__CouponRateCalculationDescription.value, __CouponRateCalculationDescription.set, None, None)

    
    # Element {http://www.w3schools.com}OverrideIndicator uses Python identifier OverrideIndicator
    __OverrideIndicator = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'OverrideIndicator'), 'OverrideIndicator', '__httpwww_w3schools_com_MT598_154_MMID_FIA_httpwww_w3schools_comOverrideIndicator', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 537, 3), )

    
    OverrideIndicator = property(__OverrideIndicator.value, __OverrideIndicator.set, None, None)

    
    # Element {http://www.w3schools.com}CouponPaymentCalculationMethod uses Python identifier CouponPaymentCalculationMethod
    __CouponPaymentCalculationMethod = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'CouponPaymentCalculationMethod'), 'CouponPaymentCalculationMethod', '__httpwww_w3schools_com_MT598_154_MMID_FIA_httpwww_w3schools_comCouponPaymentCalculationMethod', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 538, 3), )

    
    CouponPaymentCalculationMethod = property(__CouponPaymentCalculationMethod.value, __CouponPaymentCalculationMethod.set, None, None)

    
    # Element {http://www.w3schools.com}CouponRateSource uses Python identifier CouponRateSource
    __CouponRateSource = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'CouponRateSource'), 'CouponRateSource', '__httpwww_w3schools_com_MT598_154_MMID_FIA_httpwww_w3schools_comCouponRateSource', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 539, 3), )

    
    CouponRateSource = property(__CouponRateSource.value, __CouponRateSource.set, None, None)

    
    # Element {http://www.w3schools.com}CouponRateVarianceFromSource uses Python identifier CouponRateVarianceFromSource
    __CouponRateVarianceFromSource = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'CouponRateVarianceFromSource'), 'CouponRateVarianceFromSource', '__httpwww_w3schools_com_MT598_154_MMID_FIA_httpwww_w3schools_comCouponRateVarianceFromSource', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 540, 3), )

    
    CouponRateVarianceFromSource = property(__CouponRateVarianceFromSource.value, __CouponRateVarianceFromSource.set, None, None)

    
    # Element {http://www.w3schools.com}CouponCompoundFrequency uses Python identifier CouponCompoundFrequency
    __CouponCompoundFrequency = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'CouponCompoundFrequency'), 'CouponCompoundFrequency', '__httpwww_w3schools_com_MT598_154_MMID_FIA_httpwww_w3schools_comCouponCompoundFrequency', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 541, 3), )

    
    CouponCompoundFrequency = property(__CouponCompoundFrequency.value, __CouponCompoundFrequency.set, None, None)

    
    # Element {http://www.w3schools.com}CouponResetFrequency uses Python identifier CouponResetFrequency
    __CouponResetFrequency = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'CouponResetFrequency'), 'CouponResetFrequency', '__httpwww_w3schools_com_MT598_154_MMID_FIA_httpwww_w3schools_comCouponResetFrequency', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 542, 3), )

    
    CouponResetFrequency = property(__CouponResetFrequency.value, __CouponResetFrequency.set, None, None)

    
    # Element {http://www.w3schools.com}CouponResetStartDate uses Python identifier CouponResetStartDate
    __CouponResetStartDate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'CouponResetStartDate'), 'CouponResetStartDate', '__httpwww_w3schools_com_MT598_154_MMID_FIA_httpwww_w3schools_comCouponResetStartDate', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 543, 3), )

    
    CouponResetStartDate = property(__CouponResetStartDate.value, __CouponResetStartDate.set, None, None)

    
    # Element {http://www.w3schools.com}CRDDET uses Python identifier CRDDET
    __CRDDET = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'CRDDET'), 'CRDDET', '__httpwww_w3schools_com_MT598_154_MMID_FIA_httpwww_w3schools_comCRDDET', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 544, 3), )

    
    CRDDET = property(__CRDDET.value, __CRDDET.set, None, None)

    
    # Element {http://www.w3schools.com}CPDDET uses Python identifier CPDDET
    __CPDDET = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'CPDDET'), 'CPDDET', '__httpwww_w3schools_com_MT598_154_MMID_FIA_httpwww_w3schools_comCPDDET', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 545, 3), )

    
    CPDDET = property(__CPDDET.value, __CPDDET.set, None, None)

    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_154_MMID_FIA_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='16R')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 547, 2)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 547, 2)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        __CouponPaymentFrequency.name() : __CouponPaymentFrequency,
        __CouponPaymentDay.name() : __CouponPaymentDay,
        __CouponPaymentCycle.name() : __CouponPaymentCycle,
        __GenericCategory.name() : __GenericCategory,
        __MMSecurityType.name() : __MMSecurityType,
        __MaturityDate.name() : __MaturityDate,
        __IssueDate.name() : __IssueDate,
        __InterestRate.name() : __InterestRate,
        __CouponRateTypeIndicator.name() : __CouponRateTypeIndicator,
        __MiniumNominalValue.name() : __MiniumNominalValue,
        __AuthorisedAmount.name() : __AuthorisedAmount,
        __AcceptorOfMMSecurity.name() : __AcceptorOfMMSecurity,
        __MinimumIssuerDenomination.name() : __MinimumIssuerDenomination,
        __FloorCapRate.name() : __FloorCapRate,
        __CouponPaymentDayIndicator.name() : __CouponPaymentDayIndicator,
        __WITI.name() : __WITI,
        __WithholdingTaxOnInterestRate.name() : __WithholdingTaxOnInterestRate,
        __FinalCouponPaymentOnMaturity.name() : __FinalCouponPaymentOnMaturity,
        __CouponPaymentIndicator.name() : __CouponPaymentIndicator,
        __AutomatedCouponPaymentCalculation.name() : __AutomatedCouponPaymentCalculation,
        __AutomatedCouponPaymentOnly.name() : __AutomatedCouponPaymentOnly,
        __CouponRateCalculationDescription.name() : __CouponRateCalculationDescription,
        __OverrideIndicator.name() : __OverrideIndicator,
        __CouponPaymentCalculationMethod.name() : __CouponPaymentCalculationMethod,
        __CouponRateSource.name() : __CouponRateSource,
        __CouponRateVarianceFromSource.name() : __CouponRateVarianceFromSource,
        __CouponCompoundFrequency.name() : __CouponCompoundFrequency,
        __CouponResetFrequency.name() : __CouponResetFrequency,
        __CouponResetStartDate.name() : __CouponResetStartDate,
        __CRDDET.name() : __CRDDET,
        __CPDDET.name() : __CPDDET
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_154_MMID_FIA', MT598_154_MMID_FIA)


# Complex type {http://www.w3schools.com}MT598_154_MMID with content type ELEMENT_ONLY
class MT598_154_MMID (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_154_MMID with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_154_MMID')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 549, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}IssuersCSDParticipantCode uses Python identifier IssuersCSDParticipantCode
    __IssuersCSDParticipantCode = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'IssuersCSDParticipantCode'), 'IssuersCSDParticipantCode', '__httpwww_w3schools_com_MT598_154_MMID_httpwww_w3schools_comIssuersCSDParticipantCode', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 551, 3), )

    
    IssuersCSDParticipantCode = property(__IssuersCSDParticipantCode.value, __IssuersCSDParticipantCode.set, None, None)

    
    # Element {http://www.w3schools.com}IssuersParticipantCode uses Python identifier IssuersParticipantCode
    __IssuersParticipantCode = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'IssuersParticipantCode'), 'IssuersParticipantCode', '__httpwww_w3schools_com_MT598_154_MMID_httpwww_w3schools_comIssuersParticipantCode', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 552, 3), )

    
    IssuersParticipantCode = property(__IssuersParticipantCode.value, __IssuersParticipantCode.set, None, None)

    
    # Element {http://www.w3schools.com}IssuingAgentsParticipantCode uses Python identifier IssuingAgentsParticipantCode
    __IssuingAgentsParticipantCode = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'IssuingAgentsParticipantCode'), 'IssuingAgentsParticipantCode', '__httpwww_w3schools_com_MT598_154_MMID_httpwww_w3schools_comIssuingAgentsParticipantCode', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 553, 3), )

    
    IssuingAgentsParticipantCode = property(__IssuingAgentsParticipantCode.value, __IssuingAgentsParticipantCode.set, None, None)

    
    # Element {http://www.w3schools.com}IdenitficationOfSecurities uses Python identifier IdenitficationOfSecurities
    __IdenitficationOfSecurities = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'IdenitficationOfSecurities'), 'IdenitficationOfSecurities', '__httpwww_w3schools_com_MT598_154_MMID_httpwww_w3schools_comIdenitficationOfSecurities', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 554, 3), )

    
    IdenitficationOfSecurities = property(__IdenitficationOfSecurities.value, __IdenitficationOfSecurities.set, None, None)

    
    # Element {http://www.w3schools.com}NominalValueIssued uses Python identifier NominalValueIssued
    __NominalValueIssued = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'NominalValueIssued'), 'NominalValueIssued', '__httpwww_w3schools_com_MT598_154_MMID_httpwww_w3schools_comNominalValueIssued', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 555, 3), )

    
    NominalValueIssued = property(__NominalValueIssued.value, __NominalValueIssued.set, None, None)

    
    # Element {http://www.w3schools.com}IssuersSORAccountAtCSD uses Python identifier IssuersSORAccountAtCSD
    __IssuersSORAccountAtCSD = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'IssuersSORAccountAtCSD'), 'IssuersSORAccountAtCSD', '__httpwww_w3schools_com_MT598_154_MMID_httpwww_w3schools_comIssuersSORAccountAtCSD', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 556, 3), )

    
    IssuersSORAccountAtCSD = property(__IssuersSORAccountAtCSD.value, __IssuersSORAccountAtCSD.set, None, None)

    
    # Element {http://www.w3schools.com}FIA uses Python identifier FIA
    __FIA = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'FIA'), 'FIA', '__httpwww_w3schools_com_MT598_154_MMID_httpwww_w3schools_comFIA', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 557, 3), )

    
    FIA = property(__FIA.value, __FIA.set, None, None)

    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_154_MMID_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='16R')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 559, 2)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 559, 2)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        __IssuersCSDParticipantCode.name() : __IssuersCSDParticipantCode,
        __IssuersParticipantCode.name() : __IssuersParticipantCode,
        __IssuingAgentsParticipantCode.name() : __IssuingAgentsParticipantCode,
        __IdenitficationOfSecurities.name() : __IdenitficationOfSecurities,
        __NominalValueIssued.name() : __NominalValueIssued,
        __IssuersSORAccountAtCSD.name() : __IssuersSORAccountAtCSD,
        __FIA.name() : __FIA
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_154_MMID', MT598_154_MMID)


# Complex type {http://www.w3schools.com}MT598_154_MMID_FIA_CPDDET with content type ELEMENT_ONLY
class MT598_154_MMID_FIA_CPDDET (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_154_MMID_FIA_CPDDET with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_154_MMID_FIA_CPDDET')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 561, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}PaymentDate uses Python identifier PaymentDate
    __PaymentDate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PaymentDate'), 'PaymentDate', '__httpwww_w3schools_com_MT598_154_MMID_FIA_CPDDET_httpwww_w3schools_comPaymentDate', True, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 563, 3), )

    
    PaymentDate = property(__PaymentDate.value, __PaymentDate.set, None, None)

    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_154_MMID_FIA_CPDDET_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='16R')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 565, 2)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 565, 2)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        __PaymentDate.name() : __PaymentDate
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_154_MMID_FIA_CPDDET', MT598_154_MMID_FIA_CPDDET)


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 568, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}TransactionReference uses Python identifier TransactionReference
    __TransactionReference = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'TransactionReference'), 'TransactionReference', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comTransactionReference', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 570, 4), )

    
    TransactionReference = property(__TransactionReference.value, __TransactionReference.set, None, None)

    
    # Element {http://www.w3schools.com}SubMessageType uses Python identifier SubMessageType
    __SubMessageType = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SubMessageType'), 'SubMessageType', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comSubMessageType', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 571, 4), )

    
    SubMessageType = property(__SubMessageType.value, __SubMessageType.set, None, None)

    
    # Element {http://www.w3schools.com}ProprietaryMessage uses Python identifier ProprietaryMessage
    __ProprietaryMessage = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ProprietaryMessage'), 'ProprietaryMessage', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comProprietaryMessage', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 572, 4), )

    
    ProprietaryMessage = property(__ProprietaryMessage.value, __ProprietaryMessage.set, None, None)

    
    # Element {http://www.w3schools.com}GENL uses Python identifier GENL
    __GENL = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'GENL'), 'GENL', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comGENL', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 573, 4), )

    
    GENL = property(__GENL.value, __GENL.set, None, None)

    
    # Element {http://www.w3schools.com}MMID uses Python identifier MMID
    __MMID = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'MMID'), 'MMID', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comMMID', False, pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 574, 4), )

    
    MMID = property(__MMID.value, __MMID.set, None, None)

    _ElementMap.update({
        __TransactionReference.name() : __TransactionReference,
        __SubMessageType.name() : __SubMessageType,
        __ProprietaryMessage.name() : __ProprietaryMessage,
        __GENL.name() : __GENL,
        __MMID.name() : __MMID
    })
    _AttributeMap.update({
        
    })



# Complex type {http://www.w3schools.com}MT598_154_MMID_FIA_22F-CCFR_Type with content type SIMPLE
class MT598_154_MMID_FIA_22F_CCFR_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_154_MMID_FIA_22F-CCFR_Type with content type SIMPLE"""
    _TypeDefinition = MT598_154_MMID_FIA_22F_CCFR_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_154_MMID_FIA_22F-CCFR_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 8, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT598_154_MMID_FIA_22F_CCFR_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_154_MMID_FIA_22F_CCFR_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='22F')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 11, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 11, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_154_MMID_FIA_22F-CCFR_Type', MT598_154_MMID_FIA_22F_CCFR_Type)


# Complex type {http://www.w3schools.com}MT598_154_MMID_95R-ISSA_Type with content type SIMPLE
class MT598_154_MMID_95R_ISSA_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_154_MMID_95R-ISSA_Type with content type SIMPLE"""
    _TypeDefinition = MT598_154_MMID_95R_ISSA_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_154_MMID_95R-ISSA_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 20, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT598_154_MMID_95R_ISSA_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_154_MMID_95R_ISSA_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='95R')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 23, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 23, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_154_MMID_95R-ISSA_Type', MT598_154_MMID_95R_ISSA_Type)


# Complex type {http://www.w3schools.com}MT598_154_MMID_FIA_17B-CPMI_Type with content type SIMPLE
class MT598_154_MMID_FIA_17B_CPMI_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_154_MMID_FIA_17B-CPMI_Type with content type SIMPLE"""
    _TypeDefinition = MT598_154_MMID_FIA_17B_CPMI_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_154_MMID_FIA_17B-CPMI_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 39, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT598_154_MMID_FIA_17B_CPMI_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_154_MMID_FIA_17B_CPMI_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='17B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 42, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 42, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_154_MMID_FIA_17B-CPMI_Type', MT598_154_MMID_FIA_17B_CPMI_Type)


# Complex type {http://www.w3schools.com}MT598_154_MMID_FIA_13B-CPYD_Type with content type SIMPLE
class MT598_154_MMID_FIA_13B_CPYD_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_154_MMID_FIA_13B-CPYD_Type with content type SIMPLE"""
    _TypeDefinition = MT598_154_MMID_FIA_13B_CPYD_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_154_MMID_FIA_13B-CPYD_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 51, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT598_154_MMID_FIA_13B_CPYD_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_154_MMID_FIA_13B_CPYD_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='13B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 54, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 54, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_154_MMID_FIA_13B-CPYD_Type', MT598_154_MMID_FIA_13B_CPYD_Type)


# Complex type {http://www.w3schools.com}MT598_154_MMID_FIA_CPDDET_98A_Type with content type SIMPLE
class MT598_154_MMID_FIA_CPDDET_98A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_154_MMID_FIA_CPDDET_98A_Type with content type SIMPLE"""
    _TypeDefinition = MT598_154_MMID_FIA_CPDDET_98A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_154_MMID_FIA_CPDDET_98A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 63, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT598_154_MMID_FIA_CPDDET_98A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_154_MMID_FIA_CPDDET_98A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='98A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 66, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 66, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_154_MMID_FIA_CPDDET_98A_Type', MT598_154_MMID_FIA_CPDDET_98A_Type)


# Complex type {http://www.w3schools.com}MT598_154_MMID_FIA_36B-AUTH_Type with content type SIMPLE
class MT598_154_MMID_FIA_36B_AUTH_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_154_MMID_FIA_36B-AUTH_Type with content type SIMPLE"""
    _TypeDefinition = MT598_154_MMID_FIA_36B_AUTH_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_154_MMID_FIA_36B-AUTH_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 75, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT598_154_MMID_FIA_36B_AUTH_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_154_MMID_FIA_36B_AUTH_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='36B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 78, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 78, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_154_MMID_FIA_36B-AUTH_Type', MT598_154_MMID_FIA_36B_AUTH_Type)


# Complex type {http://www.w3schools.com}MT598_154_MMID_FIA_98A-CRSD_Type with content type SIMPLE
class MT598_154_MMID_FIA_98A_CRSD_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_154_MMID_FIA_98A-CRSD_Type with content type SIMPLE"""
    _TypeDefinition = MT598_154_MMID_FIA_98A_CRSD_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_154_MMID_FIA_98A-CRSD_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 87, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT598_154_MMID_FIA_98A_CRSD_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_154_MMID_FIA_98A_CRSD_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='98A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 90, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 90, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_154_MMID_FIA_98A-CRSD_Type', MT598_154_MMID_FIA_98A_CRSD_Type)


# Complex type {http://www.w3schools.com}MT598_154_MMID_FIA_36B-MINI_Type with content type SIMPLE
class MT598_154_MMID_FIA_36B_MINI_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_154_MMID_FIA_36B-MINI_Type with content type SIMPLE"""
    _TypeDefinition = MT598_154_MMID_FIA_36B_MINI_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_154_MMID_FIA_36B-MINI_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 99, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT598_154_MMID_FIA_36B_MINI_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_154_MMID_FIA_36B_MINI_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='36B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 102, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 102, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_154_MMID_FIA_36B-MINI_Type', MT598_154_MMID_FIA_36B_MINI_Type)


# Complex type {http://www.w3schools.com}MT598_154_MMID_FIA_92A-TAXR_Type with content type SIMPLE
class MT598_154_MMID_FIA_92A_TAXR_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_154_MMID_FIA_92A-TAXR_Type with content type SIMPLE"""
    _TypeDefinition = MT598_154_MMID_FIA_92A_TAXR_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_154_MMID_FIA_92A-TAXR_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 111, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT598_154_MMID_FIA_92A_TAXR_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_154_MMID_FIA_92A_TAXR_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='92A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 114, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 114, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_154_MMID_FIA_92A-TAXR_Type', MT598_154_MMID_FIA_92A_TAXR_Type)


# Complex type {http://www.w3schools.com}MT598_154_MMID_FIA_22F-CPDI_Type with content type SIMPLE
class MT598_154_MMID_FIA_22F_CPDI_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_154_MMID_FIA_22F-CPDI_Type with content type SIMPLE"""
    _TypeDefinition = MT598_154_MMID_FIA_22F_CPDI_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_154_MMID_FIA_22F-CPDI_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 123, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT598_154_MMID_FIA_22F_CPDI_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_154_MMID_FIA_22F_CPDI_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='22F')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 126, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 126, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_154_MMID_FIA_22F-CPDI_Type', MT598_154_MMID_FIA_22F_CPDI_Type)


# Complex type {http://www.w3schools.com}MT598_154_20_Type with content type SIMPLE
class MT598_154_20_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_154_20_Type with content type SIMPLE"""
    _TypeDefinition = MT598_154_20_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_154_20_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 135, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT598_154_20_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_154_20_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='20')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 138, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 138, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_154_20_Type', MT598_154_20_Type)


# Complex type {http://www.w3schools.com}MT598_154_MMID_35B_Type with content type SIMPLE
class MT598_154_MMID_35B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_154_MMID_35B_Type with content type SIMPLE"""
    _TypeDefinition = MT598_154_MMID_35B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_154_MMID_35B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 147, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT598_154_MMID_35B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_154_MMID_35B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='35B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 150, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 150, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_154_MMID_35B_Type', MT598_154_MMID_35B_Type)


# Complex type {http://www.w3schools.com}MT598_154_MMID_FIA_14F_Type with content type SIMPLE
class MT598_154_MMID_FIA_14F_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_154_MMID_FIA_14F_Type with content type SIMPLE"""
    _TypeDefinition = MT598_154_MMID_FIA_14F_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_154_MMID_FIA_14F_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 159, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT598_154_MMID_FIA_14F_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_154_MMID_FIA_14F_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='14F')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 162, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 162, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_154_MMID_FIA_14F_Type', MT598_154_MMID_FIA_14F_Type)


# Complex type {http://www.w3schools.com}MT598_154_MMID_FIA_CRDDET_98A_Type with content type SIMPLE
class MT598_154_MMID_FIA_CRDDET_98A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_154_MMID_FIA_CRDDET_98A_Type with content type SIMPLE"""
    _TypeDefinition = MT598_154_MMID_FIA_CRDDET_98A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_154_MMID_FIA_CRDDET_98A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 171, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT598_154_MMID_FIA_CRDDET_98A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_154_MMID_FIA_CRDDET_98A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='98A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 174, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 174, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_154_MMID_FIA_CRDDET_98A_Type', MT598_154_MMID_FIA_CRDDET_98A_Type)


# Complex type {http://www.w3schools.com}MT598_154_MMID_FIA_25_Type with content type SIMPLE
class MT598_154_MMID_FIA_25_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_154_MMID_FIA_25_Type with content type SIMPLE"""
    _TypeDefinition = MT598_154_MMID_FIA_25_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_154_MMID_FIA_25_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 183, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT598_154_MMID_FIA_25_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_154_MMID_FIA_25_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='25')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 186, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 186, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_154_MMID_FIA_25_Type', MT598_154_MMID_FIA_25_Type)


# Complex type {http://www.w3schools.com}MT598_154_MMID_FIA_98A-MATU_Type with content type SIMPLE
class MT598_154_MMID_FIA_98A_MATU_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_154_MMID_FIA_98A-MATU_Type with content type SIMPLE"""
    _TypeDefinition = MT598_154_MMID_FIA_98A_MATU_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_154_MMID_FIA_98A-MATU_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 195, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT598_154_MMID_FIA_98A_MATU_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_154_MMID_FIA_98A_MATU_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='98A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 198, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 198, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_154_MMID_FIA_98A-MATU_Type', MT598_154_MMID_FIA_98A_MATU_Type)


# Complex type {http://www.w3schools.com}MT598_154_MMID_36B-QISS_Type with content type SIMPLE
class MT598_154_MMID_36B_QISS_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_154_MMID_36B-QISS_Type with content type SIMPLE"""
    _TypeDefinition = MT598_154_MMID_36B_QISS_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_154_MMID_36B-QISS_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 207, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT598_154_MMID_36B_QISS_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_154_MMID_36B_QISS_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='36B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 210, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 210, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_154_MMID_36B-QISS_Type', MT598_154_MMID_36B_QISS_Type)


# Complex type {http://www.w3schools.com}MT598_154_MMID_FIA_36B-MINO_Type with content type SIMPLE
class MT598_154_MMID_FIA_36B_MINO_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_154_MMID_FIA_36B-MINO_Type with content type SIMPLE"""
    _TypeDefinition = MT598_154_MMID_FIA_36B_MINO_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_154_MMID_FIA_36B-MINO_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 226, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT598_154_MMID_FIA_36B_MINO_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_154_MMID_FIA_36B_MINO_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='36B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 229, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 229, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_154_MMID_FIA_36B-MINO_Type', MT598_154_MMID_FIA_36B_MINO_Type)


# Complex type {http://www.w3schools.com}MT598_154_MMID_FIA_13B-CPCM_Type with content type SIMPLE
class MT598_154_MMID_FIA_13B_CPCM_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_154_MMID_FIA_13B-CPCM_Type with content type SIMPLE"""
    _TypeDefinition = MT598_154_MMID_FIA_13B_CPCM_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_154_MMID_FIA_13B-CPCM_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 238, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT598_154_MMID_FIA_13B_CPCM_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_154_MMID_FIA_13B_CPCM_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='13B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 241, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 241, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_154_MMID_FIA_13B-CPCM_Type', MT598_154_MMID_FIA_13B_CPCM_Type)


# Complex type {http://www.w3schools.com}MT598_154_MMID_FIA_12A_Type with content type SIMPLE
class MT598_154_MMID_FIA_12A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_154_MMID_FIA_12A_Type with content type SIMPLE"""
    _TypeDefinition = MT598_154_MMID_FIA_12A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_154_MMID_FIA_12A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 250, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT598_154_MMID_FIA_12A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_154_MMID_FIA_12A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='12A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 253, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 253, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_154_MMID_FIA_12A_Type', MT598_154_MMID_FIA_12A_Type)


# Complex type {http://www.w3schools.com}MT598_154_MMID_FIA_98A-ISSU_Type with content type SIMPLE
class MT598_154_MMID_FIA_98A_ISSU_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_154_MMID_FIA_98A-ISSU_Type with content type SIMPLE"""
    _TypeDefinition = MT598_154_MMID_FIA_98A_ISSU_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_154_MMID_FIA_98A-ISSU_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 262, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT598_154_MMID_FIA_98A_ISSU_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_154_MMID_FIA_98A_ISSU_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='98A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 265, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 265, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_154_MMID_FIA_98A-ISSU_Type', MT598_154_MMID_FIA_98A_ISSU_Type)


# Complex type {http://www.w3schools.com}MT598_154_MMID_FIA_17B-ACPC_Type with content type SIMPLE
class MT598_154_MMID_FIA_17B_ACPC_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_154_MMID_FIA_17B-ACPC_Type with content type SIMPLE"""
    _TypeDefinition = MT598_154_MMID_FIA_17B_ACPC_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_154_MMID_FIA_17B-ACPC_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 274, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT598_154_MMID_FIA_17B_ACPC_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_154_MMID_FIA_17B_ACPC_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='17B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 277, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 277, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_154_MMID_FIA_17B-ACPC_Type', MT598_154_MMID_FIA_17B_ACPC_Type)


# Complex type {http://www.w3schools.com}MT598_154_GENL_20C_Type with content type SIMPLE
class MT598_154_GENL_20C_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_154_GENL_20C_Type with content type SIMPLE"""
    _TypeDefinition = MT598_154_GENL_20C_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_154_GENL_20C_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 286, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT598_154_GENL_20C_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_154_GENL_20C_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='20C')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 289, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 289, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_154_GENL_20C_Type', MT598_154_GENL_20C_Type)


# Complex type {http://www.w3schools.com}MT598_154_MMID_FIA_22F-RESF_Type with content type SIMPLE
class MT598_154_MMID_FIA_22F_RESF_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_154_MMID_FIA_22F-RESF_Type with content type SIMPLE"""
    _TypeDefinition = MT598_154_MMID_FIA_22F_RESF_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_154_MMID_FIA_22F-RESF_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 298, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT598_154_MMID_FIA_22F_RESF_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_154_MMID_FIA_22F_RESF_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='22F')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 301, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 301, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_154_MMID_FIA_22F-RESF_Type', MT598_154_MMID_FIA_22F_RESF_Type)


# Complex type {http://www.w3schools.com}MT598_154_MMID_97B_Type with content type SIMPLE
class MT598_154_MMID_97B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_154_MMID_97B_Type with content type SIMPLE"""
    _TypeDefinition = MT598_154_MMID_97B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_154_MMID_97B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 310, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT598_154_MMID_97B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_154_MMID_97B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='97B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 313, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 313, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_154_MMID_97B_Type', MT598_154_MMID_97B_Type)


# Complex type {http://www.w3schools.com}MT598_154_MMID_FIA_92A-INTR_Type with content type SIMPLE
class MT598_154_MMID_FIA_92A_INTR_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_154_MMID_FIA_92A-INTR_Type with content type SIMPLE"""
    _TypeDefinition = MT598_154_MMID_FIA_92A_INTR_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_154_MMID_FIA_92A-INTR_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 322, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT598_154_MMID_FIA_92A_INTR_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_154_MMID_FIA_92A_INTR_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='92A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 325, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 325, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_154_MMID_FIA_92A-INTR_Type', MT598_154_MMID_FIA_92A_INTR_Type)


# Complex type {http://www.w3schools.com}MT598_154_MMID_FIA_17B-FCPM_Type with content type SIMPLE
class MT598_154_MMID_FIA_17B_FCPM_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_154_MMID_FIA_17B-FCPM_Type with content type SIMPLE"""
    _TypeDefinition = MT598_154_MMID_FIA_17B_FCPM_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_154_MMID_FIA_17B-FCPM_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 334, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT598_154_MMID_FIA_17B_FCPM_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_154_MMID_FIA_17B_FCPM_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='17B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 337, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 337, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_154_MMID_FIA_17B-FCPM_Type', MT598_154_MMID_FIA_17B_FCPM_Type)


# Complex type {http://www.w3schools.com}MT598_154_MMID_FIA_17B-OVER_Type with content type SIMPLE
class MT598_154_MMID_FIA_17B_OVER_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_154_MMID_FIA_17B-OVER_Type with content type SIMPLE"""
    _TypeDefinition = MT598_154_MMID_FIA_17B_OVER_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_154_MMID_FIA_17B-OVER_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 346, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT598_154_MMID_FIA_17B_OVER_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_154_MMID_FIA_17B_OVER_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='17B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 349, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 349, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_154_MMID_FIA_17B-OVER_Type', MT598_154_MMID_FIA_17B_OVER_Type)


# Complex type {http://www.w3schools.com}MT598_154_MMID_FIA_17B-ACPO_Type with content type SIMPLE
class MT598_154_MMID_FIA_17B_ACPO_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_154_MMID_FIA_17B-ACPO_Type with content type SIMPLE"""
    _TypeDefinition = MT598_154_MMID_FIA_17B_ACPO_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_154_MMID_FIA_17B-ACPO_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 358, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT598_154_MMID_FIA_17B_ACPO_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_154_MMID_FIA_17B_ACPO_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='17B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 361, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 361, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_154_MMID_FIA_17B-ACPO_Type', MT598_154_MMID_FIA_17B_ACPO_Type)


# Complex type {http://www.w3schools.com}MT598_154_MMID_95R-CSDP_Type with content type SIMPLE
class MT598_154_MMID_95R_CSDP_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_154_MMID_95R-CSDP_Type with content type SIMPLE"""
    _TypeDefinition = MT598_154_MMID_95R_CSDP_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_154_MMID_95R-CSDP_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 370, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT598_154_MMID_95R_CSDP_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_154_MMID_95R_CSDP_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='95R')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 373, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 373, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_154_MMID_95R-CSDP_Type', MT598_154_MMID_95R_CSDP_Type)


# Complex type {http://www.w3schools.com}MT598_154_MMID_FIA_77B_Type with content type SIMPLE
class MT598_154_MMID_FIA_77B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_154_MMID_FIA_77B_Type with content type SIMPLE"""
    _TypeDefinition = MT598_154_MMID_FIA_77B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_154_MMID_FIA_77B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 382, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT598_154_MMID_FIA_77B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_154_MMID_FIA_77B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='77B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 385, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 385, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_154_MMID_FIA_77B_Type', MT598_154_MMID_FIA_77B_Type)


# Complex type {http://www.w3schools.com}MT598_154_MMID_FIA_17B-WITI_Type with content type SIMPLE
class MT598_154_MMID_FIA_17B_WITI_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_154_MMID_FIA_17B-WITI_Type with content type SIMPLE"""
    _TypeDefinition = MT598_154_MMID_FIA_17B_WITI_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_154_MMID_FIA_17B-WITI_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 394, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT598_154_MMID_FIA_17B_WITI_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_154_MMID_FIA_17B_WITI_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='17B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 397, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 397, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_154_MMID_FIA_17B-WITI_Type', MT598_154_MMID_FIA_17B_WITI_Type)


# Complex type {http://www.w3schools.com}MT598_154_MMID_FIA_95R_Type with content type SIMPLE
class MT598_154_MMID_FIA_95R_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_154_MMID_FIA_95R_Type with content type SIMPLE"""
    _TypeDefinition = MT598_154_MMID_FIA_95R_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_154_MMID_FIA_95R_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 406, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT598_154_MMID_FIA_95R_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_154_MMID_FIA_95R_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='95R')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 409, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 409, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_154_MMID_FIA_95R_Type', MT598_154_MMID_FIA_95R_Type)


# Complex type {http://www.w3schools.com}MT598_154_MMID_95R-ISSR_Type with content type SIMPLE
class MT598_154_MMID_95R_ISSR_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_154_MMID_95R-ISSR_Type with content type SIMPLE"""
    _TypeDefinition = MT598_154_MMID_95R_ISSR_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_154_MMID_95R-ISSR_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 418, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT598_154_MMID_95R_ISSR_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_154_MMID_95R_ISSR_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='95R')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 421, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 421, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_154_MMID_95R-ISSR_Type', MT598_154_MMID_95R_ISSR_Type)


# Complex type {http://www.w3schools.com}MT598_154_MMID_FIA_22F-PFRE_Type with content type SIMPLE
class MT598_154_MMID_FIA_22F_PFRE_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_154_MMID_FIA_22F-PFRE_Type with content type SIMPLE"""
    _TypeDefinition = MT598_154_MMID_FIA_22F_PFRE_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_154_MMID_FIA_22F-PFRE_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 430, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT598_154_MMID_FIA_22F_PFRE_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_154_MMID_FIA_22F_PFRE_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='22F')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 433, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 433, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_154_MMID_FIA_22F-PFRE_Type', MT598_154_MMID_FIA_22F_PFRE_Type)


# Complex type {http://www.w3schools.com}MT598_154_MMID_FIA_13B-CCYC_Type with content type SIMPLE
class MT598_154_MMID_FIA_13B_CCYC_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_154_MMID_FIA_13B-CCYC_Type with content type SIMPLE"""
    _TypeDefinition = MT598_154_MMID_FIA_13B_CCYC_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_154_MMID_FIA_13B-CCYC_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 442, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT598_154_MMID_FIA_13B_CCYC_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_154_MMID_FIA_13B_CCYC_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='13B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 445, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 445, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_154_MMID_FIA_13B-CCYC_Type', MT598_154_MMID_FIA_13B_CCYC_Type)


# Complex type {http://www.w3schools.com}MT598_154_MMID_FIA_22F-RTYP_Type with content type SIMPLE
class MT598_154_MMID_FIA_22F_RTYP_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_154_MMID_FIA_22F-RTYP_Type with content type SIMPLE"""
    _TypeDefinition = MT598_154_MMID_FIA_22F_RTYP_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_154_MMID_FIA_22F-RTYP_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 454, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT598_154_MMID_FIA_22F_RTYP_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_154_MMID_FIA_22F_RTYP_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='22F')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 457, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 457, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_154_MMID_FIA_22F-RTYP_Type', MT598_154_MMID_FIA_22F_RTYP_Type)


# Complex type {http://www.w3schools.com}MT598_154_MMID_FIA_22H_Type with content type SIMPLE
class MT598_154_MMID_FIA_22H_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_154_MMID_FIA_22H_Type with content type SIMPLE"""
    _TypeDefinition = MT598_154_MMID_FIA_22H_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_154_MMID_FIA_22H_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 466, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT598_154_MMID_FIA_22H_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_154_MMID_FIA_22H_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='22H')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 469, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 469, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_154_MMID_FIA_22H_Type', MT598_154_MMID_FIA_22H_Type)


# Complex type {http://www.w3schools.com}MT598_154_GENL_22F-CONF_Type with content type SIMPLE
class MT598_154_GENL_22F_CONF_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_154_GENL_22F-CONF_Type with content type SIMPLE"""
    _TypeDefinition = MT598_154_GENL_22F_CONF_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_154_GENL_22F-CONF_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 478, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT598_154_GENL_22F_CONF_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_154_GENL_22F_CONF_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='22F')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 481, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 481, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_154_GENL_22F-CONF_Type', MT598_154_GENL_22F_CONF_Type)


# Complex type {http://www.w3schools.com}MT598_154_MMID_FIA_92D_Type with content type SIMPLE
class MT598_154_MMID_FIA_92D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT598_154_MMID_FIA_92D_Type with content type SIMPLE"""
    _TypeDefinition = MT598_154_MMID_FIA_92D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT598_154_MMID_FIA_92D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 490, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT598_154_MMID_FIA_92D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT598_154_MMID_FIA_92D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='92D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 493, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 493, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag
    })
Namespace.addCategoryObject('typeBinding', 'MT598_154_MMID_FIA_92D_Type', MT598_154_MMID_FIA_92D_Type)


MT598_154 = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'MT598_154'), CTD_ANON, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 567, 1))
Namespace.addCategoryObject('elementBinding', MT598_154.name().localName(), MT598_154)



MT598_154_MMID_FIA_CRDDET._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ResetDate'), MT598_154_MMID_FIA_CRDDET_98A_Type, scope=MT598_154_MMID_FIA_CRDDET, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 502, 3)))

def _BuildAutomaton ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT598_154_MMID_FIA_CRDDET._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ResetDate')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 502, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
MT598_154_MMID_FIA_CRDDET._Automaton = _BuildAutomaton()




MT598_154_GENL._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'RelatedReference'), MT598_154_GENL_20C_Type, scope=MT598_154_GENL, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 508, 3)))

MT598_154_GENL._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'TypeOfConfirmationIndicator'), MT598_154_GENL_22F_CONF_Type, scope=MT598_154_GENL, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 509, 3)))

def _BuildAutomaton_ ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_
    del _BuildAutomaton_
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 508, 3))
    counters.add(cc_0)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT598_154_GENL._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'RelatedReference')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 508, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT598_154_GENL._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'TypeOfConfirmationIndicator')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 509, 3))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
MT598_154_GENL._Automaton = _BuildAutomaton_()




MT598_154_MMID_FIA._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'CouponPaymentFrequency'), MT598_154_MMID_FIA_22F_PFRE_Type, scope=MT598_154_MMID_FIA, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 515, 3)))

MT598_154_MMID_FIA._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'CouponPaymentDay'), MT598_154_MMID_FIA_13B_CPYD_Type, scope=MT598_154_MMID_FIA, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 516, 3)))

MT598_154_MMID_FIA._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'CouponPaymentCycle'), MT598_154_MMID_FIA_13B_CCYC_Type, scope=MT598_154_MMID_FIA, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 517, 3)))

MT598_154_MMID_FIA._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'GenericCategory'), MT598_154_MMID_FIA_12A_Type, scope=MT598_154_MMID_FIA, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 518, 3)))

MT598_154_MMID_FIA._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'MMSecurityType'), MT598_154_MMID_FIA_22H_Type, scope=MT598_154_MMID_FIA, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 519, 3)))

MT598_154_MMID_FIA._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'MaturityDate'), MT598_154_MMID_FIA_98A_MATU_Type, scope=MT598_154_MMID_FIA, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 520, 3)))

MT598_154_MMID_FIA._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'IssueDate'), MT598_154_MMID_FIA_98A_ISSU_Type, scope=MT598_154_MMID_FIA, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 521, 3)))

MT598_154_MMID_FIA._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'InterestRate'), MT598_154_MMID_FIA_92A_INTR_Type, scope=MT598_154_MMID_FIA, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 522, 3)))

MT598_154_MMID_FIA._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'CouponRateTypeIndicator'), MT598_154_MMID_FIA_22F_RTYP_Type, scope=MT598_154_MMID_FIA, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 523, 3)))

MT598_154_MMID_FIA._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'MiniumNominalValue'), MT598_154_MMID_FIA_36B_MINO_Type, scope=MT598_154_MMID_FIA, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 524, 3)))

MT598_154_MMID_FIA._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'AuthorisedAmount'), MT598_154_MMID_FIA_36B_AUTH_Type, scope=MT598_154_MMID_FIA, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 525, 3)))

MT598_154_MMID_FIA._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'AcceptorOfMMSecurity'), MT598_154_MMID_FIA_95R_Type, scope=MT598_154_MMID_FIA, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 526, 3)))

MT598_154_MMID_FIA._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'MinimumIssuerDenomination'), MT598_154_MMID_FIA_36B_MINI_Type, scope=MT598_154_MMID_FIA, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 527, 3)))

MT598_154_MMID_FIA._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'FloorCapRate'), MT598_154_MMID_FIA_92D_Type, scope=MT598_154_MMID_FIA, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 528, 3)))

MT598_154_MMID_FIA._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'CouponPaymentDayIndicator'), MT598_154_MMID_FIA_22F_CPDI_Type, scope=MT598_154_MMID_FIA, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 529, 3)))

MT598_154_MMID_FIA._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'WITI'), MT598_154_MMID_FIA_17B_WITI_Type, scope=MT598_154_MMID_FIA, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 530, 3)))

MT598_154_MMID_FIA._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'WithholdingTaxOnInterestRate'), MT598_154_MMID_FIA_92A_TAXR_Type, scope=MT598_154_MMID_FIA, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 531, 3)))

MT598_154_MMID_FIA._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'FinalCouponPaymentOnMaturity'), MT598_154_MMID_FIA_17B_FCPM_Type, scope=MT598_154_MMID_FIA, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 532, 3)))

MT598_154_MMID_FIA._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'CouponPaymentIndicator'), MT598_154_MMID_FIA_17B_CPMI_Type, scope=MT598_154_MMID_FIA, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 533, 3)))

MT598_154_MMID_FIA._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'AutomatedCouponPaymentCalculation'), MT598_154_MMID_FIA_17B_ACPC_Type, scope=MT598_154_MMID_FIA, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 534, 3)))

MT598_154_MMID_FIA._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'AutomatedCouponPaymentOnly'), MT598_154_MMID_FIA_17B_ACPO_Type, scope=MT598_154_MMID_FIA, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 535, 3)))

MT598_154_MMID_FIA._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'CouponRateCalculationDescription'), MT598_154_MMID_FIA_77B_Type, scope=MT598_154_MMID_FIA, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 536, 3)))

MT598_154_MMID_FIA._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'OverrideIndicator'), MT598_154_MMID_FIA_17B_OVER_Type, scope=MT598_154_MMID_FIA, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 537, 3)))

MT598_154_MMID_FIA._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'CouponPaymentCalculationMethod'), MT598_154_MMID_FIA_13B_CPCM_Type, scope=MT598_154_MMID_FIA, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 538, 3)))

MT598_154_MMID_FIA._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'CouponRateSource'), MT598_154_MMID_FIA_14F_Type, scope=MT598_154_MMID_FIA, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 539, 3)))

MT598_154_MMID_FIA._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'CouponRateVarianceFromSource'), MT598_154_MMID_FIA_25_Type, scope=MT598_154_MMID_FIA, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 540, 3)))

MT598_154_MMID_FIA._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'CouponCompoundFrequency'), MT598_154_MMID_FIA_22F_CCFR_Type, scope=MT598_154_MMID_FIA, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 541, 3)))

MT598_154_MMID_FIA._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'CouponResetFrequency'), MT598_154_MMID_FIA_22F_RESF_Type, scope=MT598_154_MMID_FIA, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 542, 3)))

MT598_154_MMID_FIA._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'CouponResetStartDate'), MT598_154_MMID_FIA_98A_CRSD_Type, scope=MT598_154_MMID_FIA, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 543, 3)))

MT598_154_MMID_FIA._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'CRDDET'), MT598_154_MMID_FIA_CRDDET, scope=MT598_154_MMID_FIA, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 544, 3)))

MT598_154_MMID_FIA._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'CPDDET'), MT598_154_MMID_FIA_CPDDET, scope=MT598_154_MMID_FIA, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 545, 3)))

def _BuildAutomaton_2 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_2
    del _BuildAutomaton_2
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 515, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 516, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 517, 3))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 522, 3))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 523, 3))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 525, 3))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 526, 3))
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 527, 3))
    counters.add(cc_7)
    cc_8 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 528, 3))
    counters.add(cc_8)
    cc_9 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 529, 3))
    counters.add(cc_9)
    cc_10 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 530, 3))
    counters.add(cc_10)
    cc_11 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 531, 3))
    counters.add(cc_11)
    cc_12 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 532, 3))
    counters.add(cc_12)
    cc_13 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 533, 3))
    counters.add(cc_13)
    cc_14 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 534, 3))
    counters.add(cc_14)
    cc_15 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 535, 3))
    counters.add(cc_15)
    cc_16 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 536, 3))
    counters.add(cc_16)
    cc_17 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 537, 3))
    counters.add(cc_17)
    cc_18 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 538, 3))
    counters.add(cc_18)
    cc_19 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 539, 3))
    counters.add(cc_19)
    cc_20 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 540, 3))
    counters.add(cc_20)
    cc_21 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 541, 3))
    counters.add(cc_21)
    cc_22 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 542, 3))
    counters.add(cc_22)
    cc_23 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 543, 3))
    counters.add(cc_23)
    cc_24 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 544, 3))
    counters.add(cc_24)
    cc_25 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 545, 3))
    counters.add(cc_25)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT598_154_MMID_FIA._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'CouponPaymentFrequency')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 515, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT598_154_MMID_FIA._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'CouponPaymentDay')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 516, 3))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT598_154_MMID_FIA._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'CouponPaymentCycle')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 517, 3))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT598_154_MMID_FIA._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'GenericCategory')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 518, 3))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT598_154_MMID_FIA._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'MMSecurityType')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 519, 3))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT598_154_MMID_FIA._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'MaturityDate')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 520, 3))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT598_154_MMID_FIA._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'IssueDate')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 521, 3))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT598_154_MMID_FIA._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'InterestRate')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 522, 3))
    st_7 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT598_154_MMID_FIA._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'CouponRateTypeIndicator')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 523, 3))
    st_8 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT598_154_MMID_FIA._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'MiniumNominalValue')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 524, 3))
    st_9 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_5, False))
    symbol = pyxb.binding.content.ElementUse(MT598_154_MMID_FIA._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'AuthorisedAmount')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 525, 3))
    st_10 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_10)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_6, False))
    symbol = pyxb.binding.content.ElementUse(MT598_154_MMID_FIA._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'AcceptorOfMMSecurity')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 526, 3))
    st_11 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_11)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_7, False))
    symbol = pyxb.binding.content.ElementUse(MT598_154_MMID_FIA._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'MinimumIssuerDenomination')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 527, 3))
    st_12 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_12)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_8, False))
    symbol = pyxb.binding.content.ElementUse(MT598_154_MMID_FIA._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'FloorCapRate')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 528, 3))
    st_13 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_13)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_9, False))
    symbol = pyxb.binding.content.ElementUse(MT598_154_MMID_FIA._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'CouponPaymentDayIndicator')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 529, 3))
    st_14 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_14)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_10, False))
    symbol = pyxb.binding.content.ElementUse(MT598_154_MMID_FIA._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'WITI')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 530, 3))
    st_15 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_15)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_11, False))
    symbol = pyxb.binding.content.ElementUse(MT598_154_MMID_FIA._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'WithholdingTaxOnInterestRate')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 531, 3))
    st_16 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_16)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_12, False))
    symbol = pyxb.binding.content.ElementUse(MT598_154_MMID_FIA._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'FinalCouponPaymentOnMaturity')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 532, 3))
    st_17 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_17)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_13, False))
    symbol = pyxb.binding.content.ElementUse(MT598_154_MMID_FIA._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'CouponPaymentIndicator')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 533, 3))
    st_18 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_18)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_14, False))
    symbol = pyxb.binding.content.ElementUse(MT598_154_MMID_FIA._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'AutomatedCouponPaymentCalculation')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 534, 3))
    st_19 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_19)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_15, False))
    symbol = pyxb.binding.content.ElementUse(MT598_154_MMID_FIA._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'AutomatedCouponPaymentOnly')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 535, 3))
    st_20 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_20)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_16, False))
    symbol = pyxb.binding.content.ElementUse(MT598_154_MMID_FIA._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'CouponRateCalculationDescription')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 536, 3))
    st_21 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_21)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_17, False))
    symbol = pyxb.binding.content.ElementUse(MT598_154_MMID_FIA._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'OverrideIndicator')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 537, 3))
    st_22 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_22)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_18, False))
    symbol = pyxb.binding.content.ElementUse(MT598_154_MMID_FIA._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'CouponPaymentCalculationMethod')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 538, 3))
    st_23 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_23)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_19, False))
    symbol = pyxb.binding.content.ElementUse(MT598_154_MMID_FIA._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'CouponRateSource')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 539, 3))
    st_24 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_24)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_20, False))
    symbol = pyxb.binding.content.ElementUse(MT598_154_MMID_FIA._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'CouponRateVarianceFromSource')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 540, 3))
    st_25 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_25)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_21, False))
    symbol = pyxb.binding.content.ElementUse(MT598_154_MMID_FIA._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'CouponCompoundFrequency')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 541, 3))
    st_26 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_26)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_22, False))
    symbol = pyxb.binding.content.ElementUse(MT598_154_MMID_FIA._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'CouponResetFrequency')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 542, 3))
    st_27 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_27)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_23, False))
    symbol = pyxb.binding.content.ElementUse(MT598_154_MMID_FIA._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'CouponResetStartDate')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 543, 3))
    st_28 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_28)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_24, False))
    symbol = pyxb.binding.content.ElementUse(MT598_154_MMID_FIA._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'CRDDET')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 544, 3))
    st_29 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_29)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_25, False))
    symbol = pyxb.binding.content.ElementUse(MT598_154_MMID_FIA._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'CPDDET')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 545, 3))
    st_30 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_30)
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
    transitions.append(fac.Transition(st_4, [
         ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
         ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
         ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
         ]))
    transitions.append(fac.Transition(st_8, [
         ]))
    transitions.append(fac.Transition(st_9, [
         ]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_3, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_3, False) ]))
    st_7._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_4, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_4, False) ]))
    st_8._set_transitionSet(transitions)
    transitions = []
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
    transitions.append(fac.Transition(st_27, [
         ]))
    transitions.append(fac.Transition(st_28, [
         ]))
    transitions.append(fac.Transition(st_29, [
         ]))
    transitions.append(fac.Transition(st_30, [
         ]))
    st_9._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_5, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_22, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_23, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_24, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_25, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_26, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_27, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_28, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_29, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_30, [
        fac.UpdateInstruction(cc_5, False) ]))
    st_10._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_6, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_22, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_23, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_24, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_25, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_26, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_27, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_28, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_29, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_30, [
        fac.UpdateInstruction(cc_6, False) ]))
    st_11._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_7, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_22, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_23, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_24, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_25, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_26, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_27, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_28, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_29, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_30, [
        fac.UpdateInstruction(cc_7, False) ]))
    st_12._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_8, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_22, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_23, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_24, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_25, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_26, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_27, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_28, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_29, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_30, [
        fac.UpdateInstruction(cc_8, False) ]))
    st_13._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_9, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_22, [
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_23, [
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_24, [
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_25, [
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_26, [
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_27, [
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_28, [
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_29, [
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_30, [
        fac.UpdateInstruction(cc_9, False) ]))
    st_14._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_10, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_22, [
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_23, [
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_24, [
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_25, [
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_26, [
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_27, [
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_28, [
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_29, [
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_30, [
        fac.UpdateInstruction(cc_10, False) ]))
    st_15._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_11, True) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_22, [
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_23, [
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_24, [
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_25, [
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_26, [
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_27, [
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_28, [
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_29, [
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_30, [
        fac.UpdateInstruction(cc_11, False) ]))
    st_16._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_12, True) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_12, False) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_12, False) ]))
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
    transitions.append(fac.Transition(st_27, [
        fac.UpdateInstruction(cc_12, False) ]))
    transitions.append(fac.Transition(st_28, [
        fac.UpdateInstruction(cc_12, False) ]))
    transitions.append(fac.Transition(st_29, [
        fac.UpdateInstruction(cc_12, False) ]))
    transitions.append(fac.Transition(st_30, [
        fac.UpdateInstruction(cc_12, False) ]))
    st_17._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_13, True) ]))
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
    transitions.append(fac.Transition(st_30, [
        fac.UpdateInstruction(cc_13, False) ]))
    st_18._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_14, True) ]))
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
    transitions.append(fac.Transition(st_30, [
        fac.UpdateInstruction(cc_14, False) ]))
    st_19._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_15, True) ]))
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
    transitions.append(fac.Transition(st_30, [
        fac.UpdateInstruction(cc_15, False) ]))
    st_20._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_16, True) ]))
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
    transitions.append(fac.Transition(st_30, [
        fac.UpdateInstruction(cc_16, False) ]))
    st_21._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_22, [
        fac.UpdateInstruction(cc_17, True) ]))
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
    transitions.append(fac.Transition(st_30, [
        fac.UpdateInstruction(cc_17, False) ]))
    st_22._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_23, [
        fac.UpdateInstruction(cc_18, True) ]))
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
    transitions.append(fac.Transition(st_30, [
        fac.UpdateInstruction(cc_18, False) ]))
    st_23._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_24, [
        fac.UpdateInstruction(cc_19, True) ]))
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
    transitions.append(fac.Transition(st_30, [
        fac.UpdateInstruction(cc_19, False) ]))
    st_24._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_25, [
        fac.UpdateInstruction(cc_20, True) ]))
    transitions.append(fac.Transition(st_26, [
        fac.UpdateInstruction(cc_20, False) ]))
    transitions.append(fac.Transition(st_27, [
        fac.UpdateInstruction(cc_20, False) ]))
    transitions.append(fac.Transition(st_28, [
        fac.UpdateInstruction(cc_20, False) ]))
    transitions.append(fac.Transition(st_29, [
        fac.UpdateInstruction(cc_20, False) ]))
    transitions.append(fac.Transition(st_30, [
        fac.UpdateInstruction(cc_20, False) ]))
    st_25._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_26, [
        fac.UpdateInstruction(cc_21, True) ]))
    transitions.append(fac.Transition(st_27, [
        fac.UpdateInstruction(cc_21, False) ]))
    transitions.append(fac.Transition(st_28, [
        fac.UpdateInstruction(cc_21, False) ]))
    transitions.append(fac.Transition(st_29, [
        fac.UpdateInstruction(cc_21, False) ]))
    transitions.append(fac.Transition(st_30, [
        fac.UpdateInstruction(cc_21, False) ]))
    st_26._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_27, [
        fac.UpdateInstruction(cc_22, True) ]))
    transitions.append(fac.Transition(st_28, [
        fac.UpdateInstruction(cc_22, False) ]))
    transitions.append(fac.Transition(st_29, [
        fac.UpdateInstruction(cc_22, False) ]))
    transitions.append(fac.Transition(st_30, [
        fac.UpdateInstruction(cc_22, False) ]))
    st_27._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_28, [
        fac.UpdateInstruction(cc_23, True) ]))
    transitions.append(fac.Transition(st_29, [
        fac.UpdateInstruction(cc_23, False) ]))
    transitions.append(fac.Transition(st_30, [
        fac.UpdateInstruction(cc_23, False) ]))
    st_28._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_29, [
        fac.UpdateInstruction(cc_24, True) ]))
    transitions.append(fac.Transition(st_30, [
        fac.UpdateInstruction(cc_24, False) ]))
    st_29._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_30, [
        fac.UpdateInstruction(cc_25, True) ]))
    st_30._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
MT598_154_MMID_FIA._Automaton = _BuildAutomaton_2()




MT598_154_MMID._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'IssuersCSDParticipantCode'), MT598_154_MMID_95R_CSDP_Type, scope=MT598_154_MMID, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 551, 3)))

MT598_154_MMID._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'IssuersParticipantCode'), MT598_154_MMID_95R_ISSR_Type, scope=MT598_154_MMID, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 552, 3)))

MT598_154_MMID._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'IssuingAgentsParticipantCode'), MT598_154_MMID_95R_ISSA_Type, scope=MT598_154_MMID, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 553, 3)))

MT598_154_MMID._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'IdenitficationOfSecurities'), MT598_154_MMID_35B_Type, scope=MT598_154_MMID, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 554, 3)))

MT598_154_MMID._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'NominalValueIssued'), MT598_154_MMID_36B_QISS_Type, scope=MT598_154_MMID, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 555, 3)))

MT598_154_MMID._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'IssuersSORAccountAtCSD'), MT598_154_MMID_97B_Type, scope=MT598_154_MMID, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 556, 3)))

MT598_154_MMID._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'FIA'), MT598_154_MMID_FIA, scope=MT598_154_MMID, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 557, 3)))

def _BuildAutomaton_3 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_3
    del _BuildAutomaton_3
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0L, max=1, metadata=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 557, 3))
    counters.add(cc_0)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT598_154_MMID._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'IssuersCSDParticipantCode')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 551, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT598_154_MMID._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'IssuersParticipantCode')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 552, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT598_154_MMID._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'IssuingAgentsParticipantCode')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 553, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT598_154_MMID._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'IdenitficationOfSecurities')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 554, 3))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT598_154_MMID._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'NominalValueIssued')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 555, 3))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT598_154_MMID._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'IssuersSORAccountAtCSD')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 556, 3))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(MT598_154_MMID._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'FIA')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 557, 3))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
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
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
         ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_6._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
MT598_154_MMID._Automaton = _BuildAutomaton_3()




MT598_154_MMID_FIA_CPDDET._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PaymentDate'), MT598_154_MMID_FIA_CPDDET_98A_Type, scope=MT598_154_MMID_FIA_CPDDET, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 563, 3)))

def _BuildAutomaton_4 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_4
    del _BuildAutomaton_4
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT598_154_MMID_FIA_CPDDET._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PaymentDate')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 563, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
MT598_154_MMID_FIA_CPDDET._Automaton = _BuildAutomaton_4()




CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'TransactionReference'), MT598_154_20_Type, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 570, 4)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SubMessageType'), MT598_154_12_Type, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 571, 4)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ProprietaryMessage'), MT598_154_77E_Type, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 572, 4)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'GENL'), MT598_154_GENL, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 573, 4)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'MMID'), MT598_154_MMID, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 574, 4)))

def _BuildAutomaton_5 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_5
    del _BuildAutomaton_5
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'TransactionReference')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 570, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SubMessageType')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 571, 4))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ProprietaryMessage')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 572, 4))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'GENL')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 573, 4))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'MMID')), pyxb.utils.utility.Location('C:\\SWIFT\\SwiftReader\\XSD\\MT598_154.xsd', 574, 4))
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
CTD_ANON._Automaton = _BuildAutomaton_5()

