# C:\Projects\Code\SwiftMessagingSolution_Python3\base\extensions\SwiftIntegration\Utilities\XSD\MT300.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:96afad3d20bbfe8d040a1a097fa388d9fecd10e3
# Generated 2019-11-06 16:26:52.989184 by PyXB version 1.2.6 using Python 3.7.4.final.0
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
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:23ecc800-0084-11ea-98ee-509a4c321f2f')

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


# Atomic simple type: {http://www.w3schools.com}MT300_SequenceA_GeneralInformation_20_Type_Pattern
class MT300_SequenceA_GeneralInformation_20_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceA_GeneralInformation_20_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 3, 1)
    _Documentation = None
MT300_SequenceA_GeneralInformation_20_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceA_GeneralInformation_20_Type_Pattern._CF_pattern.addPattern(pattern="(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,16})")
MT300_SequenceA_GeneralInformation_20_Type_Pattern._InitializeFacetMap(MT300_SequenceA_GeneralInformation_20_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceA_GeneralInformation_20_Type_Pattern', MT300_SequenceA_GeneralInformation_20_Type_Pattern)
_module_typeBindings.MT300_SequenceA_GeneralInformation_20_Type_Pattern = MT300_SequenceA_GeneralInformation_20_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceA_GeneralInformation_21_Type_Pattern
class MT300_SequenceA_GeneralInformation_21_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceA_GeneralInformation_21_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 16, 1)
    _Documentation = None
MT300_SequenceA_GeneralInformation_21_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceA_GeneralInformation_21_Type_Pattern._CF_pattern.addPattern(pattern="(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,16})")
MT300_SequenceA_GeneralInformation_21_Type_Pattern._InitializeFacetMap(MT300_SequenceA_GeneralInformation_21_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceA_GeneralInformation_21_Type_Pattern', MT300_SequenceA_GeneralInformation_21_Type_Pattern)
_module_typeBindings.MT300_SequenceA_GeneralInformation_21_Type_Pattern = MT300_SequenceA_GeneralInformation_21_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceA_GeneralInformation_22A_Type_Pattern
class MT300_SequenceA_GeneralInformation_22A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceA_GeneralInformation_22A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 29, 1)
    _Documentation = None
MT300_SequenceA_GeneralInformation_22A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceA_GeneralInformation_22A_Type_Pattern._CF_pattern.addPattern(pattern='((AMND|CANC|DUPL|EXOP|NEWT))')
MT300_SequenceA_GeneralInformation_22A_Type_Pattern._InitializeFacetMap(MT300_SequenceA_GeneralInformation_22A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceA_GeneralInformation_22A_Type_Pattern', MT300_SequenceA_GeneralInformation_22A_Type_Pattern)
_module_typeBindings.MT300_SequenceA_GeneralInformation_22A_Type_Pattern = MT300_SequenceA_GeneralInformation_22A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceA_GeneralInformation_94A_Type_Pattern
class MT300_SequenceA_GeneralInformation_94A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceA_GeneralInformation_94A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 42, 1)
    _Documentation = None
MT300_SequenceA_GeneralInformation_94A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceA_GeneralInformation_94A_Type_Pattern._CF_pattern.addPattern(pattern='((AGNT|BILA|BROK))')
MT300_SequenceA_GeneralInformation_94A_Type_Pattern._InitializeFacetMap(MT300_SequenceA_GeneralInformation_94A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceA_GeneralInformation_94A_Type_Pattern', MT300_SequenceA_GeneralInformation_94A_Type_Pattern)
_module_typeBindings.MT300_SequenceA_GeneralInformation_94A_Type_Pattern = MT300_SequenceA_GeneralInformation_94A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceA_GeneralInformation_22C_Type_Pattern
class MT300_SequenceA_GeneralInformation_22C_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceA_GeneralInformation_22C_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 55, 1)
    _Documentation = None
MT300_SequenceA_GeneralInformation_22C_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceA_GeneralInformation_22C_Type_Pattern._CF_pattern.addPattern(pattern='([A-Z]{4}[A-Z0-9]{2}[0-9]{4}[A-Z]{4}[A-Z0-9]{2})')
MT300_SequenceA_GeneralInformation_22C_Type_Pattern._InitializeFacetMap(MT300_SequenceA_GeneralInformation_22C_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceA_GeneralInformation_22C_Type_Pattern', MT300_SequenceA_GeneralInformation_22C_Type_Pattern)
_module_typeBindings.MT300_SequenceA_GeneralInformation_22C_Type_Pattern = MT300_SequenceA_GeneralInformation_22C_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceA_GeneralInformation_17T_Type_Pattern
class MT300_SequenceA_GeneralInformation_17T_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceA_GeneralInformation_17T_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 68, 1)
    _Documentation = None
MT300_SequenceA_GeneralInformation_17T_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceA_GeneralInformation_17T_Type_Pattern._CF_pattern.addPattern(pattern='((N|Y))')
MT300_SequenceA_GeneralInformation_17T_Type_Pattern._InitializeFacetMap(MT300_SequenceA_GeneralInformation_17T_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceA_GeneralInformation_17T_Type_Pattern', MT300_SequenceA_GeneralInformation_17T_Type_Pattern)
_module_typeBindings.MT300_SequenceA_GeneralInformation_17T_Type_Pattern = MT300_SequenceA_GeneralInformation_17T_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceA_GeneralInformation_17U_Type_Pattern
class MT300_SequenceA_GeneralInformation_17U_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceA_GeneralInformation_17U_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 81, 1)
    _Documentation = None
MT300_SequenceA_GeneralInformation_17U_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceA_GeneralInformation_17U_Type_Pattern._CF_pattern.addPattern(pattern='((N|Y))')
MT300_SequenceA_GeneralInformation_17U_Type_Pattern._InitializeFacetMap(MT300_SequenceA_GeneralInformation_17U_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceA_GeneralInformation_17U_Type_Pattern', MT300_SequenceA_GeneralInformation_17U_Type_Pattern)
_module_typeBindings.MT300_SequenceA_GeneralInformation_17U_Type_Pattern = MT300_SequenceA_GeneralInformation_17U_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceA_GeneralInformation_17I_Type_Pattern
class MT300_SequenceA_GeneralInformation_17I_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceA_GeneralInformation_17I_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 94, 1)
    _Documentation = None
MT300_SequenceA_GeneralInformation_17I_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceA_GeneralInformation_17I_Type_Pattern._CF_pattern.addPattern(pattern='((N|Y))')
MT300_SequenceA_GeneralInformation_17I_Type_Pattern._InitializeFacetMap(MT300_SequenceA_GeneralInformation_17I_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceA_GeneralInformation_17I_Type_Pattern', MT300_SequenceA_GeneralInformation_17I_Type_Pattern)
_module_typeBindings.MT300_SequenceA_GeneralInformation_17I_Type_Pattern = MT300_SequenceA_GeneralInformation_17I_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceA_GeneralInformation_82A_Type_Pattern
class MT300_SequenceA_GeneralInformation_82A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceA_GeneralInformation_82A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 107, 1)
    _Documentation = None
MT300_SequenceA_GeneralInformation_82A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceA_GeneralInformation_82A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT300_SequenceA_GeneralInformation_82A_Type_Pattern._InitializeFacetMap(MT300_SequenceA_GeneralInformation_82A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceA_GeneralInformation_82A_Type_Pattern', MT300_SequenceA_GeneralInformation_82A_Type_Pattern)
_module_typeBindings.MT300_SequenceA_GeneralInformation_82A_Type_Pattern = MT300_SequenceA_GeneralInformation_82A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceA_GeneralInformation_82J_Type_Pattern
class MT300_SequenceA_GeneralInformation_82J_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceA_GeneralInformation_82J_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 120, 1)
    _Documentation = None
MT300_SequenceA_GeneralInformation_82J_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceA_GeneralInformation_82J_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,40}\\n?){1,5})")
MT300_SequenceA_GeneralInformation_82J_Type_Pattern._InitializeFacetMap(MT300_SequenceA_GeneralInformation_82J_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceA_GeneralInformation_82J_Type_Pattern', MT300_SequenceA_GeneralInformation_82J_Type_Pattern)
_module_typeBindings.MT300_SequenceA_GeneralInformation_82J_Type_Pattern = MT300_SequenceA_GeneralInformation_82J_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceA_GeneralInformation_87A_Type_Pattern
class MT300_SequenceA_GeneralInformation_87A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceA_GeneralInformation_87A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 133, 1)
    _Documentation = None
MT300_SequenceA_GeneralInformation_87A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceA_GeneralInformation_87A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT300_SequenceA_GeneralInformation_87A_Type_Pattern._InitializeFacetMap(MT300_SequenceA_GeneralInformation_87A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceA_GeneralInformation_87A_Type_Pattern', MT300_SequenceA_GeneralInformation_87A_Type_Pattern)
_module_typeBindings.MT300_SequenceA_GeneralInformation_87A_Type_Pattern = MT300_SequenceA_GeneralInformation_87A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceA_GeneralInformation_87J_Type_Pattern
class MT300_SequenceA_GeneralInformation_87J_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceA_GeneralInformation_87J_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 146, 1)
    _Documentation = None
MT300_SequenceA_GeneralInformation_87J_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceA_GeneralInformation_87J_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,40}\\n?){1,5})")
MT300_SequenceA_GeneralInformation_87J_Type_Pattern._InitializeFacetMap(MT300_SequenceA_GeneralInformation_87J_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceA_GeneralInformation_87J_Type_Pattern', MT300_SequenceA_GeneralInformation_87J_Type_Pattern)
_module_typeBindings.MT300_SequenceA_GeneralInformation_87J_Type_Pattern = MT300_SequenceA_GeneralInformation_87J_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceA_GeneralInformation_83A_Type_Pattern
class MT300_SequenceA_GeneralInformation_83A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceA_GeneralInformation_83A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 159, 1)
    _Documentation = None
MT300_SequenceA_GeneralInformation_83A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceA_GeneralInformation_83A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT300_SequenceA_GeneralInformation_83A_Type_Pattern._InitializeFacetMap(MT300_SequenceA_GeneralInformation_83A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceA_GeneralInformation_83A_Type_Pattern', MT300_SequenceA_GeneralInformation_83A_Type_Pattern)
_module_typeBindings.MT300_SequenceA_GeneralInformation_83A_Type_Pattern = MT300_SequenceA_GeneralInformation_83A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceA_GeneralInformation_83J_Type_Pattern
class MT300_SequenceA_GeneralInformation_83J_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceA_GeneralInformation_83J_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 172, 1)
    _Documentation = None
MT300_SequenceA_GeneralInformation_83J_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceA_GeneralInformation_83J_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,40}\\n?){1,5})")
MT300_SequenceA_GeneralInformation_83J_Type_Pattern._InitializeFacetMap(MT300_SequenceA_GeneralInformation_83J_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceA_GeneralInformation_83J_Type_Pattern', MT300_SequenceA_GeneralInformation_83J_Type_Pattern)
_module_typeBindings.MT300_SequenceA_GeneralInformation_83J_Type_Pattern = MT300_SequenceA_GeneralInformation_83J_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceA_GeneralInformation_77H_Type_Pattern
class MT300_SequenceA_GeneralInformation_77H_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceA_GeneralInformation_77H_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 185, 1)
    _Documentation = None
MT300_SequenceA_GeneralInformation_77H_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceA_GeneralInformation_77H_Type_Pattern._CF_pattern.addPattern(pattern='((AFB|DERV|FBF|FEOMA|ICOM|IFEMA|ISDA|ISDACN|OTHER)(/[0-9]{8})?(//[0-9]{4})?)')
MT300_SequenceA_GeneralInformation_77H_Type_Pattern._InitializeFacetMap(MT300_SequenceA_GeneralInformation_77H_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceA_GeneralInformation_77H_Type_Pattern', MT300_SequenceA_GeneralInformation_77H_Type_Pattern)
_module_typeBindings.MT300_SequenceA_GeneralInformation_77H_Type_Pattern = MT300_SequenceA_GeneralInformation_77H_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceA_GeneralInformation_77D_Type_Pattern
class MT300_SequenceA_GeneralInformation_77D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceA_GeneralInformation_77D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 198, 1)
    _Documentation = None
MT300_SequenceA_GeneralInformation_77D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceA_GeneralInformation_77D_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,6})")
MT300_SequenceA_GeneralInformation_77D_Type_Pattern._InitializeFacetMap(MT300_SequenceA_GeneralInformation_77D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceA_GeneralInformation_77D_Type_Pattern', MT300_SequenceA_GeneralInformation_77D_Type_Pattern)
_module_typeBindings.MT300_SequenceA_GeneralInformation_77D_Type_Pattern = MT300_SequenceA_GeneralInformation_77D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceA_GeneralInformation_14C_Type_Pattern
class MT300_SequenceA_GeneralInformation_14C_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceA_GeneralInformation_14C_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 211, 1)
    _Documentation = None
MT300_SequenceA_GeneralInformation_14C_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceA_GeneralInformation_14C_Type_Pattern._CF_pattern.addPattern(pattern='([0-9]{4})')
MT300_SequenceA_GeneralInformation_14C_Type_Pattern._InitializeFacetMap(MT300_SequenceA_GeneralInformation_14C_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceA_GeneralInformation_14C_Type_Pattern', MT300_SequenceA_GeneralInformation_14C_Type_Pattern)
_module_typeBindings.MT300_SequenceA_GeneralInformation_14C_Type_Pattern = MT300_SequenceA_GeneralInformation_14C_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceA_GeneralInformation_17F_Type_Pattern
class MT300_SequenceA_GeneralInformation_17F_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceA_GeneralInformation_17F_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 224, 1)
    _Documentation = None
MT300_SequenceA_GeneralInformation_17F_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceA_GeneralInformation_17F_Type_Pattern._CF_pattern.addPattern(pattern='((N|Y))')
MT300_SequenceA_GeneralInformation_17F_Type_Pattern._InitializeFacetMap(MT300_SequenceA_GeneralInformation_17F_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceA_GeneralInformation_17F_Type_Pattern', MT300_SequenceA_GeneralInformation_17F_Type_Pattern)
_module_typeBindings.MT300_SequenceA_GeneralInformation_17F_Type_Pattern = MT300_SequenceA_GeneralInformation_17F_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceA_GeneralInformation_17O_Type_Pattern
class MT300_SequenceA_GeneralInformation_17O_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceA_GeneralInformation_17O_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 237, 1)
    _Documentation = None
MT300_SequenceA_GeneralInformation_17O_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceA_GeneralInformation_17O_Type_Pattern._CF_pattern.addPattern(pattern='((N|Y))')
MT300_SequenceA_GeneralInformation_17O_Type_Pattern._InitializeFacetMap(MT300_SequenceA_GeneralInformation_17O_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceA_GeneralInformation_17O_Type_Pattern', MT300_SequenceA_GeneralInformation_17O_Type_Pattern)
_module_typeBindings.MT300_SequenceA_GeneralInformation_17O_Type_Pattern = MT300_SequenceA_GeneralInformation_17O_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceA_GeneralInformation_32E_Type_Pattern
class MT300_SequenceA_GeneralInformation_32E_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceA_GeneralInformation_32E_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 250, 1)
    _Documentation = None
MT300_SequenceA_GeneralInformation_32E_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceA_GeneralInformation_32E_Type_Pattern._CF_pattern.addPattern(pattern='([A-Z]{3})')
MT300_SequenceA_GeneralInformation_32E_Type_Pattern._InitializeFacetMap(MT300_SequenceA_GeneralInformation_32E_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceA_GeneralInformation_32E_Type_Pattern', MT300_SequenceA_GeneralInformation_32E_Type_Pattern)
_module_typeBindings.MT300_SequenceA_GeneralInformation_32E_Type_Pattern = MT300_SequenceA_GeneralInformation_32E_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceA_GeneralInformation_30U_Type_Pattern
class MT300_SequenceA_GeneralInformation_30U_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceA_GeneralInformation_30U_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 263, 1)
    _Documentation = None
MT300_SequenceA_GeneralInformation_30U_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceA_GeneralInformation_30U_Type_Pattern._CF_pattern.addPattern(pattern='([0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01]))')
MT300_SequenceA_GeneralInformation_30U_Type_Pattern._InitializeFacetMap(MT300_SequenceA_GeneralInformation_30U_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceA_GeneralInformation_30U_Type_Pattern', MT300_SequenceA_GeneralInformation_30U_Type_Pattern)
_module_typeBindings.MT300_SequenceA_GeneralInformation_30U_Type_Pattern = MT300_SequenceA_GeneralInformation_30U_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceA_GeneralInformation_14S_Type_Pattern
class MT300_SequenceA_GeneralInformation_14S_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceA_GeneralInformation_14S_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 276, 1)
    _Documentation = None
MT300_SequenceA_GeneralInformation_14S_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceA_GeneralInformation_14S_Type_Pattern._CF_pattern.addPattern(pattern='([A-Z]{3}[0-9]{1,2}(/[0-9]{4}/[A-Z0-9]{4})?)')
MT300_SequenceA_GeneralInformation_14S_Type_Pattern._InitializeFacetMap(MT300_SequenceA_GeneralInformation_14S_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceA_GeneralInformation_14S_Type_Pattern', MT300_SequenceA_GeneralInformation_14S_Type_Pattern)
_module_typeBindings.MT300_SequenceA_GeneralInformation_14S_Type_Pattern = MT300_SequenceA_GeneralInformation_14S_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceA_GeneralInformation_21A_Type_Pattern
class MT300_SequenceA_GeneralInformation_21A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceA_GeneralInformation_21A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 289, 1)
    _Documentation = None
MT300_SequenceA_GeneralInformation_21A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceA_GeneralInformation_21A_Type_Pattern._CF_pattern.addPattern(pattern="(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,16})")
MT300_SequenceA_GeneralInformation_21A_Type_Pattern._InitializeFacetMap(MT300_SequenceA_GeneralInformation_21A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceA_GeneralInformation_21A_Type_Pattern', MT300_SequenceA_GeneralInformation_21A_Type_Pattern)
_module_typeBindings.MT300_SequenceA_GeneralInformation_21A_Type_Pattern = MT300_SequenceA_GeneralInformation_21A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceA_GeneralInformation_14E_Type_Pattern
class MT300_SequenceA_GeneralInformation_14E_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceA_GeneralInformation_14E_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 302, 1)
    _Documentation = None
MT300_SequenceA_GeneralInformation_14E_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceA_GeneralInformation_14E_Type_Pattern._CF_pattern.addPattern(pattern="(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35})")
MT300_SequenceA_GeneralInformation_14E_Type_Pattern._InitializeFacetMap(MT300_SequenceA_GeneralInformation_14E_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceA_GeneralInformation_14E_Type_Pattern', MT300_SequenceA_GeneralInformation_14E_Type_Pattern)
_module_typeBindings.MT300_SequenceA_GeneralInformation_14E_Type_Pattern = MT300_SequenceA_GeneralInformation_14E_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceB_TransactionDetails_30T_Type_Pattern
class MT300_SequenceB_TransactionDetails_30T_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceB_TransactionDetails_30T_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 315, 1)
    _Documentation = None
MT300_SequenceB_TransactionDetails_30T_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceB_TransactionDetails_30T_Type_Pattern._CF_pattern.addPattern(pattern='([0-9]{8})')
MT300_SequenceB_TransactionDetails_30T_Type_Pattern._InitializeFacetMap(MT300_SequenceB_TransactionDetails_30T_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceB_TransactionDetails_30T_Type_Pattern', MT300_SequenceB_TransactionDetails_30T_Type_Pattern)
_module_typeBindings.MT300_SequenceB_TransactionDetails_30T_Type_Pattern = MT300_SequenceB_TransactionDetails_30T_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceB_TransactionDetails_30V_Type_Pattern
class MT300_SequenceB_TransactionDetails_30V_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceB_TransactionDetails_30V_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 328, 1)
    _Documentation = None
MT300_SequenceB_TransactionDetails_30V_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceB_TransactionDetails_30V_Type_Pattern._CF_pattern.addPattern(pattern='([0-9]{8})')
MT300_SequenceB_TransactionDetails_30V_Type_Pattern._InitializeFacetMap(MT300_SequenceB_TransactionDetails_30V_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceB_TransactionDetails_30V_Type_Pattern', MT300_SequenceB_TransactionDetails_30V_Type_Pattern)
_module_typeBindings.MT300_SequenceB_TransactionDetails_30V_Type_Pattern = MT300_SequenceB_TransactionDetails_30V_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceB_TransactionDetails_36_Type_Pattern
class MT300_SequenceB_TransactionDetails_36_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceB_TransactionDetails_36_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 341, 1)
    _Documentation = None
MT300_SequenceB_TransactionDetails_36_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceB_TransactionDetails_36_Type_Pattern._CF_pattern.addPattern(pattern='([0-9,(?0-9)]{1,12})')
MT300_SequenceB_TransactionDetails_36_Type_Pattern._InitializeFacetMap(MT300_SequenceB_TransactionDetails_36_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceB_TransactionDetails_36_Type_Pattern', MT300_SequenceB_TransactionDetails_36_Type_Pattern)
_module_typeBindings.MT300_SequenceB_TransactionDetails_36_Type_Pattern = MT300_SequenceB_TransactionDetails_36_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceB_TransactionDetails_39M_Type_Pattern
class MT300_SequenceB_TransactionDetails_39M_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceB_TransactionDetails_39M_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 354, 1)
    _Documentation = None
MT300_SequenceB_TransactionDetails_39M_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceB_TransactionDetails_39M_Type_Pattern._CF_pattern.addPattern(pattern='([A-Z]{2})')
MT300_SequenceB_TransactionDetails_39M_Type_Pattern._InitializeFacetMap(MT300_SequenceB_TransactionDetails_39M_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceB_TransactionDetails_39M_Type_Pattern', MT300_SequenceB_TransactionDetails_39M_Type_Pattern)
_module_typeBindings.MT300_SequenceB_TransactionDetails_39M_Type_Pattern = MT300_SequenceB_TransactionDetails_39M_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SubSequenceB1_AmountBought_32B_Type_Pattern
class MT300_SubSequenceB1_AmountBought_32B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SubSequenceB1_AmountBought_32B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 367, 1)
    _Documentation = None
MT300_SubSequenceB1_AmountBought_32B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SubSequenceB1_AmountBought_32B_Type_Pattern._CF_pattern.addPattern(pattern='((AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})')
MT300_SubSequenceB1_AmountBought_32B_Type_Pattern._InitializeFacetMap(MT300_SubSequenceB1_AmountBought_32B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SubSequenceB1_AmountBought_32B_Type_Pattern', MT300_SubSequenceB1_AmountBought_32B_Type_Pattern)
_module_typeBindings.MT300_SubSequenceB1_AmountBought_32B_Type_Pattern = MT300_SubSequenceB1_AmountBought_32B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_53A_Type_Pattern
class MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_53A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_53A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 380, 1)
    _Documentation = None
MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_53A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_53A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_53A_Type_Pattern._InitializeFacetMap(MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_53A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_53A_Type_Pattern', MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_53A_Type_Pattern)
_module_typeBindings.MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_53A_Type_Pattern = MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_53A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_53J_Type_Pattern
class MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_53J_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_53J_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 393, 1)
    _Documentation = None
MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_53J_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_53J_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,40}\\n?){1,5})")
MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_53J_Type_Pattern._InitializeFacetMap(MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_53J_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_53J_Type_Pattern', MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_53J_Type_Pattern)
_module_typeBindings.MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_53J_Type_Pattern = MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_53J_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_56A_Type_Pattern
class MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_56A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_56A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 406, 1)
    _Documentation = None
MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_56A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_56A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_56A_Type_Pattern._InitializeFacetMap(MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_56A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_56A_Type_Pattern', MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_56A_Type_Pattern)
_module_typeBindings.MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_56A_Type_Pattern = MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_56A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_56J_Type_Pattern
class MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_56J_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_56J_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 419, 1)
    _Documentation = None
MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_56J_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_56J_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,40}\\n?){1,5})")
MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_56J_Type_Pattern._InitializeFacetMap(MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_56J_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_56J_Type_Pattern', MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_56J_Type_Pattern)
_module_typeBindings.MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_56J_Type_Pattern = MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_56J_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_57A_Type_Pattern
class MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_57A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_57A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 432, 1)
    _Documentation = None
MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_57A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_57A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_57A_Type_Pattern._InitializeFacetMap(MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_57A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_57A_Type_Pattern', MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_57A_Type_Pattern)
_module_typeBindings.MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_57A_Type_Pattern = MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_57A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_57J_Type_Pattern
class MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_57J_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_57J_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 445, 1)
    _Documentation = None
MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_57J_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_57J_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,40}\\n?){1,5})")
MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_57J_Type_Pattern._InitializeFacetMap(MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_57J_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_57J_Type_Pattern', MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_57J_Type_Pattern)
_module_typeBindings.MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_57J_Type_Pattern = MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_57J_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SubSequenceB2_AmountSold_33B_Type_Pattern
class MT300_SubSequenceB2_AmountSold_33B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SubSequenceB2_AmountSold_33B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 458, 1)
    _Documentation = None
MT300_SubSequenceB2_AmountSold_33B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SubSequenceB2_AmountSold_33B_Type_Pattern._CF_pattern.addPattern(pattern='((AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})')
MT300_SubSequenceB2_AmountSold_33B_Type_Pattern._InitializeFacetMap(MT300_SubSequenceB2_AmountSold_33B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SubSequenceB2_AmountSold_33B_Type_Pattern', MT300_SubSequenceB2_AmountSold_33B_Type_Pattern)
_module_typeBindings.MT300_SubSequenceB2_AmountSold_33B_Type_Pattern = MT300_SubSequenceB2_AmountSold_33B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_53A_Type_Pattern
class MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_53A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_53A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 471, 1)
    _Documentation = None
MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_53A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_53A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_53A_Type_Pattern._InitializeFacetMap(MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_53A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_53A_Type_Pattern', MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_53A_Type_Pattern)
_module_typeBindings.MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_53A_Type_Pattern = MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_53A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_53J_Type_Pattern
class MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_53J_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_53J_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 484, 1)
    _Documentation = None
MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_53J_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_53J_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,40}\\n?){1,5})")
MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_53J_Type_Pattern._InitializeFacetMap(MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_53J_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_53J_Type_Pattern', MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_53J_Type_Pattern)
_module_typeBindings.MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_53J_Type_Pattern = MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_53J_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_56A_Type_Pattern
class MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_56A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_56A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 497, 1)
    _Documentation = None
MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_56A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_56A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_56A_Type_Pattern._InitializeFacetMap(MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_56A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_56A_Type_Pattern', MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_56A_Type_Pattern)
_module_typeBindings.MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_56A_Type_Pattern = MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_56A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_56J_Type_Pattern
class MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_56J_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_56J_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 510, 1)
    _Documentation = None
MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_56J_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_56J_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,40}\\n?){1,5})")
MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_56J_Type_Pattern._InitializeFacetMap(MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_56J_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_56J_Type_Pattern', MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_56J_Type_Pattern)
_module_typeBindings.MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_56J_Type_Pattern = MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_56J_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_57A_Type_Pattern
class MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_57A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_57A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 523, 1)
    _Documentation = None
MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_57A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_57A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_57A_Type_Pattern._InitializeFacetMap(MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_57A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_57A_Type_Pattern', MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_57A_Type_Pattern)
_module_typeBindings.MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_57A_Type_Pattern = MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_57A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_57J_Type_Pattern
class MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_57J_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_57J_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 536, 1)
    _Documentation = None
MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_57J_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_57J_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,40}\\n?){1,5})")
MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_57J_Type_Pattern._InitializeFacetMap(MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_57J_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_57J_Type_Pattern', MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_57J_Type_Pattern)
_module_typeBindings.MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_57J_Type_Pattern = MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_57J_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_58A_Type_Pattern
class MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_58A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_58A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 549, 1)
    _Documentation = None
MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_58A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_58A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_58A_Type_Pattern._InitializeFacetMap(MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_58A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_58A_Type_Pattern', MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_58A_Type_Pattern)
_module_typeBindings.MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_58A_Type_Pattern = MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_58A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_58J_Type_Pattern
class MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_58J_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_58J_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 562, 1)
    _Documentation = None
MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_58J_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_58J_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,40}\\n?){1,5})")
MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_58J_Type_Pattern._InitializeFacetMap(MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_58J_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_58J_Type_Pattern', MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_58J_Type_Pattern)
_module_typeBindings.MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_58J_Type_Pattern = MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_58J_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceC_OptionalGeneralInformation_29A_Type_Pattern
class MT300_SequenceC_OptionalGeneralInformation_29A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceC_OptionalGeneralInformation_29A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 575, 1)
    _Documentation = None
MT300_SequenceC_OptionalGeneralInformation_29A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceC_OptionalGeneralInformation_29A_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT300_SequenceC_OptionalGeneralInformation_29A_Type_Pattern._InitializeFacetMap(MT300_SequenceC_OptionalGeneralInformation_29A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceC_OptionalGeneralInformation_29A_Type_Pattern', MT300_SequenceC_OptionalGeneralInformation_29A_Type_Pattern)
_module_typeBindings.MT300_SequenceC_OptionalGeneralInformation_29A_Type_Pattern = MT300_SequenceC_OptionalGeneralInformation_29A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceC_OptionalGeneralInformation_24D_Type_Pattern
class MT300_SequenceC_OptionalGeneralInformation_24D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceC_OptionalGeneralInformation_24D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 588, 1)
    _Documentation = None
MT300_SequenceC_OptionalGeneralInformation_24D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceC_OptionalGeneralInformation_24D_Type_Pattern._CF_pattern.addPattern(pattern="((BROK|ELEC|FAXT|PHON|TELX)(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35})?)")
MT300_SequenceC_OptionalGeneralInformation_24D_Type_Pattern._InitializeFacetMap(MT300_SequenceC_OptionalGeneralInformation_24D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceC_OptionalGeneralInformation_24D_Type_Pattern', MT300_SequenceC_OptionalGeneralInformation_24D_Type_Pattern)
_module_typeBindings.MT300_SequenceC_OptionalGeneralInformation_24D_Type_Pattern = MT300_SequenceC_OptionalGeneralInformation_24D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceC_OptionalGeneralInformation_84A_Type_Pattern
class MT300_SequenceC_OptionalGeneralInformation_84A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceC_OptionalGeneralInformation_84A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 601, 1)
    _Documentation = None
MT300_SequenceC_OptionalGeneralInformation_84A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceC_OptionalGeneralInformation_84A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT300_SequenceC_OptionalGeneralInformation_84A_Type_Pattern._InitializeFacetMap(MT300_SequenceC_OptionalGeneralInformation_84A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceC_OptionalGeneralInformation_84A_Type_Pattern', MT300_SequenceC_OptionalGeneralInformation_84A_Type_Pattern)
_module_typeBindings.MT300_SequenceC_OptionalGeneralInformation_84A_Type_Pattern = MT300_SequenceC_OptionalGeneralInformation_84A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceC_OptionalGeneralInformation_84B_Type_Pattern
class MT300_SequenceC_OptionalGeneralInformation_84B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceC_OptionalGeneralInformation_84B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 614, 1)
    _Documentation = None
MT300_SequenceC_OptionalGeneralInformation_84B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceC_OptionalGeneralInformation_84B_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35})?)")
MT300_SequenceC_OptionalGeneralInformation_84B_Type_Pattern._InitializeFacetMap(MT300_SequenceC_OptionalGeneralInformation_84B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceC_OptionalGeneralInformation_84B_Type_Pattern', MT300_SequenceC_OptionalGeneralInformation_84B_Type_Pattern)
_module_typeBindings.MT300_SequenceC_OptionalGeneralInformation_84B_Type_Pattern = MT300_SequenceC_OptionalGeneralInformation_84B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceC_OptionalGeneralInformation_84D_Type_Pattern
class MT300_SequenceC_OptionalGeneralInformation_84D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceC_OptionalGeneralInformation_84D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 627, 1)
    _Documentation = None
MT300_SequenceC_OptionalGeneralInformation_84D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceC_OptionalGeneralInformation_84D_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT300_SequenceC_OptionalGeneralInformation_84D_Type_Pattern._InitializeFacetMap(MT300_SequenceC_OptionalGeneralInformation_84D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceC_OptionalGeneralInformation_84D_Type_Pattern', MT300_SequenceC_OptionalGeneralInformation_84D_Type_Pattern)
_module_typeBindings.MT300_SequenceC_OptionalGeneralInformation_84D_Type_Pattern = MT300_SequenceC_OptionalGeneralInformation_84D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceC_OptionalGeneralInformation_84J_Type_Pattern
class MT300_SequenceC_OptionalGeneralInformation_84J_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceC_OptionalGeneralInformation_84J_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 640, 1)
    _Documentation = None
MT300_SequenceC_OptionalGeneralInformation_84J_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceC_OptionalGeneralInformation_84J_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,40}\\n?){1,5})")
MT300_SequenceC_OptionalGeneralInformation_84J_Type_Pattern._InitializeFacetMap(MT300_SequenceC_OptionalGeneralInformation_84J_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceC_OptionalGeneralInformation_84J_Type_Pattern', MT300_SequenceC_OptionalGeneralInformation_84J_Type_Pattern)
_module_typeBindings.MT300_SequenceC_OptionalGeneralInformation_84J_Type_Pattern = MT300_SequenceC_OptionalGeneralInformation_84J_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceC_OptionalGeneralInformation_85A_Type_Pattern
class MT300_SequenceC_OptionalGeneralInformation_85A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceC_OptionalGeneralInformation_85A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 653, 1)
    _Documentation = None
MT300_SequenceC_OptionalGeneralInformation_85A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceC_OptionalGeneralInformation_85A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT300_SequenceC_OptionalGeneralInformation_85A_Type_Pattern._InitializeFacetMap(MT300_SequenceC_OptionalGeneralInformation_85A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceC_OptionalGeneralInformation_85A_Type_Pattern', MT300_SequenceC_OptionalGeneralInformation_85A_Type_Pattern)
_module_typeBindings.MT300_SequenceC_OptionalGeneralInformation_85A_Type_Pattern = MT300_SequenceC_OptionalGeneralInformation_85A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceC_OptionalGeneralInformation_85B_Type_Pattern
class MT300_SequenceC_OptionalGeneralInformation_85B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceC_OptionalGeneralInformation_85B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 666, 1)
    _Documentation = None
MT300_SequenceC_OptionalGeneralInformation_85B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceC_OptionalGeneralInformation_85B_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35})?)")
MT300_SequenceC_OptionalGeneralInformation_85B_Type_Pattern._InitializeFacetMap(MT300_SequenceC_OptionalGeneralInformation_85B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceC_OptionalGeneralInformation_85B_Type_Pattern', MT300_SequenceC_OptionalGeneralInformation_85B_Type_Pattern)
_module_typeBindings.MT300_SequenceC_OptionalGeneralInformation_85B_Type_Pattern = MT300_SequenceC_OptionalGeneralInformation_85B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceC_OptionalGeneralInformation_85D_Type_Pattern
class MT300_SequenceC_OptionalGeneralInformation_85D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceC_OptionalGeneralInformation_85D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 679, 1)
    _Documentation = None
MT300_SequenceC_OptionalGeneralInformation_85D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceC_OptionalGeneralInformation_85D_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT300_SequenceC_OptionalGeneralInformation_85D_Type_Pattern._InitializeFacetMap(MT300_SequenceC_OptionalGeneralInformation_85D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceC_OptionalGeneralInformation_85D_Type_Pattern', MT300_SequenceC_OptionalGeneralInformation_85D_Type_Pattern)
_module_typeBindings.MT300_SequenceC_OptionalGeneralInformation_85D_Type_Pattern = MT300_SequenceC_OptionalGeneralInformation_85D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceC_OptionalGeneralInformation_85J_Type_Pattern
class MT300_SequenceC_OptionalGeneralInformation_85J_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceC_OptionalGeneralInformation_85J_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 692, 1)
    _Documentation = None
MT300_SequenceC_OptionalGeneralInformation_85J_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceC_OptionalGeneralInformation_85J_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,40}\\n?){1,5})")
MT300_SequenceC_OptionalGeneralInformation_85J_Type_Pattern._InitializeFacetMap(MT300_SequenceC_OptionalGeneralInformation_85J_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceC_OptionalGeneralInformation_85J_Type_Pattern', MT300_SequenceC_OptionalGeneralInformation_85J_Type_Pattern)
_module_typeBindings.MT300_SequenceC_OptionalGeneralInformation_85J_Type_Pattern = MT300_SequenceC_OptionalGeneralInformation_85J_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceC_OptionalGeneralInformation_88A_Type_Pattern
class MT300_SequenceC_OptionalGeneralInformation_88A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceC_OptionalGeneralInformation_88A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 705, 1)
    _Documentation = None
MT300_SequenceC_OptionalGeneralInformation_88A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceC_OptionalGeneralInformation_88A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT300_SequenceC_OptionalGeneralInformation_88A_Type_Pattern._InitializeFacetMap(MT300_SequenceC_OptionalGeneralInformation_88A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceC_OptionalGeneralInformation_88A_Type_Pattern', MT300_SequenceC_OptionalGeneralInformation_88A_Type_Pattern)
_module_typeBindings.MT300_SequenceC_OptionalGeneralInformation_88A_Type_Pattern = MT300_SequenceC_OptionalGeneralInformation_88A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceC_OptionalGeneralInformation_88D_Type_Pattern
class MT300_SequenceC_OptionalGeneralInformation_88D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceC_OptionalGeneralInformation_88D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 718, 1)
    _Documentation = None
MT300_SequenceC_OptionalGeneralInformation_88D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceC_OptionalGeneralInformation_88D_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT300_SequenceC_OptionalGeneralInformation_88D_Type_Pattern._InitializeFacetMap(MT300_SequenceC_OptionalGeneralInformation_88D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceC_OptionalGeneralInformation_88D_Type_Pattern', MT300_SequenceC_OptionalGeneralInformation_88D_Type_Pattern)
_module_typeBindings.MT300_SequenceC_OptionalGeneralInformation_88D_Type_Pattern = MT300_SequenceC_OptionalGeneralInformation_88D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceC_OptionalGeneralInformation_88J_Type_Pattern
class MT300_SequenceC_OptionalGeneralInformation_88J_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceC_OptionalGeneralInformation_88J_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 731, 1)
    _Documentation = None
MT300_SequenceC_OptionalGeneralInformation_88J_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceC_OptionalGeneralInformation_88J_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,40}\\n?){1,5})")
MT300_SequenceC_OptionalGeneralInformation_88J_Type_Pattern._InitializeFacetMap(MT300_SequenceC_OptionalGeneralInformation_88J_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceC_OptionalGeneralInformation_88J_Type_Pattern', MT300_SequenceC_OptionalGeneralInformation_88J_Type_Pattern)
_module_typeBindings.MT300_SequenceC_OptionalGeneralInformation_88J_Type_Pattern = MT300_SequenceC_OptionalGeneralInformation_88J_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceC_OptionalGeneralInformation_71F_Type_Pattern
class MT300_SequenceC_OptionalGeneralInformation_71F_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceC_OptionalGeneralInformation_71F_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 744, 1)
    _Documentation = None
MT300_SequenceC_OptionalGeneralInformation_71F_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceC_OptionalGeneralInformation_71F_Type_Pattern._CF_pattern.addPattern(pattern='((AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})')
MT300_SequenceC_OptionalGeneralInformation_71F_Type_Pattern._InitializeFacetMap(MT300_SequenceC_OptionalGeneralInformation_71F_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceC_OptionalGeneralInformation_71F_Type_Pattern', MT300_SequenceC_OptionalGeneralInformation_71F_Type_Pattern)
_module_typeBindings.MT300_SequenceC_OptionalGeneralInformation_71F_Type_Pattern = MT300_SequenceC_OptionalGeneralInformation_71F_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceC_OptionalGeneralInformation_26H_Type_Pattern
class MT300_SequenceC_OptionalGeneralInformation_26H_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceC_OptionalGeneralInformation_26H_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 757, 1)
    _Documentation = None
MT300_SequenceC_OptionalGeneralInformation_26H_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceC_OptionalGeneralInformation_26H_Type_Pattern._CF_pattern.addPattern(pattern="(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,16})")
MT300_SequenceC_OptionalGeneralInformation_26H_Type_Pattern._InitializeFacetMap(MT300_SequenceC_OptionalGeneralInformation_26H_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceC_OptionalGeneralInformation_26H_Type_Pattern', MT300_SequenceC_OptionalGeneralInformation_26H_Type_Pattern)
_module_typeBindings.MT300_SequenceC_OptionalGeneralInformation_26H_Type_Pattern = MT300_SequenceC_OptionalGeneralInformation_26H_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceC_OptionalGeneralInformation_21G_Type_Pattern
class MT300_SequenceC_OptionalGeneralInformation_21G_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceC_OptionalGeneralInformation_21G_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 770, 1)
    _Documentation = None
MT300_SequenceC_OptionalGeneralInformation_21G_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceC_OptionalGeneralInformation_21G_Type_Pattern._CF_pattern.addPattern(pattern="(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,16})")
MT300_SequenceC_OptionalGeneralInformation_21G_Type_Pattern._InitializeFacetMap(MT300_SequenceC_OptionalGeneralInformation_21G_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceC_OptionalGeneralInformation_21G_Type_Pattern', MT300_SequenceC_OptionalGeneralInformation_21G_Type_Pattern)
_module_typeBindings.MT300_SequenceC_OptionalGeneralInformation_21G_Type_Pattern = MT300_SequenceC_OptionalGeneralInformation_21G_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceC_OptionalGeneralInformation_72_Type_Pattern
class MT300_SequenceC_OptionalGeneralInformation_72_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceC_OptionalGeneralInformation_72_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 783, 1)
    _Documentation = None
MT300_SequenceC_OptionalGeneralInformation_72_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceC_OptionalGeneralInformation_72_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,6})")
MT300_SequenceC_OptionalGeneralInformation_72_Type_Pattern._InitializeFacetMap(MT300_SequenceC_OptionalGeneralInformation_72_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceC_OptionalGeneralInformation_72_Type_Pattern', MT300_SequenceC_OptionalGeneralInformation_72_Type_Pattern)
_module_typeBindings.MT300_SequenceC_OptionalGeneralInformation_72_Type_Pattern = MT300_SequenceC_OptionalGeneralInformation_72_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceD_SplitSettlementDetails_SettlementDetails_17A_Type_Pattern
class MT300_SequenceD_SplitSettlementDetails_SettlementDetails_17A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceD_SplitSettlementDetails_SettlementDetails_17A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 796, 1)
    _Documentation = None
MT300_SequenceD_SplitSettlementDetails_SettlementDetails_17A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceD_SplitSettlementDetails_SettlementDetails_17A_Type_Pattern._CF_pattern.addPattern(pattern='(N|[0-9])')
MT300_SequenceD_SplitSettlementDetails_SettlementDetails_17A_Type_Pattern._InitializeFacetMap(MT300_SequenceD_SplitSettlementDetails_SettlementDetails_17A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceD_SplitSettlementDetails_SettlementDetails_17A_Type_Pattern', MT300_SequenceD_SplitSettlementDetails_SettlementDetails_17A_Type_Pattern)
_module_typeBindings.MT300_SequenceD_SplitSettlementDetails_SettlementDetails_17A_Type_Pattern = MT300_SequenceD_SplitSettlementDetails_SettlementDetails_17A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceD_SplitSettlementDetails_SettlementDetails_32B_Type_Pattern
class MT300_SequenceD_SplitSettlementDetails_SettlementDetails_32B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceD_SplitSettlementDetails_SettlementDetails_32B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 809, 1)
    _Documentation = None
MT300_SequenceD_SplitSettlementDetails_SettlementDetails_32B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceD_SplitSettlementDetails_SettlementDetails_32B_Type_Pattern._CF_pattern.addPattern(pattern='((AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})')
MT300_SequenceD_SplitSettlementDetails_SettlementDetails_32B_Type_Pattern._InitializeFacetMap(MT300_SequenceD_SplitSettlementDetails_SettlementDetails_32B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceD_SplitSettlementDetails_SettlementDetails_32B_Type_Pattern', MT300_SequenceD_SplitSettlementDetails_SettlementDetails_32B_Type_Pattern)
_module_typeBindings.MT300_SequenceD_SplitSettlementDetails_SettlementDetails_32B_Type_Pattern = MT300_SequenceD_SplitSettlementDetails_SettlementDetails_32B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceD_SplitSettlementDetails_SettlementDetails_53A_Type_Pattern
class MT300_SequenceD_SplitSettlementDetails_SettlementDetails_53A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceD_SplitSettlementDetails_SettlementDetails_53A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 822, 1)
    _Documentation = None
MT300_SequenceD_SplitSettlementDetails_SettlementDetails_53A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceD_SplitSettlementDetails_SettlementDetails_53A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT300_SequenceD_SplitSettlementDetails_SettlementDetails_53A_Type_Pattern._InitializeFacetMap(MT300_SequenceD_SplitSettlementDetails_SettlementDetails_53A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceD_SplitSettlementDetails_SettlementDetails_53A_Type_Pattern', MT300_SequenceD_SplitSettlementDetails_SettlementDetails_53A_Type_Pattern)
_module_typeBindings.MT300_SequenceD_SplitSettlementDetails_SettlementDetails_53A_Type_Pattern = MT300_SequenceD_SplitSettlementDetails_SettlementDetails_53A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceD_SplitSettlementDetails_SettlementDetails_53D_Type_Pattern
class MT300_SequenceD_SplitSettlementDetails_SettlementDetails_53D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceD_SplitSettlementDetails_SettlementDetails_53D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 835, 1)
    _Documentation = None
MT300_SequenceD_SplitSettlementDetails_SettlementDetails_53D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceD_SplitSettlementDetails_SettlementDetails_53D_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT300_SequenceD_SplitSettlementDetails_SettlementDetails_53D_Type_Pattern._InitializeFacetMap(MT300_SequenceD_SplitSettlementDetails_SettlementDetails_53D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceD_SplitSettlementDetails_SettlementDetails_53D_Type_Pattern', MT300_SequenceD_SplitSettlementDetails_SettlementDetails_53D_Type_Pattern)
_module_typeBindings.MT300_SequenceD_SplitSettlementDetails_SettlementDetails_53D_Type_Pattern = MT300_SequenceD_SplitSettlementDetails_SettlementDetails_53D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceD_SplitSettlementDetails_SettlementDetails_53J_Type_Pattern
class MT300_SequenceD_SplitSettlementDetails_SettlementDetails_53J_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceD_SplitSettlementDetails_SettlementDetails_53J_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 848, 1)
    _Documentation = None
MT300_SequenceD_SplitSettlementDetails_SettlementDetails_53J_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceD_SplitSettlementDetails_SettlementDetails_53J_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,40}\\n?){1,5})")
MT300_SequenceD_SplitSettlementDetails_SettlementDetails_53J_Type_Pattern._InitializeFacetMap(MT300_SequenceD_SplitSettlementDetails_SettlementDetails_53J_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceD_SplitSettlementDetails_SettlementDetails_53J_Type_Pattern', MT300_SequenceD_SplitSettlementDetails_SettlementDetails_53J_Type_Pattern)
_module_typeBindings.MT300_SequenceD_SplitSettlementDetails_SettlementDetails_53J_Type_Pattern = MT300_SequenceD_SplitSettlementDetails_SettlementDetails_53J_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceD_SplitSettlementDetails_SettlementDetails_56A_Type_Pattern
class MT300_SequenceD_SplitSettlementDetails_SettlementDetails_56A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceD_SplitSettlementDetails_SettlementDetails_56A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 861, 1)
    _Documentation = None
MT300_SequenceD_SplitSettlementDetails_SettlementDetails_56A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceD_SplitSettlementDetails_SettlementDetails_56A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT300_SequenceD_SplitSettlementDetails_SettlementDetails_56A_Type_Pattern._InitializeFacetMap(MT300_SequenceD_SplitSettlementDetails_SettlementDetails_56A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceD_SplitSettlementDetails_SettlementDetails_56A_Type_Pattern', MT300_SequenceD_SplitSettlementDetails_SettlementDetails_56A_Type_Pattern)
_module_typeBindings.MT300_SequenceD_SplitSettlementDetails_SettlementDetails_56A_Type_Pattern = MT300_SequenceD_SplitSettlementDetails_SettlementDetails_56A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceD_SplitSettlementDetails_SettlementDetails_56D_Type_Pattern
class MT300_SequenceD_SplitSettlementDetails_SettlementDetails_56D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceD_SplitSettlementDetails_SettlementDetails_56D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 874, 1)
    _Documentation = None
MT300_SequenceD_SplitSettlementDetails_SettlementDetails_56D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceD_SplitSettlementDetails_SettlementDetails_56D_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT300_SequenceD_SplitSettlementDetails_SettlementDetails_56D_Type_Pattern._InitializeFacetMap(MT300_SequenceD_SplitSettlementDetails_SettlementDetails_56D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceD_SplitSettlementDetails_SettlementDetails_56D_Type_Pattern', MT300_SequenceD_SplitSettlementDetails_SettlementDetails_56D_Type_Pattern)
_module_typeBindings.MT300_SequenceD_SplitSettlementDetails_SettlementDetails_56D_Type_Pattern = MT300_SequenceD_SplitSettlementDetails_SettlementDetails_56D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceD_SplitSettlementDetails_SettlementDetails_56J_Type_Pattern
class MT300_SequenceD_SplitSettlementDetails_SettlementDetails_56J_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceD_SplitSettlementDetails_SettlementDetails_56J_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 887, 1)
    _Documentation = None
MT300_SequenceD_SplitSettlementDetails_SettlementDetails_56J_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceD_SplitSettlementDetails_SettlementDetails_56J_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,40}\\n?){1,5})")
MT300_SequenceD_SplitSettlementDetails_SettlementDetails_56J_Type_Pattern._InitializeFacetMap(MT300_SequenceD_SplitSettlementDetails_SettlementDetails_56J_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceD_SplitSettlementDetails_SettlementDetails_56J_Type_Pattern', MT300_SequenceD_SplitSettlementDetails_SettlementDetails_56J_Type_Pattern)
_module_typeBindings.MT300_SequenceD_SplitSettlementDetails_SettlementDetails_56J_Type_Pattern = MT300_SequenceD_SplitSettlementDetails_SettlementDetails_56J_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceD_SplitSettlementDetails_SettlementDetails_57A_Type_Pattern
class MT300_SequenceD_SplitSettlementDetails_SettlementDetails_57A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceD_SplitSettlementDetails_SettlementDetails_57A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 900, 1)
    _Documentation = None
MT300_SequenceD_SplitSettlementDetails_SettlementDetails_57A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceD_SplitSettlementDetails_SettlementDetails_57A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT300_SequenceD_SplitSettlementDetails_SettlementDetails_57A_Type_Pattern._InitializeFacetMap(MT300_SequenceD_SplitSettlementDetails_SettlementDetails_57A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceD_SplitSettlementDetails_SettlementDetails_57A_Type_Pattern', MT300_SequenceD_SplitSettlementDetails_SettlementDetails_57A_Type_Pattern)
_module_typeBindings.MT300_SequenceD_SplitSettlementDetails_SettlementDetails_57A_Type_Pattern = MT300_SequenceD_SplitSettlementDetails_SettlementDetails_57A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceD_SplitSettlementDetails_SettlementDetails_57D_Type_Pattern
class MT300_SequenceD_SplitSettlementDetails_SettlementDetails_57D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceD_SplitSettlementDetails_SettlementDetails_57D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 913, 1)
    _Documentation = None
MT300_SequenceD_SplitSettlementDetails_SettlementDetails_57D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceD_SplitSettlementDetails_SettlementDetails_57D_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT300_SequenceD_SplitSettlementDetails_SettlementDetails_57D_Type_Pattern._InitializeFacetMap(MT300_SequenceD_SplitSettlementDetails_SettlementDetails_57D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceD_SplitSettlementDetails_SettlementDetails_57D_Type_Pattern', MT300_SequenceD_SplitSettlementDetails_SettlementDetails_57D_Type_Pattern)
_module_typeBindings.MT300_SequenceD_SplitSettlementDetails_SettlementDetails_57D_Type_Pattern = MT300_SequenceD_SplitSettlementDetails_SettlementDetails_57D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceD_SplitSettlementDetails_SettlementDetails_57J_Type_Pattern
class MT300_SequenceD_SplitSettlementDetails_SettlementDetails_57J_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceD_SplitSettlementDetails_SettlementDetails_57J_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 926, 1)
    _Documentation = None
MT300_SequenceD_SplitSettlementDetails_SettlementDetails_57J_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceD_SplitSettlementDetails_SettlementDetails_57J_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,40}\\n?){1,5})")
MT300_SequenceD_SplitSettlementDetails_SettlementDetails_57J_Type_Pattern._InitializeFacetMap(MT300_SequenceD_SplitSettlementDetails_SettlementDetails_57J_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceD_SplitSettlementDetails_SettlementDetails_57J_Type_Pattern', MT300_SequenceD_SplitSettlementDetails_SettlementDetails_57J_Type_Pattern)
_module_typeBindings.MT300_SequenceD_SplitSettlementDetails_SettlementDetails_57J_Type_Pattern = MT300_SequenceD_SplitSettlementDetails_SettlementDetails_57J_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceD_SplitSettlementDetails_SettlementDetails_58A_Type_Pattern
class MT300_SequenceD_SplitSettlementDetails_SettlementDetails_58A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceD_SplitSettlementDetails_SettlementDetails_58A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 939, 1)
    _Documentation = None
MT300_SequenceD_SplitSettlementDetails_SettlementDetails_58A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceD_SplitSettlementDetails_SettlementDetails_58A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT300_SequenceD_SplitSettlementDetails_SettlementDetails_58A_Type_Pattern._InitializeFacetMap(MT300_SequenceD_SplitSettlementDetails_SettlementDetails_58A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceD_SplitSettlementDetails_SettlementDetails_58A_Type_Pattern', MT300_SequenceD_SplitSettlementDetails_SettlementDetails_58A_Type_Pattern)
_module_typeBindings.MT300_SequenceD_SplitSettlementDetails_SettlementDetails_58A_Type_Pattern = MT300_SequenceD_SplitSettlementDetails_SettlementDetails_58A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceD_SplitSettlementDetails_SettlementDetails_58D_Type_Pattern
class MT300_SequenceD_SplitSettlementDetails_SettlementDetails_58D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceD_SplitSettlementDetails_SettlementDetails_58D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 952, 1)
    _Documentation = None
MT300_SequenceD_SplitSettlementDetails_SettlementDetails_58D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceD_SplitSettlementDetails_SettlementDetails_58D_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT300_SequenceD_SplitSettlementDetails_SettlementDetails_58D_Type_Pattern._InitializeFacetMap(MT300_SequenceD_SplitSettlementDetails_SettlementDetails_58D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceD_SplitSettlementDetails_SettlementDetails_58D_Type_Pattern', MT300_SequenceD_SplitSettlementDetails_SettlementDetails_58D_Type_Pattern)
_module_typeBindings.MT300_SequenceD_SplitSettlementDetails_SettlementDetails_58D_Type_Pattern = MT300_SequenceD_SplitSettlementDetails_SettlementDetails_58D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceD_SplitSettlementDetails_SettlementDetails_58J_Type_Pattern
class MT300_SequenceD_SplitSettlementDetails_SettlementDetails_58J_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceD_SplitSettlementDetails_SettlementDetails_58J_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 965, 1)
    _Documentation = None
MT300_SequenceD_SplitSettlementDetails_SettlementDetails_58J_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceD_SplitSettlementDetails_SettlementDetails_58J_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,40}\\n?){1,5})")
MT300_SequenceD_SplitSettlementDetails_SettlementDetails_58J_Type_Pattern._InitializeFacetMap(MT300_SequenceD_SplitSettlementDetails_SettlementDetails_58J_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceD_SplitSettlementDetails_SettlementDetails_58J_Type_Pattern', MT300_SequenceD_SplitSettlementDetails_SettlementDetails_58J_Type_Pattern)
_module_typeBindings.MT300_SequenceD_SplitSettlementDetails_SettlementDetails_58J_Type_Pattern = MT300_SequenceD_SplitSettlementDetails_SettlementDetails_58J_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceD_SplitSettlementDetails_16A_Type_Pattern
class MT300_SequenceD_SplitSettlementDetails_16A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceD_SplitSettlementDetails_16A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 978, 1)
    _Documentation = None
MT300_SequenceD_SplitSettlementDetails_16A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceD_SplitSettlementDetails_16A_Type_Pattern._CF_pattern.addPattern(pattern='([0-9]{1,5})')
MT300_SequenceD_SplitSettlementDetails_16A_Type_Pattern._InitializeFacetMap(MT300_SequenceD_SplitSettlementDetails_16A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceD_SplitSettlementDetails_16A_Type_Pattern', MT300_SequenceD_SplitSettlementDetails_16A_Type_Pattern)
_module_typeBindings.MT300_SequenceD_SplitSettlementDetails_16A_Type_Pattern = MT300_SequenceD_SplitSettlementDetails_16A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_22L_Type_Pattern
class MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_22L_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_22L_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 991, 1)
    _Documentation = None
MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_22L_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_22L_Type_Pattern._CF_pattern.addPattern(pattern="(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35})")
MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_22L_Type_Pattern._InitializeFacetMap(MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_22L_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_22L_Type_Pattern', MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_22L_Type_Pattern)
_module_typeBindings.MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_22L_Type_Pattern = MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_22L_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_91A_Type_Pattern
class MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_91A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_91A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1004, 1)
    _Documentation = None
MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_91A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_91A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_91A_Type_Pattern._InitializeFacetMap(MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_91A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_91A_Type_Pattern', MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_91A_Type_Pattern)
_module_typeBindings.MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_91A_Type_Pattern = MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_91A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_91D_Type_Pattern
class MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_91D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_91D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1017, 1)
    _Documentation = None
MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_91D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_91D_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_91D_Type_Pattern._InitializeFacetMap(MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_91D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_91D_Type_Pattern', MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_91D_Type_Pattern)
_module_typeBindings.MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_91D_Type_Pattern = MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_91D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_91J_Type_Pattern
class MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_91J_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_91J_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1030, 1)
    _Documentation = None
MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_91J_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_91J_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,40}\\n?){1,5})")
MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_91J_Type_Pattern._InitializeFacetMap(MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_91J_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_91J_Type_Pattern', MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_91J_Type_Pattern)
_module_typeBindings.MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_91J_Type_Pattern = MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_91J_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_22M_Type_Pattern
class MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_22M_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_22M_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1043, 1)
    _Documentation = None
MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_22M_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_22M_Type_Pattern._CF_pattern.addPattern(pattern="(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,30})")
MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_22M_Type_Pattern._InitializeFacetMap(MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_22M_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_22M_Type_Pattern', MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_22M_Type_Pattern)
_module_typeBindings.MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_22M_Type_Pattern = MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_22M_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_22N_Type_Pattern
class MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_22N_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_22N_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1056, 1)
    _Documentation = None
MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_22N_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_22N_Type_Pattern._CF_pattern.addPattern(pattern="(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,32})")
MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_22N_Type_Pattern._InitializeFacetMap(MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_22N_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_22N_Type_Pattern', MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_22N_Type_Pattern)
_module_typeBindings.MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_22N_Type_Pattern = MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_22N_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_SubSequenceE1a1_PriorUniqueTransactionIdentifier_22P_Type_Pattern
class MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_SubSequenceE1a1_PriorUniqueTransactionIdentifier_22P_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_SubSequenceE1a1_PriorUniqueTransactionIdentifier_22P_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1069, 1)
    _Documentation = None
MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_SubSequenceE1a1_PriorUniqueTransactionIdentifier_22P_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_SubSequenceE1a1_PriorUniqueTransactionIdentifier_22P_Type_Pattern._CF_pattern.addPattern(pattern="(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,30})")
MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_SubSequenceE1a1_PriorUniqueTransactionIdentifier_22P_Type_Pattern._InitializeFacetMap(MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_SubSequenceE1a1_PriorUniqueTransactionIdentifier_22P_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_SubSequenceE1a1_PriorUniqueTransactionIdentifier_22P_Type_Pattern', MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_SubSequenceE1a1_PriorUniqueTransactionIdentifier_22P_Type_Pattern)
_module_typeBindings.MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_SubSequenceE1a1_PriorUniqueTransactionIdentifier_22P_Type_Pattern = MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_SubSequenceE1a1_PriorUniqueTransactionIdentifier_22P_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_SubSequenceE1a1_PriorUniqueTransactionIdentifier_22R_Type_Pattern
class MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_SubSequenceE1a1_PriorUniqueTransactionIdentifier_22R_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_SubSequenceE1a1_PriorUniqueTransactionIdentifier_22R_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1082, 1)
    _Documentation = None
MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_SubSequenceE1a1_PriorUniqueTransactionIdentifier_22R_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_SubSequenceE1a1_PriorUniqueTransactionIdentifier_22R_Type_Pattern._CF_pattern.addPattern(pattern="(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,32})")
MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_SubSequenceE1a1_PriorUniqueTransactionIdentifier_22R_Type_Pattern._InitializeFacetMap(MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_SubSequenceE1a1_PriorUniqueTransactionIdentifier_22R_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_SubSequenceE1a1_PriorUniqueTransactionIdentifier_22R_Type_Pattern', MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_SubSequenceE1a1_PriorUniqueTransactionIdentifier_22R_Type_Pattern)
_module_typeBindings.MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_SubSequenceE1a1_PriorUniqueTransactionIdentifier_22R_Type_Pattern = MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_SubSequenceE1a1_PriorUniqueTransactionIdentifier_22R_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_81A_Type_Pattern
class MT300_SequenceE_ReportingInformation_81A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceE_ReportingInformation_81A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1095, 1)
    _Documentation = None
MT300_SequenceE_ReportingInformation_81A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceE_ReportingInformation_81A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT300_SequenceE_ReportingInformation_81A_Type_Pattern._InitializeFacetMap(MT300_SequenceE_ReportingInformation_81A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceE_ReportingInformation_81A_Type_Pattern', MT300_SequenceE_ReportingInformation_81A_Type_Pattern)
_module_typeBindings.MT300_SequenceE_ReportingInformation_81A_Type_Pattern = MT300_SequenceE_ReportingInformation_81A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_81D_Type_Pattern
class MT300_SequenceE_ReportingInformation_81D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceE_ReportingInformation_81D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1108, 1)
    _Documentation = None
MT300_SequenceE_ReportingInformation_81D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceE_ReportingInformation_81D_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT300_SequenceE_ReportingInformation_81D_Type_Pattern._InitializeFacetMap(MT300_SequenceE_ReportingInformation_81D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceE_ReportingInformation_81D_Type_Pattern', MT300_SequenceE_ReportingInformation_81D_Type_Pattern)
_module_typeBindings.MT300_SequenceE_ReportingInformation_81D_Type_Pattern = MT300_SequenceE_ReportingInformation_81D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_81J_Type_Pattern
class MT300_SequenceE_ReportingInformation_81J_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceE_ReportingInformation_81J_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1121, 1)
    _Documentation = None
MT300_SequenceE_ReportingInformation_81J_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceE_ReportingInformation_81J_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,40}\\n?){1,5})")
MT300_SequenceE_ReportingInformation_81J_Type_Pattern._InitializeFacetMap(MT300_SequenceE_ReportingInformation_81J_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceE_ReportingInformation_81J_Type_Pattern', MT300_SequenceE_ReportingInformation_81J_Type_Pattern)
_module_typeBindings.MT300_SequenceE_ReportingInformation_81J_Type_Pattern = MT300_SequenceE_ReportingInformation_81J_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_89A_Type_Pattern
class MT300_SequenceE_ReportingInformation_89A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceE_ReportingInformation_89A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1134, 1)
    _Documentation = None
MT300_SequenceE_ReportingInformation_89A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceE_ReportingInformation_89A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT300_SequenceE_ReportingInformation_89A_Type_Pattern._InitializeFacetMap(MT300_SequenceE_ReportingInformation_89A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceE_ReportingInformation_89A_Type_Pattern', MT300_SequenceE_ReportingInformation_89A_Type_Pattern)
_module_typeBindings.MT300_SequenceE_ReportingInformation_89A_Type_Pattern = MT300_SequenceE_ReportingInformation_89A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_89D_Type_Pattern
class MT300_SequenceE_ReportingInformation_89D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceE_ReportingInformation_89D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1147, 1)
    _Documentation = None
MT300_SequenceE_ReportingInformation_89D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceE_ReportingInformation_89D_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT300_SequenceE_ReportingInformation_89D_Type_Pattern._InitializeFacetMap(MT300_SequenceE_ReportingInformation_89D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceE_ReportingInformation_89D_Type_Pattern', MT300_SequenceE_ReportingInformation_89D_Type_Pattern)
_module_typeBindings.MT300_SequenceE_ReportingInformation_89D_Type_Pattern = MT300_SequenceE_ReportingInformation_89D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_89J_Type_Pattern
class MT300_SequenceE_ReportingInformation_89J_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceE_ReportingInformation_89J_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1160, 1)
    _Documentation = None
MT300_SequenceE_ReportingInformation_89J_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceE_ReportingInformation_89J_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,40}\\n?){1,5})")
MT300_SequenceE_ReportingInformation_89J_Type_Pattern._InitializeFacetMap(MT300_SequenceE_ReportingInformation_89J_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceE_ReportingInformation_89J_Type_Pattern', MT300_SequenceE_ReportingInformation_89J_Type_Pattern)
_module_typeBindings.MT300_SequenceE_ReportingInformation_89J_Type_Pattern = MT300_SequenceE_ReportingInformation_89J_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_96A_Type_Pattern
class MT300_SequenceE_ReportingInformation_96A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceE_ReportingInformation_96A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1173, 1)
    _Documentation = None
MT300_SequenceE_ReportingInformation_96A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceE_ReportingInformation_96A_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?)")
MT300_SequenceE_ReportingInformation_96A_Type_Pattern._InitializeFacetMap(MT300_SequenceE_ReportingInformation_96A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceE_ReportingInformation_96A_Type_Pattern', MT300_SequenceE_ReportingInformation_96A_Type_Pattern)
_module_typeBindings.MT300_SequenceE_ReportingInformation_96A_Type_Pattern = MT300_SequenceE_ReportingInformation_96A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_96D_Type_Pattern
class MT300_SequenceE_ReportingInformation_96D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceE_ReportingInformation_96D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1186, 1)
    _Documentation = None
MT300_SequenceE_ReportingInformation_96D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceE_ReportingInformation_96D_Type_Pattern._CF_pattern.addPattern(pattern="((/[A-Z]{1})?(/([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,34})?(\\n)?(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})")
MT300_SequenceE_ReportingInformation_96D_Type_Pattern._InitializeFacetMap(MT300_SequenceE_ReportingInformation_96D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceE_ReportingInformation_96D_Type_Pattern', MT300_SequenceE_ReportingInformation_96D_Type_Pattern)
_module_typeBindings.MT300_SequenceE_ReportingInformation_96D_Type_Pattern = MT300_SequenceE_ReportingInformation_96D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_96J_Type_Pattern
class MT300_SequenceE_ReportingInformation_96J_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceE_ReportingInformation_96J_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1199, 1)
    _Documentation = None
MT300_SequenceE_ReportingInformation_96J_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceE_ReportingInformation_96J_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,40}\\n?){1,5})")
MT300_SequenceE_ReportingInformation_96J_Type_Pattern._InitializeFacetMap(MT300_SequenceE_ReportingInformation_96J_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceE_ReportingInformation_96J_Type_Pattern', MT300_SequenceE_ReportingInformation_96J_Type_Pattern)
_module_typeBindings.MT300_SequenceE_ReportingInformation_96J_Type_Pattern = MT300_SequenceE_ReportingInformation_96J_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_22S_Type_Pattern
class MT300_SequenceE_ReportingInformation_22S_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceE_ReportingInformation_22S_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1212, 1)
    _Documentation = None
MT300_SequenceE_ReportingInformation_22S_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceE_ReportingInformation_22S_Type_Pattern._CF_pattern.addPattern(pattern="((C|P)/(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35})?)")
MT300_SequenceE_ReportingInformation_22S_Type_Pattern._InitializeFacetMap(MT300_SequenceE_ReportingInformation_22S_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceE_ReportingInformation_22S_Type_Pattern', MT300_SequenceE_ReportingInformation_22S_Type_Pattern)
_module_typeBindings.MT300_SequenceE_ReportingInformation_22S_Type_Pattern = MT300_SequenceE_ReportingInformation_22S_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_22T_Type_Pattern
class MT300_SequenceE_ReportingInformation_22T_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceE_ReportingInformation_22T_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1225, 1)
    _Documentation = None
MT300_SequenceE_ReportingInformation_22T_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceE_ReportingInformation_22T_Type_Pattern._CF_pattern.addPattern(pattern="(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35})")
MT300_SequenceE_ReportingInformation_22T_Type_Pattern._InitializeFacetMap(MT300_SequenceE_ReportingInformation_22T_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceE_ReportingInformation_22T_Type_Pattern', MT300_SequenceE_ReportingInformation_22T_Type_Pattern)
_module_typeBindings.MT300_SequenceE_ReportingInformation_22T_Type_Pattern = MT300_SequenceE_ReportingInformation_22T_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_17E_Type_Pattern
class MT300_SequenceE_ReportingInformation_17E_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceE_ReportingInformation_17E_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1238, 1)
    _Documentation = None
MT300_SequenceE_ReportingInformation_17E_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceE_ReportingInformation_17E_Type_Pattern._CF_pattern.addPattern(pattern='((N|Y))')
MT300_SequenceE_ReportingInformation_17E_Type_Pattern._InitializeFacetMap(MT300_SequenceE_ReportingInformation_17E_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceE_ReportingInformation_17E_Type_Pattern', MT300_SequenceE_ReportingInformation_17E_Type_Pattern)
_module_typeBindings.MT300_SequenceE_ReportingInformation_17E_Type_Pattern = MT300_SequenceE_ReportingInformation_17E_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_22U_Type_Pattern
class MT300_SequenceE_ReportingInformation_22U_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceE_ReportingInformation_22U_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1251, 1)
    _Documentation = None
MT300_SequenceE_ReportingInformation_22U_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceE_ReportingInformation_22U_Type_Pattern._CF_pattern.addPattern(pattern='((FXFORW|FXNDFO|FXSPOT|FXSWAP))')
MT300_SequenceE_ReportingInformation_22U_Type_Pattern._InitializeFacetMap(MT300_SequenceE_ReportingInformation_22U_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceE_ReportingInformation_22U_Type_Pattern', MT300_SequenceE_ReportingInformation_22U_Type_Pattern)
_module_typeBindings.MT300_SequenceE_ReportingInformation_22U_Type_Pattern = MT300_SequenceE_ReportingInformation_22U_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_35B_Type_Pattern
class MT300_SequenceE_ReportingInformation_35B_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceE_ReportingInformation_35B_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1264, 1)
    _Documentation = None
MT300_SequenceE_ReportingInformation_35B_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceE_ReportingInformation_35B_Type_Pattern._CF_pattern.addPattern(pattern="((ISIN {1}[A-Z0-9]{12})?(\\n(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,4})?)")
MT300_SequenceE_ReportingInformation_35B_Type_Pattern._InitializeFacetMap(MT300_SequenceE_ReportingInformation_35B_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceE_ReportingInformation_35B_Type_Pattern', MT300_SequenceE_ReportingInformation_35B_Type_Pattern)
_module_typeBindings.MT300_SequenceE_ReportingInformation_35B_Type_Pattern = MT300_SequenceE_ReportingInformation_35B_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_17H_Type_Pattern
class MT300_SequenceE_ReportingInformation_17H_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceE_ReportingInformation_17H_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1277, 1)
    _Documentation = None
MT300_SequenceE_ReportingInformation_17H_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceE_ReportingInformation_17H_Type_Pattern._CF_pattern.addPattern(pattern='((A|P|U))')
MT300_SequenceE_ReportingInformation_17H_Type_Pattern._InitializeFacetMap(MT300_SequenceE_ReportingInformation_17H_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceE_ReportingInformation_17H_Type_Pattern', MT300_SequenceE_ReportingInformation_17H_Type_Pattern)
_module_typeBindings.MT300_SequenceE_ReportingInformation_17H_Type_Pattern = MT300_SequenceE_ReportingInformation_17H_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_17P_Type_Pattern
class MT300_SequenceE_ReportingInformation_17P_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceE_ReportingInformation_17P_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1290, 1)
    _Documentation = None
MT300_SequenceE_ReportingInformation_17P_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceE_ReportingInformation_17P_Type_Pattern._CF_pattern.addPattern(pattern='((F|O|P|U))')
MT300_SequenceE_ReportingInformation_17P_Type_Pattern._InitializeFacetMap(MT300_SequenceE_ReportingInformation_17P_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceE_ReportingInformation_17P_Type_Pattern', MT300_SequenceE_ReportingInformation_17P_Type_Pattern)
_module_typeBindings.MT300_SequenceE_ReportingInformation_17P_Type_Pattern = MT300_SequenceE_ReportingInformation_17P_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_22V_Type_Pattern
class MT300_SequenceE_ReportingInformation_22V_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceE_ReportingInformation_22V_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1303, 1)
    _Documentation = None
MT300_SequenceE_ReportingInformation_22V_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceE_ReportingInformation_22V_Type_Pattern._CF_pattern.addPattern(pattern="(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35})")
MT300_SequenceE_ReportingInformation_22V_Type_Pattern._InitializeFacetMap(MT300_SequenceE_ReportingInformation_22V_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceE_ReportingInformation_22V_Type_Pattern', MT300_SequenceE_ReportingInformation_22V_Type_Pattern)
_module_typeBindings.MT300_SequenceE_ReportingInformation_22V_Type_Pattern = MT300_SequenceE_ReportingInformation_22V_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_98D_Type_Pattern
class MT300_SequenceE_ReportingInformation_98D_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceE_ReportingInformation_98D_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1316, 1)
    _Documentation = None
MT300_SequenceE_ReportingInformation_98D_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceE_ReportingInformation_98D_Type_Pattern._CF_pattern.addPattern(pattern='([0-9]{8}[0-9]{6}(,[0-9]{1,3})?(/(N)?[0-9]{2}([0-9]{2})?)?)')
MT300_SequenceE_ReportingInformation_98D_Type_Pattern._InitializeFacetMap(MT300_SequenceE_ReportingInformation_98D_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceE_ReportingInformation_98D_Type_Pattern', MT300_SequenceE_ReportingInformation_98D_Type_Pattern)
_module_typeBindings.MT300_SequenceE_ReportingInformation_98D_Type_Pattern = MT300_SequenceE_ReportingInformation_98D_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_17W_Type_Pattern
class MT300_SequenceE_ReportingInformation_17W_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceE_ReportingInformation_17W_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1329, 1)
    _Documentation = None
MT300_SequenceE_ReportingInformation_17W_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceE_ReportingInformation_17W_Type_Pattern._CF_pattern.addPattern(pattern='([0-9])')
MT300_SequenceE_ReportingInformation_17W_Type_Pattern._InitializeFacetMap(MT300_SequenceE_ReportingInformation_17W_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceE_ReportingInformation_17W_Type_Pattern', MT300_SequenceE_ReportingInformation_17W_Type_Pattern)
_module_typeBindings.MT300_SequenceE_ReportingInformation_17W_Type_Pattern = MT300_SequenceE_ReportingInformation_17W_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_22W_Type_Pattern
class MT300_SequenceE_ReportingInformation_22W_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceE_ReportingInformation_22W_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1342, 1)
    _Documentation = None
MT300_SequenceE_ReportingInformation_22W_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceE_ReportingInformation_22W_Type_Pattern._CF_pattern.addPattern(pattern="(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,42})")
MT300_SequenceE_ReportingInformation_22W_Type_Pattern._InitializeFacetMap(MT300_SequenceE_ReportingInformation_22W_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceE_ReportingInformation_22W_Type_Pattern', MT300_SequenceE_ReportingInformation_22W_Type_Pattern)
_module_typeBindings.MT300_SequenceE_ReportingInformation_22W_Type_Pattern = MT300_SequenceE_ReportingInformation_22W_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_17Y_Type_Pattern
class MT300_SequenceE_ReportingInformation_17Y_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceE_ReportingInformation_17Y_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1355, 1)
    _Documentation = None
MT300_SequenceE_ReportingInformation_17Y_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceE_ReportingInformation_17Y_Type_Pattern._CF_pattern.addPattern(pattern='((F|N))')
MT300_SequenceE_ReportingInformation_17Y_Type_Pattern._InitializeFacetMap(MT300_SequenceE_ReportingInformation_17Y_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceE_ReportingInformation_17Y_Type_Pattern', MT300_SequenceE_ReportingInformation_17Y_Type_Pattern)
_module_typeBindings.MT300_SequenceE_ReportingInformation_17Y_Type_Pattern = MT300_SequenceE_ReportingInformation_17Y_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_17Z_Type_Pattern
class MT300_SequenceE_ReportingInformation_17Z_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceE_ReportingInformation_17Z_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1368, 1)
    _Documentation = None
MT300_SequenceE_ReportingInformation_17Z_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceE_ReportingInformation_17Z_Type_Pattern._CF_pattern.addPattern(pattern='((N|Y))')
MT300_SequenceE_ReportingInformation_17Z_Type_Pattern._InitializeFacetMap(MT300_SequenceE_ReportingInformation_17Z_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceE_ReportingInformation_17Z_Type_Pattern', MT300_SequenceE_ReportingInformation_17Z_Type_Pattern)
_module_typeBindings.MT300_SequenceE_ReportingInformation_17Z_Type_Pattern = MT300_SequenceE_ReportingInformation_17Z_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_22Q_Type_Pattern
class MT300_SequenceE_ReportingInformation_22Q_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceE_ReportingInformation_22Q_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1381, 1)
    _Documentation = None
MT300_SequenceE_ReportingInformation_22Q_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceE_ReportingInformation_22Q_Type_Pattern._CF_pattern.addPattern(pattern="(([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,10})")
MT300_SequenceE_ReportingInformation_22Q_Type_Pattern._InitializeFacetMap(MT300_SequenceE_ReportingInformation_22Q_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceE_ReportingInformation_22Q_Type_Pattern', MT300_SequenceE_ReportingInformation_22Q_Type_Pattern)
_module_typeBindings.MT300_SequenceE_ReportingInformation_22Q_Type_Pattern = MT300_SequenceE_ReportingInformation_22Q_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_17L_Type_Pattern
class MT300_SequenceE_ReportingInformation_17L_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceE_ReportingInformation_17L_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1394, 1)
    _Documentation = None
MT300_SequenceE_ReportingInformation_17L_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceE_ReportingInformation_17L_Type_Pattern._CF_pattern.addPattern(pattern='((N|Y))')
MT300_SequenceE_ReportingInformation_17L_Type_Pattern._InitializeFacetMap(MT300_SequenceE_ReportingInformation_17L_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceE_ReportingInformation_17L_Type_Pattern', MT300_SequenceE_ReportingInformation_17L_Type_Pattern)
_module_typeBindings.MT300_SequenceE_ReportingInformation_17L_Type_Pattern = MT300_SequenceE_ReportingInformation_17L_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_17M_Type_Pattern
class MT300_SequenceE_ReportingInformation_17M_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceE_ReportingInformation_17M_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1407, 1)
    _Documentation = None
MT300_SequenceE_ReportingInformation_17M_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceE_ReportingInformation_17M_Type_Pattern._CF_pattern.addPattern(pattern='((A|C|F|I|L|O|R|U))')
MT300_SequenceE_ReportingInformation_17M_Type_Pattern._InitializeFacetMap(MT300_SequenceE_ReportingInformation_17M_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceE_ReportingInformation_17M_Type_Pattern', MT300_SequenceE_ReportingInformation_17M_Type_Pattern)
_module_typeBindings.MT300_SequenceE_ReportingInformation_17M_Type_Pattern = MT300_SequenceE_ReportingInformation_17M_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_17Q_Type_Pattern
class MT300_SequenceE_ReportingInformation_17Q_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceE_ReportingInformation_17Q_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1420, 1)
    _Documentation = None
MT300_SequenceE_ReportingInformation_17Q_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceE_ReportingInformation_17Q_Type_Pattern._CF_pattern.addPattern(pattern='((N|Y))')
MT300_SequenceE_ReportingInformation_17Q_Type_Pattern._InitializeFacetMap(MT300_SequenceE_ReportingInformation_17Q_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceE_ReportingInformation_17Q_Type_Pattern', MT300_SequenceE_ReportingInformation_17Q_Type_Pattern)
_module_typeBindings.MT300_SequenceE_ReportingInformation_17Q_Type_Pattern = MT300_SequenceE_ReportingInformation_17Q_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_17S_Type_Pattern
class MT300_SequenceE_ReportingInformation_17S_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceE_ReportingInformation_17S_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1433, 1)
    _Documentation = None
MT300_SequenceE_ReportingInformation_17S_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceE_ReportingInformation_17S_Type_Pattern._CF_pattern.addPattern(pattern='((N|Y))')
MT300_SequenceE_ReportingInformation_17S_Type_Pattern._InitializeFacetMap(MT300_SequenceE_ReportingInformation_17S_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceE_ReportingInformation_17S_Type_Pattern', MT300_SequenceE_ReportingInformation_17S_Type_Pattern)
_module_typeBindings.MT300_SequenceE_ReportingInformation_17S_Type_Pattern = MT300_SequenceE_ReportingInformation_17S_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_17X_Type_Pattern
class MT300_SequenceE_ReportingInformation_17X_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceE_ReportingInformation_17X_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1446, 1)
    _Documentation = None
MT300_SequenceE_ReportingInformation_17X_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceE_ReportingInformation_17X_Type_Pattern._CF_pattern.addPattern(pattern='((N|Y))')
MT300_SequenceE_ReportingInformation_17X_Type_Pattern._InitializeFacetMap(MT300_SequenceE_ReportingInformation_17X_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceE_ReportingInformation_17X_Type_Pattern', MT300_SequenceE_ReportingInformation_17X_Type_Pattern)
_module_typeBindings.MT300_SequenceE_ReportingInformation_17X_Type_Pattern = MT300_SequenceE_ReportingInformation_17X_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_98G_Type_Pattern
class MT300_SequenceE_ReportingInformation_98G_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceE_ReportingInformation_98G_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1459, 1)
    _Documentation = None
MT300_SequenceE_ReportingInformation_98G_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceE_ReportingInformation_98G_Type_Pattern._CF_pattern.addPattern(pattern='([0-9]{8}[0-9]{6}(,[0-9]{1,3})?(/(N)?[0-9]{2}([0-9]{2})?)?)')
MT300_SequenceE_ReportingInformation_98G_Type_Pattern._InitializeFacetMap(MT300_SequenceE_ReportingInformation_98G_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceE_ReportingInformation_98G_Type_Pattern', MT300_SequenceE_ReportingInformation_98G_Type_Pattern)
_module_typeBindings.MT300_SequenceE_ReportingInformation_98G_Type_Pattern = MT300_SequenceE_ReportingInformation_98G_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_98H_Type_Pattern
class MT300_SequenceE_ReportingInformation_98H_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceE_ReportingInformation_98H_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1472, 1)
    _Documentation = None
MT300_SequenceE_ReportingInformation_98H_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceE_ReportingInformation_98H_Type_Pattern._CF_pattern.addPattern(pattern='([0-9]{6}(,[0-9]{1,3})?(/(N)?[0-9]{2}([0-9]{2})?)?)')
MT300_SequenceE_ReportingInformation_98H_Type_Pattern._InitializeFacetMap(MT300_SequenceE_ReportingInformation_98H_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceE_ReportingInformation_98H_Type_Pattern', MT300_SequenceE_ReportingInformation_98H_Type_Pattern)
_module_typeBindings.MT300_SequenceE_ReportingInformation_98H_Type_Pattern = MT300_SequenceE_ReportingInformation_98H_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_34C_Type_Pattern
class MT300_SequenceE_ReportingInformation_34C_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceE_ReportingInformation_34C_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1485, 1)
    _Documentation = None
MT300_SequenceE_ReportingInformation_34C_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceE_ReportingInformation_34C_Type_Pattern._CF_pattern.addPattern(pattern='([A-Z0-9]{4}/(N)?(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})')
MT300_SequenceE_ReportingInformation_34C_Type_Pattern._InitializeFacetMap(MT300_SequenceE_ReportingInformation_34C_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceE_ReportingInformation_34C_Type_Pattern', MT300_SequenceE_ReportingInformation_34C_Type_Pattern)
_module_typeBindings.MT300_SequenceE_ReportingInformation_34C_Type_Pattern = MT300_SequenceE_ReportingInformation_34C_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_77A_Type_Pattern
class MT300_SequenceE_ReportingInformation_77A_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceE_ReportingInformation_77A_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1498, 1)
    _Documentation = None
MT300_SequenceE_ReportingInformation_77A_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceE_ReportingInformation_77A_Type_Pattern._CF_pattern.addPattern(pattern="((([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,35}\\n?){1,20})")
MT300_SequenceE_ReportingInformation_77A_Type_Pattern._InitializeFacetMap(MT300_SequenceE_ReportingInformation_77A_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceE_ReportingInformation_77A_Type_Pattern', MT300_SequenceE_ReportingInformation_77A_Type_Pattern)
_module_typeBindings.MT300_SequenceE_ReportingInformation_77A_Type_Pattern = MT300_SequenceE_ReportingInformation_77A_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceF_PostTradeEvents_21H_Type_Pattern
class MT300_SequenceF_PostTradeEvents_21H_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceF_PostTradeEvents_21H_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1511, 1)
    _Documentation = None
MT300_SequenceF_PostTradeEvents_21H_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceF_PostTradeEvents_21H_Type_Pattern._CF_pattern.addPattern(pattern="((EAMT|PEAM|PRUR|PRUW|ROLL|UNWD|UNWR)[^/]([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,16}[^/])")
MT300_SequenceF_PostTradeEvents_21H_Type_Pattern._InitializeFacetMap(MT300_SequenceF_PostTradeEvents_21H_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceF_PostTradeEvents_21H_Type_Pattern', MT300_SequenceF_PostTradeEvents_21H_Type_Pattern)
_module_typeBindings.MT300_SequenceF_PostTradeEvents_21H_Type_Pattern = MT300_SequenceF_PostTradeEvents_21H_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceF_PostTradeEvents_21F_Type_Pattern
class MT300_SequenceF_PostTradeEvents_21F_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceF_PostTradeEvents_21F_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1524, 1)
    _Documentation = None
MT300_SequenceF_PostTradeEvents_21F_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceF_PostTradeEvents_21F_Type_Pattern._CF_pattern.addPattern(pattern="([^/]([a-zA-Z0-9]|/|-|\\?|:|\\(|\\)|\\.|,|'|\\+|\\n|\\s){1,16}[^/])")
MT300_SequenceF_PostTradeEvents_21F_Type_Pattern._InitializeFacetMap(MT300_SequenceF_PostTradeEvents_21F_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceF_PostTradeEvents_21F_Type_Pattern', MT300_SequenceF_PostTradeEvents_21F_Type_Pattern)
_module_typeBindings.MT300_SequenceF_PostTradeEvents_21F_Type_Pattern = MT300_SequenceF_PostTradeEvents_21F_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceF_PostTradeEvents_30F_Type_Pattern
class MT300_SequenceF_PostTradeEvents_30F_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceF_PostTradeEvents_30F_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1537, 1)
    _Documentation = None
MT300_SequenceF_PostTradeEvents_30F_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceF_PostTradeEvents_30F_Type_Pattern._CF_pattern.addPattern(pattern='([0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01]))')
MT300_SequenceF_PostTradeEvents_30F_Type_Pattern._InitializeFacetMap(MT300_SequenceF_PostTradeEvents_30F_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceF_PostTradeEvents_30F_Type_Pattern', MT300_SequenceF_PostTradeEvents_30F_Type_Pattern)
_module_typeBindings.MT300_SequenceF_PostTradeEvents_30F_Type_Pattern = MT300_SequenceF_PostTradeEvents_30F_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceF_PostTradeEvents_32H_Type_Pattern
class MT300_SequenceF_PostTradeEvents_32H_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceF_PostTradeEvents_32H_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1550, 1)
    _Documentation = None
MT300_SequenceF_PostTradeEvents_32H_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceF_PostTradeEvents_32H_Type_Pattern._CF_pattern.addPattern(pattern='((N)?(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})')
MT300_SequenceF_PostTradeEvents_32H_Type_Pattern._InitializeFacetMap(MT300_SequenceF_PostTradeEvents_32H_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceF_PostTradeEvents_32H_Type_Pattern', MT300_SequenceF_PostTradeEvents_32H_Type_Pattern)
_module_typeBindings.MT300_SequenceF_PostTradeEvents_32H_Type_Pattern = MT300_SequenceF_PostTradeEvents_32H_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_SequenceF_PostTradeEvents_33E_Type_Pattern
class MT300_SequenceF_PostTradeEvents_33E_Type_Pattern (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceF_PostTradeEvents_33E_Type_Pattern')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1563, 1)
    _Documentation = None
MT300_SequenceF_PostTradeEvents_33E_Type_Pattern._CF_pattern = pyxb.binding.facets.CF_pattern()
MT300_SequenceF_PostTradeEvents_33E_Type_Pattern._CF_pattern.addPattern(pattern='((AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR|FJD|FKP|GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|USD|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW|ZWD)[0-9,(?0-9)]{1,15})')
MT300_SequenceF_PostTradeEvents_33E_Type_Pattern._InitializeFacetMap(MT300_SequenceF_PostTradeEvents_33E_Type_Pattern._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceF_PostTradeEvents_33E_Type_Pattern', MT300_SequenceF_PostTradeEvents_33E_Type_Pattern)
_module_typeBindings.MT300_SequenceF_PostTradeEvents_33E_Type_Pattern = MT300_SequenceF_PostTradeEvents_33E_Type_Pattern

# Atomic simple type: {http://www.w3schools.com}MT300_15A_Type
class MT300_15A_Type (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_15A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1576, 1)
    _Documentation = None
MT300_15A_Type._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'MT300_15A_Type', MT300_15A_Type)
_module_typeBindings.MT300_15A_Type = MT300_15A_Type

# Atomic simple type: {http://www.w3schools.com}MT300_15B_Type
class MT300_15B_Type (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_15B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1579, 1)
    _Documentation = None
MT300_15B_Type._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'MT300_15B_Type', MT300_15B_Type)
_module_typeBindings.MT300_15B_Type = MT300_15B_Type

# Atomic simple type: {http://www.w3schools.com}MT300_15C_Type
class MT300_15C_Type (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_15C_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1582, 1)
    _Documentation = None
MT300_15C_Type._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'MT300_15C_Type', MT300_15C_Type)
_module_typeBindings.MT300_15C_Type = MT300_15C_Type

# Atomic simple type: {http://www.w3schools.com}MT300_15D_Type
class MT300_15D_Type (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_15D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1585, 1)
    _Documentation = None
MT300_15D_Type._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'MT300_15D_Type', MT300_15D_Type)
_module_typeBindings.MT300_15D_Type = MT300_15D_Type

# Atomic simple type: {http://www.w3schools.com}MT300_15E_Type
class MT300_15E_Type (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_15E_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1588, 1)
    _Documentation = None
MT300_15E_Type._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'MT300_15E_Type', MT300_15E_Type)
_module_typeBindings.MT300_15E_Type = MT300_15E_Type

# Complex type {http://www.w3schools.com}MT300_SequenceA_GeneralInformation with content type ELEMENT_ONLY
class MT300_SequenceA_GeneralInformation (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceA_GeneralInformation with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceA_GeneralInformation')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1591, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}SendersReference uses Python identifier SendersReference
    __SendersReference = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SendersReference'), 'SendersReference', '__httpwww_w3schools_com_MT300_SequenceA_GeneralInformation_httpwww_w3schools_comSendersReference', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1593, 3), )

    
    SendersReference = property(__SendersReference.value, __SendersReference.set, None, None)

    
    # Element {http://www.w3schools.com}RelatedReference uses Python identifier RelatedReference
    __RelatedReference = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'RelatedReference'), 'RelatedReference', '__httpwww_w3schools_com_MT300_SequenceA_GeneralInformation_httpwww_w3schools_comRelatedReference', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1594, 3), )

    
    RelatedReference = property(__RelatedReference.value, __RelatedReference.set, None, None)

    
    # Element {http://www.w3schools.com}TypeOfOperation uses Python identifier TypeOfOperation
    __TypeOfOperation = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'TypeOfOperation'), 'TypeOfOperation', '__httpwww_w3schools_com_MT300_SequenceA_GeneralInformation_httpwww_w3schools_comTypeOfOperation', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1595, 3), )

    
    TypeOfOperation = property(__TypeOfOperation.value, __TypeOfOperation.set, None, None)

    
    # Element {http://www.w3schools.com}ScopeOfOperation uses Python identifier ScopeOfOperation
    __ScopeOfOperation = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ScopeOfOperation'), 'ScopeOfOperation', '__httpwww_w3schools_com_MT300_SequenceA_GeneralInformation_httpwww_w3schools_comScopeOfOperation', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1596, 3), )

    
    ScopeOfOperation = property(__ScopeOfOperation.value, __ScopeOfOperation.set, None, None)

    
    # Element {http://www.w3schools.com}CommonReference uses Python identifier CommonReference
    __CommonReference = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'CommonReference'), 'CommonReference', '__httpwww_w3schools_com_MT300_SequenceA_GeneralInformation_httpwww_w3schools_comCommonReference', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1597, 3), )

    
    CommonReference = property(__CommonReference.value, __CommonReference.set, None, None)

    
    # Element {http://www.w3schools.com}BlockTradeIndicator uses Python identifier BlockTradeIndicator
    __BlockTradeIndicator = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'BlockTradeIndicator'), 'BlockTradeIndicator', '__httpwww_w3schools_com_MT300_SequenceA_GeneralInformation_httpwww_w3schools_comBlockTradeIndicator', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1598, 3), )

    
    BlockTradeIndicator = property(__BlockTradeIndicator.value, __BlockTradeIndicator.set, None, None)

    
    # Element {http://www.w3schools.com}SplitSettlementIndicator uses Python identifier SplitSettlementIndicator
    __SplitSettlementIndicator = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SplitSettlementIndicator'), 'SplitSettlementIndicator', '__httpwww_w3schools_com_MT300_SequenceA_GeneralInformation_httpwww_w3schools_comSplitSettlementIndicator', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1599, 3), )

    
    SplitSettlementIndicator = property(__SplitSettlementIndicator.value, __SplitSettlementIndicator.set, None, None)

    
    # Element {http://www.w3schools.com}PaymentVersusPaymentSettlementIndicator uses Python identifier PaymentVersusPaymentSettlementIndicator
    __PaymentVersusPaymentSettlementIndicator = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PaymentVersusPaymentSettlementIndicator'), 'PaymentVersusPaymentSettlementIndicator', '__httpwww_w3schools_com_MT300_SequenceA_GeneralInformation_httpwww_w3schools_comPaymentVersusPaymentSettlementIndicator', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1600, 3), )

    
    PaymentVersusPaymentSettlementIndicator = property(__PaymentVersusPaymentSettlementIndicator.value, __PaymentVersusPaymentSettlementIndicator.set, None, None)

    
    # Element {http://www.w3schools.com}PartyA_A uses Python identifier PartyA_A
    __PartyA_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PartyA_A'), 'PartyA_A', '__httpwww_w3schools_com_MT300_SequenceA_GeneralInformation_httpwww_w3schools_comPartyA_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1602, 4), )

    
    PartyA_A = property(__PartyA_A.value, __PartyA_A.set, None, None)

    
    # Element {http://www.w3schools.com}PartyA_J uses Python identifier PartyA_J
    __PartyA_J = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PartyA_J'), 'PartyA_J', '__httpwww_w3schools_com_MT300_SequenceA_GeneralInformation_httpwww_w3schools_comPartyA_J', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1603, 4), )

    
    PartyA_J = property(__PartyA_J.value, __PartyA_J.set, None, None)

    
    # Element {http://www.w3schools.com}PartyB_A uses Python identifier PartyB_A
    __PartyB_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PartyB_A'), 'PartyB_A', '__httpwww_w3schools_com_MT300_SequenceA_GeneralInformation_httpwww_w3schools_comPartyB_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1606, 4), )

    
    PartyB_A = property(__PartyB_A.value, __PartyB_A.set, None, None)

    
    # Element {http://www.w3schools.com}PartyB_J uses Python identifier PartyB_J
    __PartyB_J = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PartyB_J'), 'PartyB_J', '__httpwww_w3schools_com_MT300_SequenceA_GeneralInformation_httpwww_w3schools_comPartyB_J', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1607, 4), )

    
    PartyB_J = property(__PartyB_J.value, __PartyB_J.set, None, None)

    
    # Element {http://www.w3schools.com}FundOrBeneficiaryCustomer_A uses Python identifier FundOrBeneficiaryCustomer_A
    __FundOrBeneficiaryCustomer_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'FundOrBeneficiaryCustomer_A'), 'FundOrBeneficiaryCustomer_A', '__httpwww_w3schools_com_MT300_SequenceA_GeneralInformation_httpwww_w3schools_comFundOrBeneficiaryCustomer_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1610, 4), )

    
    FundOrBeneficiaryCustomer_A = property(__FundOrBeneficiaryCustomer_A.value, __FundOrBeneficiaryCustomer_A.set, None, None)

    
    # Element {http://www.w3schools.com}FundOrBeneficiaryCustomer_J uses Python identifier FundOrBeneficiaryCustomer_J
    __FundOrBeneficiaryCustomer_J = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'FundOrBeneficiaryCustomer_J'), 'FundOrBeneficiaryCustomer_J', '__httpwww_w3schools_com_MT300_SequenceA_GeneralInformation_httpwww_w3schools_comFundOrBeneficiaryCustomer_J', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1611, 4), )

    
    FundOrBeneficiaryCustomer_J = property(__FundOrBeneficiaryCustomer_J.value, __FundOrBeneficiaryCustomer_J.set, None, None)

    
    # Element {http://www.w3schools.com}TypeDateVersionOfAgreement uses Python identifier TypeDateVersionOfAgreement
    __TypeDateVersionOfAgreement = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'TypeDateVersionOfAgreement'), 'TypeDateVersionOfAgreement', '__httpwww_w3schools_com_MT300_SequenceA_GeneralInformation_httpwww_w3schools_comTypeDateVersionOfAgreement', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1613, 3), )

    
    TypeDateVersionOfAgreement = property(__TypeDateVersionOfAgreement.value, __TypeDateVersionOfAgreement.set, None, None)

    
    # Element {http://www.w3schools.com}TermsAndConditions uses Python identifier TermsAndConditions
    __TermsAndConditions = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'TermsAndConditions'), 'TermsAndConditions', '__httpwww_w3schools_com_MT300_SequenceA_GeneralInformation_httpwww_w3schools_comTermsAndConditions', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1614, 3), )

    
    TermsAndConditions = property(__TermsAndConditions.value, __TermsAndConditions.set, None, None)

    
    # Element {http://www.w3schools.com}YearOfDefinitions uses Python identifier YearOfDefinitions
    __YearOfDefinitions = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'YearOfDefinitions'), 'YearOfDefinitions', '__httpwww_w3schools_com_MT300_SequenceA_GeneralInformation_httpwww_w3schools_comYearOfDefinitions', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1615, 3), )

    
    YearOfDefinitions = property(__YearOfDefinitions.value, __YearOfDefinitions.set, None, None)

    
    # Element {http://www.w3schools.com}Non-DeliverableIndicator uses Python identifier Non_DeliverableIndicator
    __Non_DeliverableIndicator = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Non-DeliverableIndicator'), 'Non_DeliverableIndicator', '__httpwww_w3schools_com_MT300_SequenceA_GeneralInformation_httpwww_w3schools_comNon_DeliverableIndicator', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1616, 3), )

    
    Non_DeliverableIndicator = property(__Non_DeliverableIndicator.value, __Non_DeliverableIndicator.set, None, None)

    
    # Element {http://www.w3schools.com}NDFOpenIndicator uses Python identifier NDFOpenIndicator
    __NDFOpenIndicator = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'NDFOpenIndicator'), 'NDFOpenIndicator', '__httpwww_w3schools_com_MT300_SequenceA_GeneralInformation_httpwww_w3schools_comNDFOpenIndicator', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1617, 3), )

    
    NDFOpenIndicator = property(__NDFOpenIndicator.value, __NDFOpenIndicator.set, None, None)

    
    # Element {http://www.w3schools.com}SettlementCurrency uses Python identifier SettlementCurrency
    __SettlementCurrency = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SettlementCurrency'), 'SettlementCurrency', '__httpwww_w3schools_com_MT300_SequenceA_GeneralInformation_httpwww_w3schools_comSettlementCurrency', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1618, 3), )

    
    SettlementCurrency = property(__SettlementCurrency.value, __SettlementCurrency.set, None, None)

    
    # Element {http://www.w3schools.com}ValuationDate uses Python identifier ValuationDate
    __ValuationDate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ValuationDate'), 'ValuationDate', '__httpwww_w3schools_com_MT300_SequenceA_GeneralInformation_httpwww_w3schools_comValuationDate', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1619, 3), )

    
    ValuationDate = property(__ValuationDate.value, __ValuationDate.set, None, None)

    
    # Element {http://www.w3schools.com}SettlementRateSource uses Python identifier SettlementRateSource
    __SettlementRateSource = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SettlementRateSource'), 'SettlementRateSource', '__httpwww_w3schools_com_MT300_SequenceA_GeneralInformation_httpwww_w3schools_comSettlementRateSource', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1620, 3), )

    
    SettlementRateSource = property(__SettlementRateSource.value, __SettlementRateSource.set, None, None)

    
    # Element {http://www.w3schools.com}ReferenceToOpeningConfirmation uses Python identifier ReferenceToOpeningConfirmation
    __ReferenceToOpeningConfirmation = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ReferenceToOpeningConfirmation'), 'ReferenceToOpeningConfirmation', '__httpwww_w3schools_com_MT300_SequenceA_GeneralInformation_httpwww_w3schools_comReferenceToOpeningConfirmation', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1621, 3), )

    
    ReferenceToOpeningConfirmation = property(__ReferenceToOpeningConfirmation.value, __ReferenceToOpeningConfirmation.set, None, None)

    
    # Element {http://www.w3schools.com}ClearingOrSettlementSession uses Python identifier ClearingOrSettlementSession
    __ClearingOrSettlementSession = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ClearingOrSettlementSession'), 'ClearingOrSettlementSession', '__httpwww_w3schools_com_MT300_SequenceA_GeneralInformation_httpwww_w3schools_comClearingOrSettlementSession', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1622, 3), )

    
    ClearingOrSettlementSession = property(__ClearingOrSettlementSession.value, __ClearingOrSettlementSession.set, None, None)

    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceA_GeneralInformation_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='15A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1624, 2)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1624, 2)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceA_GeneralInformation_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1625, 2)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1625, 2)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    
    # Attribute formatTag uses Python identifier formatTag
    __formatTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'formatTag'), 'formatTag', '__httpwww_w3schools_com_MT300_SequenceA_GeneralInformation_formatTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='False')
    __formatTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1626, 2)
    __formatTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1626, 2)
    
    formatTag = property(__formatTag.value, __formatTag.set, None, None)

    _ElementMap.update({
        __SendersReference.name() : __SendersReference,
        __RelatedReference.name() : __RelatedReference,
        __TypeOfOperation.name() : __TypeOfOperation,
        __ScopeOfOperation.name() : __ScopeOfOperation,
        __CommonReference.name() : __CommonReference,
        __BlockTradeIndicator.name() : __BlockTradeIndicator,
        __SplitSettlementIndicator.name() : __SplitSettlementIndicator,
        __PaymentVersusPaymentSettlementIndicator.name() : __PaymentVersusPaymentSettlementIndicator,
        __PartyA_A.name() : __PartyA_A,
        __PartyA_J.name() : __PartyA_J,
        __PartyB_A.name() : __PartyB_A,
        __PartyB_J.name() : __PartyB_J,
        __FundOrBeneficiaryCustomer_A.name() : __FundOrBeneficiaryCustomer_A,
        __FundOrBeneficiaryCustomer_J.name() : __FundOrBeneficiaryCustomer_J,
        __TypeDateVersionOfAgreement.name() : __TypeDateVersionOfAgreement,
        __TermsAndConditions.name() : __TermsAndConditions,
        __YearOfDefinitions.name() : __YearOfDefinitions,
        __Non_DeliverableIndicator.name() : __Non_DeliverableIndicator,
        __NDFOpenIndicator.name() : __NDFOpenIndicator,
        __SettlementCurrency.name() : __SettlementCurrency,
        __ValuationDate.name() : __ValuationDate,
        __SettlementRateSource.name() : __SettlementRateSource,
        __ReferenceToOpeningConfirmation.name() : __ReferenceToOpeningConfirmation,
        __ClearingOrSettlementSession.name() : __ClearingOrSettlementSession
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory,
        __formatTag.name() : __formatTag
    })
_module_typeBindings.MT300_SequenceA_GeneralInformation = MT300_SequenceA_GeneralInformation
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceA_GeneralInformation', MT300_SequenceA_GeneralInformation)


# Complex type {http://www.w3schools.com}MT300_SequenceB_TransactionDetails with content type ELEMENT_ONLY
class MT300_SequenceB_TransactionDetails (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceB_TransactionDetails with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceB_TransactionDetails')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1628, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}TradeDate uses Python identifier TradeDate
    __TradeDate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'TradeDate'), 'TradeDate', '__httpwww_w3schools_com_MT300_SequenceB_TransactionDetails_httpwww_w3schools_comTradeDate', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1630, 3), )

    
    TradeDate = property(__TradeDate.value, __TradeDate.set, None, None)

    
    # Element {http://www.w3schools.com}ValueDate uses Python identifier ValueDate
    __ValueDate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ValueDate'), 'ValueDate', '__httpwww_w3schools_com_MT300_SequenceB_TransactionDetails_httpwww_w3schools_comValueDate', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1631, 3), )

    
    ValueDate = property(__ValueDate.value, __ValueDate.set, None, None)

    
    # Element {http://www.w3schools.com}ExchangeRate uses Python identifier ExchangeRate
    __ExchangeRate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ExchangeRate'), 'ExchangeRate', '__httpwww_w3schools_com_MT300_SequenceB_TransactionDetails_httpwww_w3schools_comExchangeRate', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1632, 3), )

    
    ExchangeRate = property(__ExchangeRate.value, __ExchangeRate.set, None, None)

    
    # Element {http://www.w3schools.com}PaymentClearingCentre uses Python identifier PaymentClearingCentre
    __PaymentClearingCentre = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PaymentClearingCentre'), 'PaymentClearingCentre', '__httpwww_w3schools_com_MT300_SequenceB_TransactionDetails_httpwww_w3schools_comPaymentClearingCentre', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1633, 3), )

    
    PaymentClearingCentre = property(__PaymentClearingCentre.value, __PaymentClearingCentre.set, None, None)

    
    # Element {http://www.w3schools.com}SubSequenceB1_AmountBought uses Python identifier SubSequenceB1_AmountBought
    __SubSequenceB1_AmountBought = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SubSequenceB1_AmountBought'), 'SubSequenceB1_AmountBought', '__httpwww_w3schools_com_MT300_SequenceB_TransactionDetails_httpwww_w3schools_comSubSequenceB1_AmountBought', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1634, 3), )

    
    SubSequenceB1_AmountBought = property(__SubSequenceB1_AmountBought.value, __SubSequenceB1_AmountBought.set, None, None)

    
    # Element {http://www.w3schools.com}SubSequenceB2_AmountSold uses Python identifier SubSequenceB2_AmountSold
    __SubSequenceB2_AmountSold = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SubSequenceB2_AmountSold'), 'SubSequenceB2_AmountSold', '__httpwww_w3schools_com_MT300_SequenceB_TransactionDetails_httpwww_w3schools_comSubSequenceB2_AmountSold', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1635, 3), )

    
    SubSequenceB2_AmountSold = property(__SubSequenceB2_AmountSold.value, __SubSequenceB2_AmountSold.set, None, None)

    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceB_TransactionDetails_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='15B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1637, 2)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1637, 2)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceB_TransactionDetails_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1638, 2)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1638, 2)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    
    # Attribute formatTag uses Python identifier formatTag
    __formatTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'formatTag'), 'formatTag', '__httpwww_w3schools_com_MT300_SequenceB_TransactionDetails_formatTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='False')
    __formatTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1639, 2)
    __formatTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1639, 2)
    
    formatTag = property(__formatTag.value, __formatTag.set, None, None)

    _ElementMap.update({
        __TradeDate.name() : __TradeDate,
        __ValueDate.name() : __ValueDate,
        __ExchangeRate.name() : __ExchangeRate,
        __PaymentClearingCentre.name() : __PaymentClearingCentre,
        __SubSequenceB1_AmountBought.name() : __SubSequenceB1_AmountBought,
        __SubSequenceB2_AmountSold.name() : __SubSequenceB2_AmountSold
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory,
        __formatTag.name() : __formatTag
    })
_module_typeBindings.MT300_SequenceB_TransactionDetails = MT300_SequenceB_TransactionDetails
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceB_TransactionDetails', MT300_SequenceB_TransactionDetails)


# Complex type {http://www.w3schools.com}MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought with content type ELEMENT_ONLY
class MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1641, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}CurrencyAmount uses Python identifier CurrencyAmount
    __CurrencyAmount = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'CurrencyAmount'), 'CurrencyAmount', '__httpwww_w3schools_com_MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_httpwww_w3schools_comCurrencyAmount', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1643, 3), )

    
    CurrencyAmount = property(__CurrencyAmount.value, __CurrencyAmount.set, None, None)

    
    # Element {http://www.w3schools.com}DeliveryAgent_A uses Python identifier DeliveryAgent_A
    __DeliveryAgent_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_A'), 'DeliveryAgent_A', '__httpwww_w3schools_com_MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_httpwww_w3schools_comDeliveryAgent_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1645, 4), )

    
    DeliveryAgent_A = property(__DeliveryAgent_A.value, __DeliveryAgent_A.set, None, None)

    
    # Element {http://www.w3schools.com}DeliveryAgent_J uses Python identifier DeliveryAgent_J
    __DeliveryAgent_J = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_J'), 'DeliveryAgent_J', '__httpwww_w3schools_com_MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_httpwww_w3schools_comDeliveryAgent_J', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1646, 4), )

    
    DeliveryAgent_J = property(__DeliveryAgent_J.value, __DeliveryAgent_J.set, None, None)

    
    # Element {http://www.w3schools.com}Intermediary_A uses Python identifier Intermediary_A
    __Intermediary_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_A'), 'Intermediary_A', '__httpwww_w3schools_com_MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_httpwww_w3schools_comIntermediary_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1649, 4), )

    
    Intermediary_A = property(__Intermediary_A.value, __Intermediary_A.set, None, None)

    
    # Element {http://www.w3schools.com}Intermediary_J uses Python identifier Intermediary_J
    __Intermediary_J = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_J'), 'Intermediary_J', '__httpwww_w3schools_com_MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_httpwww_w3schools_comIntermediary_J', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1650, 4), )

    
    Intermediary_J = property(__Intermediary_J.value, __Intermediary_J.set, None, None)

    
    # Element {http://www.w3schools.com}ReceivingAgent_A uses Python identifier ReceivingAgent_A
    __ReceivingAgent_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_A'), 'ReceivingAgent_A', '__httpwww_w3schools_com_MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_httpwww_w3schools_comReceivingAgent_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1653, 4), )

    
    ReceivingAgent_A = property(__ReceivingAgent_A.value, __ReceivingAgent_A.set, None, None)

    
    # Element {http://www.w3schools.com}ReceivingAgent_J uses Python identifier ReceivingAgent_J
    __ReceivingAgent_J = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_J'), 'ReceivingAgent_J', '__httpwww_w3schools_com_MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_httpwww_w3schools_comReceivingAgent_J', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1654, 4), )

    
    ReceivingAgent_J = property(__ReceivingAgent_J.value, __ReceivingAgent_J.set, None, None)

    _ElementMap.update({
        __CurrencyAmount.name() : __CurrencyAmount,
        __DeliveryAgent_A.name() : __DeliveryAgent_A,
        __DeliveryAgent_J.name() : __DeliveryAgent_J,
        __Intermediary_A.name() : __Intermediary_A,
        __Intermediary_J.name() : __Intermediary_J,
        __ReceivingAgent_A.name() : __ReceivingAgent_A,
        __ReceivingAgent_J.name() : __ReceivingAgent_J
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought = MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought', MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought)


# Complex type {http://www.w3schools.com}MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold with content type ELEMENT_ONLY
class MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1658, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}CurrencyAmount uses Python identifier CurrencyAmount
    __CurrencyAmount = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'CurrencyAmount'), 'CurrencyAmount', '__httpwww_w3schools_com_MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_httpwww_w3schools_comCurrencyAmount', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1660, 3), )

    
    CurrencyAmount = property(__CurrencyAmount.value, __CurrencyAmount.set, None, None)

    
    # Element {http://www.w3schools.com}DeliveryAgent_A uses Python identifier DeliveryAgent_A
    __DeliveryAgent_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_A'), 'DeliveryAgent_A', '__httpwww_w3schools_com_MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_httpwww_w3schools_comDeliveryAgent_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1662, 4), )

    
    DeliveryAgent_A = property(__DeliveryAgent_A.value, __DeliveryAgent_A.set, None, None)

    
    # Element {http://www.w3schools.com}DeliveryAgent_J uses Python identifier DeliveryAgent_J
    __DeliveryAgent_J = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_J'), 'DeliveryAgent_J', '__httpwww_w3schools_com_MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_httpwww_w3schools_comDeliveryAgent_J', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1663, 4), )

    
    DeliveryAgent_J = property(__DeliveryAgent_J.value, __DeliveryAgent_J.set, None, None)

    
    # Element {http://www.w3schools.com}Intermediary_A uses Python identifier Intermediary_A
    __Intermediary_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_A'), 'Intermediary_A', '__httpwww_w3schools_com_MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_httpwww_w3schools_comIntermediary_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1666, 4), )

    
    Intermediary_A = property(__Intermediary_A.value, __Intermediary_A.set, None, None)

    
    # Element {http://www.w3schools.com}Intermediary_J uses Python identifier Intermediary_J
    __Intermediary_J = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_J'), 'Intermediary_J', '__httpwww_w3schools_com_MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_httpwww_w3schools_comIntermediary_J', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1667, 4), )

    
    Intermediary_J = property(__Intermediary_J.value, __Intermediary_J.set, None, None)

    
    # Element {http://www.w3schools.com}ReceivingAgent_A uses Python identifier ReceivingAgent_A
    __ReceivingAgent_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_A'), 'ReceivingAgent_A', '__httpwww_w3schools_com_MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_httpwww_w3schools_comReceivingAgent_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1670, 4), )

    
    ReceivingAgent_A = property(__ReceivingAgent_A.value, __ReceivingAgent_A.set, None, None)

    
    # Element {http://www.w3schools.com}ReceivingAgent_J uses Python identifier ReceivingAgent_J
    __ReceivingAgent_J = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_J'), 'ReceivingAgent_J', '__httpwww_w3schools_com_MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_httpwww_w3schools_comReceivingAgent_J', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1671, 4), )

    
    ReceivingAgent_J = property(__ReceivingAgent_J.value, __ReceivingAgent_J.set, None, None)

    
    # Element {http://www.w3schools.com}BeneficiaryInstitution_A uses Python identifier BeneficiaryInstitution_A
    __BeneficiaryInstitution_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_A'), 'BeneficiaryInstitution_A', '__httpwww_w3schools_com_MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_httpwww_w3schools_comBeneficiaryInstitution_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1674, 4), )

    
    BeneficiaryInstitution_A = property(__BeneficiaryInstitution_A.value, __BeneficiaryInstitution_A.set, None, None)

    
    # Element {http://www.w3schools.com}BeneficiaryInstitution_J uses Python identifier BeneficiaryInstitution_J
    __BeneficiaryInstitution_J = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_J'), 'BeneficiaryInstitution_J', '__httpwww_w3schools_com_MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_httpwww_w3schools_comBeneficiaryInstitution_J', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1675, 4), )

    
    BeneficiaryInstitution_J = property(__BeneficiaryInstitution_J.value, __BeneficiaryInstitution_J.set, None, None)

    _ElementMap.update({
        __CurrencyAmount.name() : __CurrencyAmount,
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
_module_typeBindings.MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold = MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold', MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold)


# Complex type {http://www.w3schools.com}MT300_SequenceC_OptionalGeneralInformation with content type ELEMENT_ONLY
class MT300_SequenceC_OptionalGeneralInformation (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceC_OptionalGeneralInformation with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceC_OptionalGeneralInformation')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1679, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}ContactInformation uses Python identifier ContactInformation
    __ContactInformation = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ContactInformation'), 'ContactInformation', '__httpwww_w3schools_com_MT300_SequenceC_OptionalGeneralInformation_httpwww_w3schools_comContactInformation', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1681, 3), )

    
    ContactInformation = property(__ContactInformation.value, __ContactInformation.set, None, None)

    
    # Element {http://www.w3schools.com}DealingMethod uses Python identifier DealingMethod
    __DealingMethod = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'DealingMethod'), 'DealingMethod', '__httpwww_w3schools_com_MT300_SequenceC_OptionalGeneralInformation_httpwww_w3schools_comDealingMethod', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1682, 3), )

    
    DealingMethod = property(__DealingMethod.value, __DealingMethod.set, None, None)

    
    # Element {http://www.w3schools.com}DealingBranchPartyA_A uses Python identifier DealingBranchPartyA_A
    __DealingBranchPartyA_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'DealingBranchPartyA_A'), 'DealingBranchPartyA_A', '__httpwww_w3schools_com_MT300_SequenceC_OptionalGeneralInformation_httpwww_w3schools_comDealingBranchPartyA_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1684, 4), )

    
    DealingBranchPartyA_A = property(__DealingBranchPartyA_A.value, __DealingBranchPartyA_A.set, None, None)

    
    # Element {http://www.w3schools.com}DealingBranchPartyA_B uses Python identifier DealingBranchPartyA_B
    __DealingBranchPartyA_B = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'DealingBranchPartyA_B'), 'DealingBranchPartyA_B', '__httpwww_w3schools_com_MT300_SequenceC_OptionalGeneralInformation_httpwww_w3schools_comDealingBranchPartyA_B', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1685, 4), )

    
    DealingBranchPartyA_B = property(__DealingBranchPartyA_B.value, __DealingBranchPartyA_B.set, None, None)

    
    # Element {http://www.w3schools.com}DealingBranchPartyA_D uses Python identifier DealingBranchPartyA_D
    __DealingBranchPartyA_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'DealingBranchPartyA_D'), 'DealingBranchPartyA_D', '__httpwww_w3schools_com_MT300_SequenceC_OptionalGeneralInformation_httpwww_w3schools_comDealingBranchPartyA_D', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1686, 4), )

    
    DealingBranchPartyA_D = property(__DealingBranchPartyA_D.value, __DealingBranchPartyA_D.set, None, None)

    
    # Element {http://www.w3schools.com}DealingBranchPartyA_J uses Python identifier DealingBranchPartyA_J
    __DealingBranchPartyA_J = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'DealingBranchPartyA_J'), 'DealingBranchPartyA_J', '__httpwww_w3schools_com_MT300_SequenceC_OptionalGeneralInformation_httpwww_w3schools_comDealingBranchPartyA_J', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1687, 4), )

    
    DealingBranchPartyA_J = property(__DealingBranchPartyA_J.value, __DealingBranchPartyA_J.set, None, None)

    
    # Element {http://www.w3schools.com}DealingBranchPartyB_A uses Python identifier DealingBranchPartyB_A
    __DealingBranchPartyB_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'DealingBranchPartyB_A'), 'DealingBranchPartyB_A', '__httpwww_w3schools_com_MT300_SequenceC_OptionalGeneralInformation_httpwww_w3schools_comDealingBranchPartyB_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1690, 4), )

    
    DealingBranchPartyB_A = property(__DealingBranchPartyB_A.value, __DealingBranchPartyB_A.set, None, None)

    
    # Element {http://www.w3schools.com}DealingBranchPartyB_B uses Python identifier DealingBranchPartyB_B
    __DealingBranchPartyB_B = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'DealingBranchPartyB_B'), 'DealingBranchPartyB_B', '__httpwww_w3schools_com_MT300_SequenceC_OptionalGeneralInformation_httpwww_w3schools_comDealingBranchPartyB_B', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1691, 4), )

    
    DealingBranchPartyB_B = property(__DealingBranchPartyB_B.value, __DealingBranchPartyB_B.set, None, None)

    
    # Element {http://www.w3schools.com}DealingBranchPartyB_D uses Python identifier DealingBranchPartyB_D
    __DealingBranchPartyB_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'DealingBranchPartyB_D'), 'DealingBranchPartyB_D', '__httpwww_w3schools_com_MT300_SequenceC_OptionalGeneralInformation_httpwww_w3schools_comDealingBranchPartyB_D', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1692, 4), )

    
    DealingBranchPartyB_D = property(__DealingBranchPartyB_D.value, __DealingBranchPartyB_D.set, None, None)

    
    # Element {http://www.w3schools.com}DealingBranchPartyB_J uses Python identifier DealingBranchPartyB_J
    __DealingBranchPartyB_J = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'DealingBranchPartyB_J'), 'DealingBranchPartyB_J', '__httpwww_w3schools_com_MT300_SequenceC_OptionalGeneralInformation_httpwww_w3schools_comDealingBranchPartyB_J', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1693, 4), )

    
    DealingBranchPartyB_J = property(__DealingBranchPartyB_J.value, __DealingBranchPartyB_J.set, None, None)

    
    # Element {http://www.w3schools.com}BrokerIdentification_A uses Python identifier BrokerIdentification_A
    __BrokerIdentification_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'BrokerIdentification_A'), 'BrokerIdentification_A', '__httpwww_w3schools_com_MT300_SequenceC_OptionalGeneralInformation_httpwww_w3schools_comBrokerIdentification_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1696, 4), )

    
    BrokerIdentification_A = property(__BrokerIdentification_A.value, __BrokerIdentification_A.set, None, None)

    
    # Element {http://www.w3schools.com}BrokerIdentification_D uses Python identifier BrokerIdentification_D
    __BrokerIdentification_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'BrokerIdentification_D'), 'BrokerIdentification_D', '__httpwww_w3schools_com_MT300_SequenceC_OptionalGeneralInformation_httpwww_w3schools_comBrokerIdentification_D', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1697, 4), )

    
    BrokerIdentification_D = property(__BrokerIdentification_D.value, __BrokerIdentification_D.set, None, None)

    
    # Element {http://www.w3schools.com}BrokerIdentification_J uses Python identifier BrokerIdentification_J
    __BrokerIdentification_J = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'BrokerIdentification_J'), 'BrokerIdentification_J', '__httpwww_w3schools_com_MT300_SequenceC_OptionalGeneralInformation_httpwww_w3schools_comBrokerIdentification_J', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1698, 4), )

    
    BrokerIdentification_J = property(__BrokerIdentification_J.value, __BrokerIdentification_J.set, None, None)

    
    # Element {http://www.w3schools.com}BrokersCommission uses Python identifier BrokersCommission
    __BrokersCommission = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'BrokersCommission'), 'BrokersCommission', '__httpwww_w3schools_com_MT300_SequenceC_OptionalGeneralInformation_httpwww_w3schools_comBrokersCommission', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1700, 3), )

    
    BrokersCommission = property(__BrokersCommission.value, __BrokersCommission.set, None, None)

    
    # Element {http://www.w3schools.com}CounterpartysReference uses Python identifier CounterpartysReference
    __CounterpartysReference = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'CounterpartysReference'), 'CounterpartysReference', '__httpwww_w3schools_com_MT300_SequenceC_OptionalGeneralInformation_httpwww_w3schools_comCounterpartysReference', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1701, 3), )

    
    CounterpartysReference = property(__CounterpartysReference.value, __CounterpartysReference.set, None, None)

    
    # Element {http://www.w3schools.com}BrokersReference uses Python identifier BrokersReference
    __BrokersReference = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'BrokersReference'), 'BrokersReference', '__httpwww_w3schools_com_MT300_SequenceC_OptionalGeneralInformation_httpwww_w3schools_comBrokersReference', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1702, 3), )

    
    BrokersReference = property(__BrokersReference.value, __BrokersReference.set, None, None)

    
    # Element {http://www.w3schools.com}SenderToReceiverInformation uses Python identifier SenderToReceiverInformation
    __SenderToReceiverInformation = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SenderToReceiverInformation'), 'SenderToReceiverInformation', '__httpwww_w3schools_com_MT300_SequenceC_OptionalGeneralInformation_httpwww_w3schools_comSenderToReceiverInformation', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1703, 3), )

    
    SenderToReceiverInformation = property(__SenderToReceiverInformation.value, __SenderToReceiverInformation.set, None, None)

    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceC_OptionalGeneralInformation_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='15C')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1705, 2)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1705, 2)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceC_OptionalGeneralInformation_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1706, 2)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1706, 2)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    
    # Attribute formatTag uses Python identifier formatTag
    __formatTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'formatTag'), 'formatTag', '__httpwww_w3schools_com_MT300_SequenceC_OptionalGeneralInformation_formatTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='False')
    __formatTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1707, 2)
    __formatTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1707, 2)
    
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
        __SenderToReceiverInformation.name() : __SenderToReceiverInformation
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory,
        __formatTag.name() : __formatTag
    })
_module_typeBindings.MT300_SequenceC_OptionalGeneralInformation = MT300_SequenceC_OptionalGeneralInformation
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceC_OptionalGeneralInformation', MT300_SequenceC_OptionalGeneralInformation)


# Complex type {http://www.w3schools.com}MT300_SequenceD_SplitSettlementDetails with content type ELEMENT_ONLY
class MT300_SequenceD_SplitSettlementDetails (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceD_SplitSettlementDetails with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceD_SplitSettlementDetails')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1709, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}SettlementDetails uses Python identifier SettlementDetails
    __SettlementDetails = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SettlementDetails'), 'SettlementDetails', '__httpwww_w3schools_com_MT300_SequenceD_SplitSettlementDetails_httpwww_w3schools_comSettlementDetails', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1711, 3), )

    
    SettlementDetails = property(__SettlementDetails.value, __SettlementDetails.set, None, None)

    
    # Element {http://www.w3schools.com}NumberOfSettlements uses Python identifier NumberOfSettlements
    __NumberOfSettlements = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'NumberOfSettlements'), 'NumberOfSettlements', '__httpwww_w3schools_com_MT300_SequenceD_SplitSettlementDetails_httpwww_w3schools_comNumberOfSettlements', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1712, 3), )

    
    NumberOfSettlements = property(__NumberOfSettlements.value, __NumberOfSettlements.set, None, None)

    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceD_SplitSettlementDetails_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='15D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1714, 2)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1714, 2)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceD_SplitSettlementDetails_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1715, 2)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1715, 2)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    
    # Attribute formatTag uses Python identifier formatTag
    __formatTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'formatTag'), 'formatTag', '__httpwww_w3schools_com_MT300_SequenceD_SplitSettlementDetails_formatTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='False')
    __formatTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1716, 2)
    __formatTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1716, 2)
    
    formatTag = property(__formatTag.value, __formatTag.set, None, None)

    _ElementMap.update({
        __SettlementDetails.name() : __SettlementDetails,
        __NumberOfSettlements.name() : __NumberOfSettlements
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory,
        __formatTag.name() : __formatTag
    })
_module_typeBindings.MT300_SequenceD_SplitSettlementDetails = MT300_SequenceD_SplitSettlementDetails
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceD_SplitSettlementDetails', MT300_SequenceD_SplitSettlementDetails)


# Complex type {http://www.w3schools.com}MT300_SequenceD_SplitSettlementDetails_SettlementDetails with content type ELEMENT_ONLY
class MT300_SequenceD_SplitSettlementDetails_SettlementDetails (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceD_SplitSettlementDetails_SettlementDetails with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceD_SplitSettlementDetails_SettlementDetails')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1718, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}BuySellIndicator uses Python identifier BuySellIndicator
    __BuySellIndicator = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'BuySellIndicator'), 'BuySellIndicator', '__httpwww_w3schools_com_MT300_SequenceD_SplitSettlementDetails_SettlementDetails_httpwww_w3schools_comBuySellIndicator', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1720, 3), )

    
    BuySellIndicator = property(__BuySellIndicator.value, __BuySellIndicator.set, None, None)

    
    # Element {http://www.w3schools.com}CurrencyAmount uses Python identifier CurrencyAmount
    __CurrencyAmount = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'CurrencyAmount'), 'CurrencyAmount', '__httpwww_w3schools_com_MT300_SequenceD_SplitSettlementDetails_SettlementDetails_httpwww_w3schools_comCurrencyAmount', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1721, 3), )

    
    CurrencyAmount = property(__CurrencyAmount.value, __CurrencyAmount.set, None, None)

    
    # Element {http://www.w3schools.com}DeliveryAgent_A uses Python identifier DeliveryAgent_A
    __DeliveryAgent_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_A'), 'DeliveryAgent_A', '__httpwww_w3schools_com_MT300_SequenceD_SplitSettlementDetails_SettlementDetails_httpwww_w3schools_comDeliveryAgent_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1723, 4), )

    
    DeliveryAgent_A = property(__DeliveryAgent_A.value, __DeliveryAgent_A.set, None, None)

    
    # Element {http://www.w3schools.com}DeliveryAgent_D uses Python identifier DeliveryAgent_D
    __DeliveryAgent_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_D'), 'DeliveryAgent_D', '__httpwww_w3schools_com_MT300_SequenceD_SplitSettlementDetails_SettlementDetails_httpwww_w3schools_comDeliveryAgent_D', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1724, 4), )

    
    DeliveryAgent_D = property(__DeliveryAgent_D.value, __DeliveryAgent_D.set, None, None)

    
    # Element {http://www.w3schools.com}DeliveryAgent_J uses Python identifier DeliveryAgent_J
    __DeliveryAgent_J = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_J'), 'DeliveryAgent_J', '__httpwww_w3schools_com_MT300_SequenceD_SplitSettlementDetails_SettlementDetails_httpwww_w3schools_comDeliveryAgent_J', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1725, 4), )

    
    DeliveryAgent_J = property(__DeliveryAgent_J.value, __DeliveryAgent_J.set, None, None)

    
    # Element {http://www.w3schools.com}Intermediary_A uses Python identifier Intermediary_A
    __Intermediary_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_A'), 'Intermediary_A', '__httpwww_w3schools_com_MT300_SequenceD_SplitSettlementDetails_SettlementDetails_httpwww_w3schools_comIntermediary_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1728, 4), )

    
    Intermediary_A = property(__Intermediary_A.value, __Intermediary_A.set, None, None)

    
    # Element {http://www.w3schools.com}Intermediary_D uses Python identifier Intermediary_D
    __Intermediary_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_D'), 'Intermediary_D', '__httpwww_w3schools_com_MT300_SequenceD_SplitSettlementDetails_SettlementDetails_httpwww_w3schools_comIntermediary_D', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1729, 4), )

    
    Intermediary_D = property(__Intermediary_D.value, __Intermediary_D.set, None, None)

    
    # Element {http://www.w3schools.com}Intermediary_J uses Python identifier Intermediary_J
    __Intermediary_J = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_J'), 'Intermediary_J', '__httpwww_w3schools_com_MT300_SequenceD_SplitSettlementDetails_SettlementDetails_httpwww_w3schools_comIntermediary_J', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1730, 4), )

    
    Intermediary_J = property(__Intermediary_J.value, __Intermediary_J.set, None, None)

    
    # Element {http://www.w3schools.com}ReceivingAgent_A uses Python identifier ReceivingAgent_A
    __ReceivingAgent_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_A'), 'ReceivingAgent_A', '__httpwww_w3schools_com_MT300_SequenceD_SplitSettlementDetails_SettlementDetails_httpwww_w3schools_comReceivingAgent_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1733, 4), )

    
    ReceivingAgent_A = property(__ReceivingAgent_A.value, __ReceivingAgent_A.set, None, None)

    
    # Element {http://www.w3schools.com}ReceivingAgent_D uses Python identifier ReceivingAgent_D
    __ReceivingAgent_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_D'), 'ReceivingAgent_D', '__httpwww_w3schools_com_MT300_SequenceD_SplitSettlementDetails_SettlementDetails_httpwww_w3schools_comReceivingAgent_D', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1734, 4), )

    
    ReceivingAgent_D = property(__ReceivingAgent_D.value, __ReceivingAgent_D.set, None, None)

    
    # Element {http://www.w3schools.com}ReceivingAgent_J uses Python identifier ReceivingAgent_J
    __ReceivingAgent_J = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_J'), 'ReceivingAgent_J', '__httpwww_w3schools_com_MT300_SequenceD_SplitSettlementDetails_SettlementDetails_httpwww_w3schools_comReceivingAgent_J', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1735, 4), )

    
    ReceivingAgent_J = property(__ReceivingAgent_J.value, __ReceivingAgent_J.set, None, None)

    
    # Element {http://www.w3schools.com}BeneficiaryInstitution_A uses Python identifier BeneficiaryInstitution_A
    __BeneficiaryInstitution_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_A'), 'BeneficiaryInstitution_A', '__httpwww_w3schools_com_MT300_SequenceD_SplitSettlementDetails_SettlementDetails_httpwww_w3schools_comBeneficiaryInstitution_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1738, 4), )

    
    BeneficiaryInstitution_A = property(__BeneficiaryInstitution_A.value, __BeneficiaryInstitution_A.set, None, None)

    
    # Element {http://www.w3schools.com}BeneficiaryInstitution_D uses Python identifier BeneficiaryInstitution_D
    __BeneficiaryInstitution_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_D'), 'BeneficiaryInstitution_D', '__httpwww_w3schools_com_MT300_SequenceD_SplitSettlementDetails_SettlementDetails_httpwww_w3schools_comBeneficiaryInstitution_D', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1739, 4), )

    
    BeneficiaryInstitution_D = property(__BeneficiaryInstitution_D.value, __BeneficiaryInstitution_D.set, None, None)

    
    # Element {http://www.w3schools.com}BeneficiaryInstitution_J uses Python identifier BeneficiaryInstitution_J
    __BeneficiaryInstitution_J = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_J'), 'BeneficiaryInstitution_J', '__httpwww_w3schools_com_MT300_SequenceD_SplitSettlementDetails_SettlementDetails_httpwww_w3schools_comBeneficiaryInstitution_J', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1740, 4), )

    
    BeneficiaryInstitution_J = property(__BeneficiaryInstitution_J.value, __BeneficiaryInstitution_J.set, None, None)

    _ElementMap.update({
        __BuySellIndicator.name() : __BuySellIndicator,
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
        
    })
_module_typeBindings.MT300_SequenceD_SplitSettlementDetails_SettlementDetails = MT300_SequenceD_SplitSettlementDetails_SettlementDetails
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceD_SplitSettlementDetails_SettlementDetails', MT300_SequenceD_SplitSettlementDetails_SettlementDetails)


# Complex type {http://www.w3schools.com}MT300_SequenceE_ReportingInformation with content type ELEMENT_ONLY
class MT300_SequenceE_ReportingInformation (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceE_ReportingInformation with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceE_ReportingInformation')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1744, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}SubSequenceE1_ReportingParties uses Python identifier SubSequenceE1_ReportingParties
    __SubSequenceE1_ReportingParties = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SubSequenceE1_ReportingParties'), 'SubSequenceE1_ReportingParties', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_httpwww_w3schools_comSubSequenceE1_ReportingParties', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1746, 3), )

    
    SubSequenceE1_ReportingParties = property(__SubSequenceE1_ReportingParties.value, __SubSequenceE1_ReportingParties.set, None, None)

    
    # Element {http://www.w3schools.com}CentralCounterpartyClearingHouse_A uses Python identifier CentralCounterpartyClearingHouse_A
    __CentralCounterpartyClearingHouse_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'CentralCounterpartyClearingHouse_A'), 'CentralCounterpartyClearingHouse_A', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_httpwww_w3schools_comCentralCounterpartyClearingHouse_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1748, 4), )

    
    CentralCounterpartyClearingHouse_A = property(__CentralCounterpartyClearingHouse_A.value, __CentralCounterpartyClearingHouse_A.set, None, None)

    
    # Element {http://www.w3schools.com}CentralCounterpartyClearingHouse_D uses Python identifier CentralCounterpartyClearingHouse_D
    __CentralCounterpartyClearingHouse_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'CentralCounterpartyClearingHouse_D'), 'CentralCounterpartyClearingHouse_D', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_httpwww_w3schools_comCentralCounterpartyClearingHouse_D', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1749, 4), )

    
    CentralCounterpartyClearingHouse_D = property(__CentralCounterpartyClearingHouse_D.value, __CentralCounterpartyClearingHouse_D.set, None, None)

    
    # Element {http://www.w3schools.com}CentralCounterpartyClearingHouse_J uses Python identifier CentralCounterpartyClearingHouse_J
    __CentralCounterpartyClearingHouse_J = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'CentralCounterpartyClearingHouse_J'), 'CentralCounterpartyClearingHouse_J', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_httpwww_w3schools_comCentralCounterpartyClearingHouse_J', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1750, 4), )

    
    CentralCounterpartyClearingHouse_J = property(__CentralCounterpartyClearingHouse_J.value, __CentralCounterpartyClearingHouse_J.set, None, None)

    
    # Element {http://www.w3schools.com}ClearingBroker_A uses Python identifier ClearingBroker_A
    __ClearingBroker_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ClearingBroker_A'), 'ClearingBroker_A', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_httpwww_w3schools_comClearingBroker_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1753, 4), )

    
    ClearingBroker_A = property(__ClearingBroker_A.value, __ClearingBroker_A.set, None, None)

    
    # Element {http://www.w3schools.com}ClearingBroker_D uses Python identifier ClearingBroker_D
    __ClearingBroker_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ClearingBroker_D'), 'ClearingBroker_D', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_httpwww_w3schools_comClearingBroker_D', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1754, 4), )

    
    ClearingBroker_D = property(__ClearingBroker_D.value, __ClearingBroker_D.set, None, None)

    
    # Element {http://www.w3schools.com}ClearingBroker_J uses Python identifier ClearingBroker_J
    __ClearingBroker_J = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ClearingBroker_J'), 'ClearingBroker_J', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_httpwww_w3schools_comClearingBroker_J', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1755, 4), )

    
    ClearingBroker_J = property(__ClearingBroker_J.value, __ClearingBroker_J.set, None, None)

    
    # Element {http://www.w3schools.com}ClearingExceptionParty_A uses Python identifier ClearingExceptionParty_A
    __ClearingExceptionParty_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ClearingExceptionParty_A'), 'ClearingExceptionParty_A', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_httpwww_w3schools_comClearingExceptionParty_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1758, 4), )

    
    ClearingExceptionParty_A = property(__ClearingExceptionParty_A.value, __ClearingExceptionParty_A.set, None, None)

    
    # Element {http://www.w3schools.com}ClearingExceptionParty_D uses Python identifier ClearingExceptionParty_D
    __ClearingExceptionParty_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ClearingExceptionParty_D'), 'ClearingExceptionParty_D', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_httpwww_w3schools_comClearingExceptionParty_D', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1759, 4), )

    
    ClearingExceptionParty_D = property(__ClearingExceptionParty_D.value, __ClearingExceptionParty_D.set, None, None)

    
    # Element {http://www.w3schools.com}ClearingExceptionParty_J uses Python identifier ClearingExceptionParty_J
    __ClearingExceptionParty_J = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ClearingExceptionParty_J'), 'ClearingExceptionParty_J', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_httpwww_w3schools_comClearingExceptionParty_J', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1760, 4), )

    
    ClearingExceptionParty_J = property(__ClearingExceptionParty_J.value, __ClearingExceptionParty_J.set, None, None)

    
    # Element {http://www.w3schools.com}ClearingBrokerIdentification uses Python identifier ClearingBrokerIdentification
    __ClearingBrokerIdentification = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ClearingBrokerIdentification'), 'ClearingBrokerIdentification', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_httpwww_w3schools_comClearingBrokerIdentification', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1762, 3), )

    
    ClearingBrokerIdentification = property(__ClearingBrokerIdentification.value, __ClearingBrokerIdentification.set, None, None)

    
    # Element {http://www.w3schools.com}ClearedProductIdentification uses Python identifier ClearedProductIdentification
    __ClearedProductIdentification = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ClearedProductIdentification'), 'ClearedProductIdentification', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_httpwww_w3schools_comClearedProductIdentification', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1763, 3), )

    
    ClearedProductIdentification = property(__ClearedProductIdentification.value, __ClearedProductIdentification.set, None, None)

    
    # Element {http://www.w3schools.com}ClearingThresholdIndicator uses Python identifier ClearingThresholdIndicator
    __ClearingThresholdIndicator = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ClearingThresholdIndicator'), 'ClearingThresholdIndicator', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_httpwww_w3schools_comClearingThresholdIndicator', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1764, 3), )

    
    ClearingThresholdIndicator = property(__ClearingThresholdIndicator.value, __ClearingThresholdIndicator.set, None, None)

    
    # Element {http://www.w3schools.com}UnderlyingProductIdentifier uses Python identifier UnderlyingProductIdentifier
    __UnderlyingProductIdentifier = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'UnderlyingProductIdentifier'), 'UnderlyingProductIdentifier', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_httpwww_w3schools_comUnderlyingProductIdentifier', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1765, 3), )

    
    UnderlyingProductIdentifier = property(__UnderlyingProductIdentifier.value, __UnderlyingProductIdentifier.set, None, None)

    
    # Element {http://www.w3schools.com}IdentificationOfFinancialInstrument uses Python identifier IdentificationOfFinancialInstrument
    __IdentificationOfFinancialInstrument = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'IdentificationOfFinancialInstrument'), 'IdentificationOfFinancialInstrument', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_httpwww_w3schools_comIdentificationOfFinancialInstrument', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1766, 3), )

    
    IdentificationOfFinancialInstrument = property(__IdentificationOfFinancialInstrument.value, __IdentificationOfFinancialInstrument.set, None, None)

    
    # Element {http://www.w3schools.com}AllocationIndicator uses Python identifier AllocationIndicator
    __AllocationIndicator = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'AllocationIndicator'), 'AllocationIndicator', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_httpwww_w3schools_comAllocationIndicator', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1767, 3), )

    
    AllocationIndicator = property(__AllocationIndicator.value, __AllocationIndicator.set, None, None)

    
    # Element {http://www.w3schools.com}CollateralisationIndicator uses Python identifier CollateralisationIndicator
    __CollateralisationIndicator = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'CollateralisationIndicator'), 'CollateralisationIndicator', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_httpwww_w3schools_comCollateralisationIndicator', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1768, 3), )

    
    CollateralisationIndicator = property(__CollateralisationIndicator.value, __CollateralisationIndicator.set, None, None)

    
    # Element {http://www.w3schools.com}ExecutionVenue uses Python identifier ExecutionVenue
    __ExecutionVenue = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ExecutionVenue'), 'ExecutionVenue', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_httpwww_w3schools_comExecutionVenue', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1769, 3), )

    
    ExecutionVenue = property(__ExecutionVenue.value, __ExecutionVenue.set, None, None)

    
    # Element {http://www.w3schools.com}ExecutionTimestamp uses Python identifier ExecutionTimestamp
    __ExecutionTimestamp = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ExecutionTimestamp'), 'ExecutionTimestamp', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_httpwww_w3schools_comExecutionTimestamp', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1770, 3), )

    
    ExecutionTimestamp = property(__ExecutionTimestamp.value, __ExecutionTimestamp.set, None, None)

    
    # Element {http://www.w3schools.com}NonStandardFlag uses Python identifier NonStandardFlag
    __NonStandardFlag = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'NonStandardFlag'), 'NonStandardFlag', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_httpwww_w3schools_comNonStandardFlag', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1771, 3), )

    
    NonStandardFlag = property(__NonStandardFlag.value, __NonStandardFlag.set, None, None)

    
    # Element {http://www.w3schools.com}LinkSwapIdentification uses Python identifier LinkSwapIdentification
    __LinkSwapIdentification = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'LinkSwapIdentification'), 'LinkSwapIdentification', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_httpwww_w3schools_comLinkSwapIdentification', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1772, 3), )

    
    LinkSwapIdentification = property(__LinkSwapIdentification.value, __LinkSwapIdentification.set, None, None)

    
    # Element {http://www.w3schools.com}FinancialNatureOfCounterpartyIndicator uses Python identifier FinancialNatureOfCounterpartyIndicator
    __FinancialNatureOfCounterpartyIndicator = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'FinancialNatureOfCounterpartyIndicator'), 'FinancialNatureOfCounterpartyIndicator', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_httpwww_w3schools_comFinancialNatureOfCounterpartyIndicator', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1773, 3), )

    
    FinancialNatureOfCounterpartyIndicator = property(__FinancialNatureOfCounterpartyIndicator.value, __FinancialNatureOfCounterpartyIndicator.set, None, None)

    
    # Element {http://www.w3schools.com}CollateralPortfolioIndicator uses Python identifier CollateralPortfolioIndicator
    __CollateralPortfolioIndicator = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'CollateralPortfolioIndicator'), 'CollateralPortfolioIndicator', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_httpwww_w3schools_comCollateralPortfolioIndicator', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1774, 3), )

    
    CollateralPortfolioIndicator = property(__CollateralPortfolioIndicator.value, __CollateralPortfolioIndicator.set, None, None)

    
    # Element {http://www.w3schools.com}CollateralPortfolioCode uses Python identifier CollateralPortfolioCode
    __CollateralPortfolioCode = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'CollateralPortfolioCode'), 'CollateralPortfolioCode', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_httpwww_w3schools_comCollateralPortfolioCode', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1775, 3), )

    
    CollateralPortfolioCode = property(__CollateralPortfolioCode.value, __CollateralPortfolioCode.set, None, None)

    
    # Element {http://www.w3schools.com}PortfolioCompressionIndicator uses Python identifier PortfolioCompressionIndicator
    __PortfolioCompressionIndicator = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PortfolioCompressionIndicator'), 'PortfolioCompressionIndicator', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_httpwww_w3schools_comPortfolioCompressionIndicator', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1776, 3), )

    
    PortfolioCompressionIndicator = property(__PortfolioCompressionIndicator.value, __PortfolioCompressionIndicator.set, None, None)

    
    # Element {http://www.w3schools.com}CorporateSectorIndicator uses Python identifier CorporateSectorIndicator
    __CorporateSectorIndicator = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'CorporateSectorIndicator'), 'CorporateSectorIndicator', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_httpwww_w3schools_comCorporateSectorIndicator', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1777, 3), )

    
    CorporateSectorIndicator = property(__CorporateSectorIndicator.value, __CorporateSectorIndicator.set, None, None)

    
    # Element {http://www.w3schools.com}TradeWithNonEEACounterpartyIndicator uses Python identifier TradeWithNonEEACounterpartyIndicator
    __TradeWithNonEEACounterpartyIndicator = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'TradeWithNonEEACounterpartyIndicator'), 'TradeWithNonEEACounterpartyIndicator', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_httpwww_w3schools_comTradeWithNonEEACounterpartyIndicator', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1778, 3), )

    
    TradeWithNonEEACounterpartyIndicator = property(__TradeWithNonEEACounterpartyIndicator.value, __TradeWithNonEEACounterpartyIndicator.set, None, None)

    
    # Element {http://www.w3schools.com}IntragroupTradeIndicator uses Python identifier IntragroupTradeIndicator
    __IntragroupTradeIndicator = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'IntragroupTradeIndicator'), 'IntragroupTradeIndicator', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_httpwww_w3schools_comIntragroupTradeIndicator', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1779, 3), )

    
    IntragroupTradeIndicator = property(__IntragroupTradeIndicator.value, __IntragroupTradeIndicator.set, None, None)

    
    # Element {http://www.w3schools.com}CommercialOrTreasuryFinancingIndicator uses Python identifier CommercialOrTreasuryFinancingIndicator
    __CommercialOrTreasuryFinancingIndicator = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'CommercialOrTreasuryFinancingIndicator'), 'CommercialOrTreasuryFinancingIndicator', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_httpwww_w3schools_comCommercialOrTreasuryFinancingIndicator', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1780, 3), )

    
    CommercialOrTreasuryFinancingIndicator = property(__CommercialOrTreasuryFinancingIndicator.value, __CommercialOrTreasuryFinancingIndicator.set, None, None)

    
    # Element {http://www.w3schools.com}ConfirmationTimestamp uses Python identifier ConfirmationTimestamp
    __ConfirmationTimestamp = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ConfirmationTimestamp'), 'ConfirmationTimestamp', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_httpwww_w3schools_comConfirmationTimestamp', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1781, 3), )

    
    ConfirmationTimestamp = property(__ConfirmationTimestamp.value, __ConfirmationTimestamp.set, None, None)

    
    # Element {http://www.w3schools.com}ClearingTimestamp uses Python identifier ClearingTimestamp
    __ClearingTimestamp = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ClearingTimestamp'), 'ClearingTimestamp', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_httpwww_w3schools_comClearingTimestamp', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1782, 3), )

    
    ClearingTimestamp = property(__ClearingTimestamp.value, __ClearingTimestamp.set, None, None)

    
    # Element {http://www.w3schools.com}CommissionAndFees uses Python identifier CommissionAndFees
    __CommissionAndFees = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'CommissionAndFees'), 'CommissionAndFees', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_httpwww_w3schools_comCommissionAndFees', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1783, 3), )

    
    CommissionAndFees = property(__CommissionAndFees.value, __CommissionAndFees.set, None, None)

    
    # Element {http://www.w3schools.com}AdditionalReportingInformation uses Python identifier AdditionalReportingInformation
    __AdditionalReportingInformation = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'AdditionalReportingInformation'), 'AdditionalReportingInformation', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_httpwww_w3schools_comAdditionalReportingInformation', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1784, 3), )

    
    AdditionalReportingInformation = property(__AdditionalReportingInformation.value, __AdditionalReportingInformation.set, None, None)

    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='15E')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1786, 2)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1786, 2)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1787, 2)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1787, 2)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    
    # Attribute formatTag uses Python identifier formatTag
    __formatTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'formatTag'), 'formatTag', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_formatTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='False')
    __formatTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1788, 2)
    __formatTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1788, 2)
    
    formatTag = property(__formatTag.value, __formatTag.set, None, None)

    _ElementMap.update({
        __SubSequenceE1_ReportingParties.name() : __SubSequenceE1_ReportingParties,
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
        __LinkSwapIdentification.name() : __LinkSwapIdentification,
        __FinancialNatureOfCounterpartyIndicator.name() : __FinancialNatureOfCounterpartyIndicator,
        __CollateralPortfolioIndicator.name() : __CollateralPortfolioIndicator,
        __CollateralPortfolioCode.name() : __CollateralPortfolioCode,
        __PortfolioCompressionIndicator.name() : __PortfolioCompressionIndicator,
        __CorporateSectorIndicator.name() : __CorporateSectorIndicator,
        __TradeWithNonEEACounterpartyIndicator.name() : __TradeWithNonEEACounterpartyIndicator,
        __IntragroupTradeIndicator.name() : __IntragroupTradeIndicator,
        __CommercialOrTreasuryFinancingIndicator.name() : __CommercialOrTreasuryFinancingIndicator,
        __ConfirmationTimestamp.name() : __ConfirmationTimestamp,
        __ClearingTimestamp.name() : __ClearingTimestamp,
        __CommissionAndFees.name() : __CommissionAndFees,
        __AdditionalReportingInformation.name() : __AdditionalReportingInformation
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory,
        __formatTag.name() : __formatTag
    })
_module_typeBindings.MT300_SequenceE_ReportingInformation = MT300_SequenceE_ReportingInformation
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceE_ReportingInformation', MT300_SequenceE_ReportingInformation)


# Complex type {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties with content type ELEMENT_ONLY
class MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1790, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}ReportingJurisdiction uses Python identifier ReportingJurisdiction
    __ReportingJurisdiction = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ReportingJurisdiction'), 'ReportingJurisdiction', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_httpwww_w3schools_comReportingJurisdiction', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1792, 3), )

    
    ReportingJurisdiction = property(__ReportingJurisdiction.value, __ReportingJurisdiction.set, None, None)

    
    # Element {http://www.w3schools.com}ReportingParty_A uses Python identifier ReportingParty_A
    __ReportingParty_A = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ReportingParty_A'), 'ReportingParty_A', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_httpwww_w3schools_comReportingParty_A', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1794, 4), )

    
    ReportingParty_A = property(__ReportingParty_A.value, __ReportingParty_A.set, None, None)

    
    # Element {http://www.w3schools.com}ReportingParty_D uses Python identifier ReportingParty_D
    __ReportingParty_D = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ReportingParty_D'), 'ReportingParty_D', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_httpwww_w3schools_comReportingParty_D', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1795, 4), )

    
    ReportingParty_D = property(__ReportingParty_D.value, __ReportingParty_D.set, None, None)

    
    # Element {http://www.w3schools.com}ReportingParty_J uses Python identifier ReportingParty_J
    __ReportingParty_J = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ReportingParty_J'), 'ReportingParty_J', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_httpwww_w3schools_comReportingParty_J', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1796, 4), )

    
    ReportingParty_J = property(__ReportingParty_J.value, __ReportingParty_J.set, None, None)

    
    # Element {http://www.w3schools.com}SubSequenceE1a_UniqueTransactionIdentifier uses Python identifier SubSequenceE1a_UniqueTransactionIdentifier
    __SubSequenceE1a_UniqueTransactionIdentifier = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SubSequenceE1a_UniqueTransactionIdentifier'), 'SubSequenceE1a_UniqueTransactionIdentifier', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_httpwww_w3schools_comSubSequenceE1a_UniqueTransactionIdentifier', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1798, 3), )

    
    SubSequenceE1a_UniqueTransactionIdentifier = property(__SubSequenceE1a_UniqueTransactionIdentifier.value, __SubSequenceE1a_UniqueTransactionIdentifier.set, None, None)

    _ElementMap.update({
        __ReportingJurisdiction.name() : __ReportingJurisdiction,
        __ReportingParty_A.name() : __ReportingParty_A,
        __ReportingParty_D.name() : __ReportingParty_D,
        __ReportingParty_J.name() : __ReportingParty_J,
        __SubSequenceE1a_UniqueTransactionIdentifier.name() : __SubSequenceE1a_UniqueTransactionIdentifier
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties = MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties', MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties)


# Complex type {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier with content type ELEMENT_ONLY
class MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1801, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}UTINamespaceIssuerCode uses Python identifier UTINamespaceIssuerCode
    __UTINamespaceIssuerCode = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'UTINamespaceIssuerCode'), 'UTINamespaceIssuerCode', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_httpwww_w3schools_comUTINamespaceIssuerCode', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1803, 3), )

    
    UTINamespaceIssuerCode = property(__UTINamespaceIssuerCode.value, __UTINamespaceIssuerCode.set, None, None)

    
    # Element {http://www.w3schools.com}TransactionIdentifier uses Python identifier TransactionIdentifier
    __TransactionIdentifier = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'TransactionIdentifier'), 'TransactionIdentifier', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_httpwww_w3schools_comTransactionIdentifier', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1804, 3), )

    
    TransactionIdentifier = property(__TransactionIdentifier.value, __TransactionIdentifier.set, None, None)

    
    # Element {http://www.w3schools.com}SubSequenceE1a1_PriorUniqueTransactionIdentifier uses Python identifier SubSequenceE1a1_PriorUniqueTransactionIdentifier
    __SubSequenceE1a1_PriorUniqueTransactionIdentifier = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SubSequenceE1a1_PriorUniqueTransactionIdentifier'), 'SubSequenceE1a1_PriorUniqueTransactionIdentifier', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_httpwww_w3schools_comSubSequenceE1a1_PriorUniqueTransactionIdentifier', True, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1805, 3), )

    
    SubSequenceE1a1_PriorUniqueTransactionIdentifier = property(__SubSequenceE1a1_PriorUniqueTransactionIdentifier.value, __SubSequenceE1a1_PriorUniqueTransactionIdentifier.set, None, None)

    _ElementMap.update({
        __UTINamespaceIssuerCode.name() : __UTINamespaceIssuerCode,
        __TransactionIdentifier.name() : __TransactionIdentifier,
        __SubSequenceE1a1_PriorUniqueTransactionIdentifier.name() : __SubSequenceE1a1_PriorUniqueTransactionIdentifier
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier = MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier', MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier)


# Complex type {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_SubSequenceE1a1_PriorUniqueTransactionIdentifier with content type ELEMENT_ONLY
class MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_SubSequenceE1a1_PriorUniqueTransactionIdentifier (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_SubSequenceE1a1_PriorUniqueTransactionIdentifier with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_SubSequenceE1a1_PriorUniqueTransactionIdentifier')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1808, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}PUTINamespaceIssuerCode uses Python identifier PUTINamespaceIssuerCode
    __PUTINamespaceIssuerCode = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PUTINamespaceIssuerCode'), 'PUTINamespaceIssuerCode', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_SubSequenceE1a1_PriorUniqueTransactionIdentifier_httpwww_w3schools_comPUTINamespaceIssuerCode', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1810, 3), )

    
    PUTINamespaceIssuerCode = property(__PUTINamespaceIssuerCode.value, __PUTINamespaceIssuerCode.set, None, None)

    
    # Element {http://www.w3schools.com}PriorTransactionIdentifier uses Python identifier PriorTransactionIdentifier
    __PriorTransactionIdentifier = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PriorTransactionIdentifier'), 'PriorTransactionIdentifier', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_SubSequenceE1a1_PriorUniqueTransactionIdentifier_httpwww_w3schools_comPriorTransactionIdentifier', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1811, 3), )

    
    PriorTransactionIdentifier = property(__PriorTransactionIdentifier.value, __PriorTransactionIdentifier.set, None, None)

    _ElementMap.update({
        __PUTINamespaceIssuerCode.name() : __PUTINamespaceIssuerCode,
        __PriorTransactionIdentifier.name() : __PriorTransactionIdentifier
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_SubSequenceE1a1_PriorUniqueTransactionIdentifier = MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_SubSequenceE1a1_PriorUniqueTransactionIdentifier
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_SubSequenceE1a1_PriorUniqueTransactionIdentifier', MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_SubSequenceE1a1_PriorUniqueTransactionIdentifier)


# Complex type {http://www.w3schools.com}MT300_SequenceF_PostTradeEvents with content type ELEMENT_ONLY
class MT300_SequenceF_PostTradeEvents (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceF_PostTradeEvents with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceF_PostTradeEvents')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1814, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}EventTypeAndReference uses Python identifier EventTypeAndReference
    __EventTypeAndReference = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'EventTypeAndReference'), 'EventTypeAndReference', '__httpwww_w3schools_com_MT300_SequenceF_PostTradeEvents_httpwww_w3schools_comEventTypeAndReference', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1816, 3), )

    
    EventTypeAndReference = property(__EventTypeAndReference.value, __EventTypeAndReference.set, None, None)

    
    # Element {http://www.w3schools.com}UnderlyingLiabilityReference uses Python identifier UnderlyingLiabilityReference
    __UnderlyingLiabilityReference = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'UnderlyingLiabilityReference'), 'UnderlyingLiabilityReference', '__httpwww_w3schools_com_MT300_SequenceF_PostTradeEvents_httpwww_w3schools_comUnderlyingLiabilityReference', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1817, 3), )

    
    UnderlyingLiabilityReference = property(__UnderlyingLiabilityReference.value, __UnderlyingLiabilityReference.set, None, None)

    
    # Element {http://www.w3schools.com}ProfitAndLossSettlementDate uses Python identifier ProfitAndLossSettlementDate
    __ProfitAndLossSettlementDate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ProfitAndLossSettlementDate'), 'ProfitAndLossSettlementDate', '__httpwww_w3schools_com_MT300_SequenceF_PostTradeEvents_httpwww_w3schools_comProfitAndLossSettlementDate', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1818, 3), )

    
    ProfitAndLossSettlementDate = property(__ProfitAndLossSettlementDate.value, __ProfitAndLossSettlementDate.set, None, None)

    
    # Element {http://www.w3schools.com}ProfitAndLossSettlementAmount uses Python identifier ProfitAndLossSettlementAmount
    __ProfitAndLossSettlementAmount = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ProfitAndLossSettlementAmount'), 'ProfitAndLossSettlementAmount', '__httpwww_w3schools_com_MT300_SequenceF_PostTradeEvents_httpwww_w3schools_comProfitAndLossSettlementAmount', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1819, 3), )

    
    ProfitAndLossSettlementAmount = property(__ProfitAndLossSettlementAmount.value, __ProfitAndLossSettlementAmount.set, None, None)

    
    # Element {http://www.w3schools.com}OutstandingSettlementAmount uses Python identifier OutstandingSettlementAmount
    __OutstandingSettlementAmount = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'OutstandingSettlementAmount'), 'OutstandingSettlementAmount', '__httpwww_w3schools_com_MT300_SequenceF_PostTradeEvents_httpwww_w3schools_comOutstandingSettlementAmount', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1820, 3), )

    
    OutstandingSettlementAmount = property(__OutstandingSettlementAmount.value, __OutstandingSettlementAmount.set, None, None)

    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceF_PostTradeEvents_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='15F')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1822, 2)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1822, 2)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceF_PostTradeEvents_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1823, 2)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1823, 2)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    
    # Attribute formatTag uses Python identifier formatTag
    __formatTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'formatTag'), 'formatTag', '__httpwww_w3schools_com_MT300_SequenceF_PostTradeEvents_formatTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='False')
    __formatTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1824, 2)
    __formatTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1824, 2)
    
    formatTag = property(__formatTag.value, __formatTag.set, None, None)

    _ElementMap.update({
        __EventTypeAndReference.name() : __EventTypeAndReference,
        __UnderlyingLiabilityReference.name() : __UnderlyingLiabilityReference,
        __ProfitAndLossSettlementDate.name() : __ProfitAndLossSettlementDate,
        __ProfitAndLossSettlementAmount.name() : __ProfitAndLossSettlementAmount,
        __OutstandingSettlementAmount.name() : __OutstandingSettlementAmount
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory,
        __formatTag.name() : __formatTag
    })
_module_typeBindings.MT300_SequenceF_PostTradeEvents = MT300_SequenceF_PostTradeEvents
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceF_PostTradeEvents', MT300_SequenceF_PostTradeEvents)


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1827, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3schools.com}SequenceA_GeneralInformation uses Python identifier SequenceA_GeneralInformation
    __SequenceA_GeneralInformation = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SequenceA_GeneralInformation'), 'SequenceA_GeneralInformation', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comSequenceA_GeneralInformation', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1829, 4), )

    
    SequenceA_GeneralInformation = property(__SequenceA_GeneralInformation.value, __SequenceA_GeneralInformation.set, None, None)

    
    # Element {http://www.w3schools.com}SequenceB_TransactionDetails uses Python identifier SequenceB_TransactionDetails
    __SequenceB_TransactionDetails = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SequenceB_TransactionDetails'), 'SequenceB_TransactionDetails', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comSequenceB_TransactionDetails', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1830, 4), )

    
    SequenceB_TransactionDetails = property(__SequenceB_TransactionDetails.value, __SequenceB_TransactionDetails.set, None, None)

    
    # Element {http://www.w3schools.com}SequenceC_OptionalGeneralInformation uses Python identifier SequenceC_OptionalGeneralInformation
    __SequenceC_OptionalGeneralInformation = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SequenceC_OptionalGeneralInformation'), 'SequenceC_OptionalGeneralInformation', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comSequenceC_OptionalGeneralInformation', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1831, 4), )

    
    SequenceC_OptionalGeneralInformation = property(__SequenceC_OptionalGeneralInformation.value, __SequenceC_OptionalGeneralInformation.set, None, None)

    
    # Element {http://www.w3schools.com}SequenceD_SplitSettlementDetails uses Python identifier SequenceD_SplitSettlementDetails
    __SequenceD_SplitSettlementDetails = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SequenceD_SplitSettlementDetails'), 'SequenceD_SplitSettlementDetails', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comSequenceD_SplitSettlementDetails', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1832, 4), )

    
    SequenceD_SplitSettlementDetails = property(__SequenceD_SplitSettlementDetails.value, __SequenceD_SplitSettlementDetails.set, None, None)

    
    # Element {http://www.w3schools.com}SequenceE_ReportingInformation uses Python identifier SequenceE_ReportingInformation
    __SequenceE_ReportingInformation = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SequenceE_ReportingInformation'), 'SequenceE_ReportingInformation', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comSequenceE_ReportingInformation', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1833, 4), )

    
    SequenceE_ReportingInformation = property(__SequenceE_ReportingInformation.value, __SequenceE_ReportingInformation.set, None, None)

    
    # Element {http://www.w3schools.com}SequenceF_PostTradeEvents uses Python identifier SequenceF_PostTradeEvents
    __SequenceF_PostTradeEvents = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SequenceF_PostTradeEvents'), 'SequenceF_PostTradeEvents', '__httpwww_w3schools_com_CTD_ANON_httpwww_w3schools_comSequenceF_PostTradeEvents', False, pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1834, 4), )

    
    SequenceF_PostTradeEvents = property(__SequenceF_PostTradeEvents.value, __SequenceF_PostTradeEvents.set, None, None)

    _ElementMap.update({
        __SequenceA_GeneralInformation.name() : __SequenceA_GeneralInformation,
        __SequenceB_TransactionDetails.name() : __SequenceB_TransactionDetails,
        __SequenceC_OptionalGeneralInformation.name() : __SequenceC_OptionalGeneralInformation,
        __SequenceD_SplitSettlementDetails.name() : __SequenceD_SplitSettlementDetails,
        __SequenceE_ReportingInformation.name() : __SequenceE_ReportingInformation,
        __SequenceF_PostTradeEvents.name() : __SequenceF_PostTradeEvents
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON = CTD_ANON


# Complex type {http://www.w3schools.com}MT300_SequenceA_GeneralInformation_20_Type with content type SIMPLE
class MT300_SequenceA_GeneralInformation_20_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceA_GeneralInformation_20_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceA_GeneralInformation_20_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceA_GeneralInformation_20_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 8, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceA_GeneralInformation_20_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceA_GeneralInformation_20_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='20')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 11, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 11, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceA_GeneralInformation_20_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 12, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 12, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceA_GeneralInformation_20_Type = MT300_SequenceA_GeneralInformation_20_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceA_GeneralInformation_20_Type', MT300_SequenceA_GeneralInformation_20_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceA_GeneralInformation_21_Type with content type SIMPLE
class MT300_SequenceA_GeneralInformation_21_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceA_GeneralInformation_21_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceA_GeneralInformation_21_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceA_GeneralInformation_21_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 21, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceA_GeneralInformation_21_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceA_GeneralInformation_21_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='21')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 24, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 24, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceA_GeneralInformation_21_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 25, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 25, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceA_GeneralInformation_21_Type = MT300_SequenceA_GeneralInformation_21_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceA_GeneralInformation_21_Type', MT300_SequenceA_GeneralInformation_21_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceA_GeneralInformation_22A_Type with content type SIMPLE
class MT300_SequenceA_GeneralInformation_22A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceA_GeneralInformation_22A_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceA_GeneralInformation_22A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceA_GeneralInformation_22A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 34, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceA_GeneralInformation_22A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceA_GeneralInformation_22A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='22A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 37, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 37, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceA_GeneralInformation_22A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 38, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 38, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceA_GeneralInformation_22A_Type = MT300_SequenceA_GeneralInformation_22A_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceA_GeneralInformation_22A_Type', MT300_SequenceA_GeneralInformation_22A_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceA_GeneralInformation_94A_Type with content type SIMPLE
class MT300_SequenceA_GeneralInformation_94A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceA_GeneralInformation_94A_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceA_GeneralInformation_94A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceA_GeneralInformation_94A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 47, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceA_GeneralInformation_94A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceA_GeneralInformation_94A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='94A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 50, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 50, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceA_GeneralInformation_94A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 51, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 51, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceA_GeneralInformation_94A_Type = MT300_SequenceA_GeneralInformation_94A_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceA_GeneralInformation_94A_Type', MT300_SequenceA_GeneralInformation_94A_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceA_GeneralInformation_22C_Type with content type SIMPLE
class MT300_SequenceA_GeneralInformation_22C_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceA_GeneralInformation_22C_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceA_GeneralInformation_22C_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceA_GeneralInformation_22C_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 60, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceA_GeneralInformation_22C_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceA_GeneralInformation_22C_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='22C')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 63, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 63, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceA_GeneralInformation_22C_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 64, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 64, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceA_GeneralInformation_22C_Type = MT300_SequenceA_GeneralInformation_22C_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceA_GeneralInformation_22C_Type', MT300_SequenceA_GeneralInformation_22C_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceA_GeneralInformation_17T_Type with content type SIMPLE
class MT300_SequenceA_GeneralInformation_17T_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceA_GeneralInformation_17T_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceA_GeneralInformation_17T_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceA_GeneralInformation_17T_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 73, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceA_GeneralInformation_17T_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceA_GeneralInformation_17T_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='17T')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 76, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 76, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceA_GeneralInformation_17T_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 77, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 77, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceA_GeneralInformation_17T_Type = MT300_SequenceA_GeneralInformation_17T_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceA_GeneralInformation_17T_Type', MT300_SequenceA_GeneralInformation_17T_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceA_GeneralInformation_17U_Type with content type SIMPLE
class MT300_SequenceA_GeneralInformation_17U_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceA_GeneralInformation_17U_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceA_GeneralInformation_17U_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceA_GeneralInformation_17U_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 86, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceA_GeneralInformation_17U_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceA_GeneralInformation_17U_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='17U')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 89, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 89, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceA_GeneralInformation_17U_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 90, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 90, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceA_GeneralInformation_17U_Type = MT300_SequenceA_GeneralInformation_17U_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceA_GeneralInformation_17U_Type', MT300_SequenceA_GeneralInformation_17U_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceA_GeneralInformation_17I_Type with content type SIMPLE
class MT300_SequenceA_GeneralInformation_17I_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceA_GeneralInformation_17I_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceA_GeneralInformation_17I_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceA_GeneralInformation_17I_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 99, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceA_GeneralInformation_17I_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceA_GeneralInformation_17I_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='17I')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 102, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 102, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceA_GeneralInformation_17I_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 103, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 103, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceA_GeneralInformation_17I_Type = MT300_SequenceA_GeneralInformation_17I_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceA_GeneralInformation_17I_Type', MT300_SequenceA_GeneralInformation_17I_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceA_GeneralInformation_82A_Type with content type SIMPLE
class MT300_SequenceA_GeneralInformation_82A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceA_GeneralInformation_82A_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceA_GeneralInformation_82A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceA_GeneralInformation_82A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 112, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceA_GeneralInformation_82A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceA_GeneralInformation_82A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='82A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 115, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 115, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceA_GeneralInformation_82A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 116, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 116, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceA_GeneralInformation_82A_Type = MT300_SequenceA_GeneralInformation_82A_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceA_GeneralInformation_82A_Type', MT300_SequenceA_GeneralInformation_82A_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceA_GeneralInformation_82J_Type with content type SIMPLE
class MT300_SequenceA_GeneralInformation_82J_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceA_GeneralInformation_82J_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceA_GeneralInformation_82J_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceA_GeneralInformation_82J_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 125, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceA_GeneralInformation_82J_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceA_GeneralInformation_82J_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='82J')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 128, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 128, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceA_GeneralInformation_82J_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 129, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 129, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceA_GeneralInformation_82J_Type = MT300_SequenceA_GeneralInformation_82J_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceA_GeneralInformation_82J_Type', MT300_SequenceA_GeneralInformation_82J_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceA_GeneralInformation_87A_Type with content type SIMPLE
class MT300_SequenceA_GeneralInformation_87A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceA_GeneralInformation_87A_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceA_GeneralInformation_87A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceA_GeneralInformation_87A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 138, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceA_GeneralInformation_87A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceA_GeneralInformation_87A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='87A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 141, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 141, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceA_GeneralInformation_87A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 142, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 142, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceA_GeneralInformation_87A_Type = MT300_SequenceA_GeneralInformation_87A_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceA_GeneralInformation_87A_Type', MT300_SequenceA_GeneralInformation_87A_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceA_GeneralInformation_87J_Type with content type SIMPLE
class MT300_SequenceA_GeneralInformation_87J_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceA_GeneralInformation_87J_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceA_GeneralInformation_87J_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceA_GeneralInformation_87J_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 151, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceA_GeneralInformation_87J_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceA_GeneralInformation_87J_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='87J')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 154, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 154, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceA_GeneralInformation_87J_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 155, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 155, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceA_GeneralInformation_87J_Type = MT300_SequenceA_GeneralInformation_87J_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceA_GeneralInformation_87J_Type', MT300_SequenceA_GeneralInformation_87J_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceA_GeneralInformation_83A_Type with content type SIMPLE
class MT300_SequenceA_GeneralInformation_83A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceA_GeneralInformation_83A_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceA_GeneralInformation_83A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceA_GeneralInformation_83A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 164, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceA_GeneralInformation_83A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceA_GeneralInformation_83A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='83A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 167, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 167, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceA_GeneralInformation_83A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 168, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 168, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceA_GeneralInformation_83A_Type = MT300_SequenceA_GeneralInformation_83A_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceA_GeneralInformation_83A_Type', MT300_SequenceA_GeneralInformation_83A_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceA_GeneralInformation_83J_Type with content type SIMPLE
class MT300_SequenceA_GeneralInformation_83J_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceA_GeneralInformation_83J_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceA_GeneralInformation_83J_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceA_GeneralInformation_83J_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 177, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceA_GeneralInformation_83J_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceA_GeneralInformation_83J_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='83J')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 180, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 180, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceA_GeneralInformation_83J_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 181, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 181, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceA_GeneralInformation_83J_Type = MT300_SequenceA_GeneralInformation_83J_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceA_GeneralInformation_83J_Type', MT300_SequenceA_GeneralInformation_83J_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceA_GeneralInformation_77H_Type with content type SIMPLE
class MT300_SequenceA_GeneralInformation_77H_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceA_GeneralInformation_77H_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceA_GeneralInformation_77H_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceA_GeneralInformation_77H_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 190, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceA_GeneralInformation_77H_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceA_GeneralInformation_77H_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='77H')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 193, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 193, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceA_GeneralInformation_77H_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 194, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 194, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceA_GeneralInformation_77H_Type = MT300_SequenceA_GeneralInformation_77H_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceA_GeneralInformation_77H_Type', MT300_SequenceA_GeneralInformation_77H_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceA_GeneralInformation_77D_Type with content type SIMPLE
class MT300_SequenceA_GeneralInformation_77D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceA_GeneralInformation_77D_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceA_GeneralInformation_77D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceA_GeneralInformation_77D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 203, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceA_GeneralInformation_77D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceA_GeneralInformation_77D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='77D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 206, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 206, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceA_GeneralInformation_77D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 207, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 207, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceA_GeneralInformation_77D_Type = MT300_SequenceA_GeneralInformation_77D_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceA_GeneralInformation_77D_Type', MT300_SequenceA_GeneralInformation_77D_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceA_GeneralInformation_14C_Type with content type SIMPLE
class MT300_SequenceA_GeneralInformation_14C_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceA_GeneralInformation_14C_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceA_GeneralInformation_14C_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceA_GeneralInformation_14C_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 216, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceA_GeneralInformation_14C_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceA_GeneralInformation_14C_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='14C')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 219, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 219, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceA_GeneralInformation_14C_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 220, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 220, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceA_GeneralInformation_14C_Type = MT300_SequenceA_GeneralInformation_14C_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceA_GeneralInformation_14C_Type', MT300_SequenceA_GeneralInformation_14C_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceA_GeneralInformation_17F_Type with content type SIMPLE
class MT300_SequenceA_GeneralInformation_17F_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceA_GeneralInformation_17F_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceA_GeneralInformation_17F_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceA_GeneralInformation_17F_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 229, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceA_GeneralInformation_17F_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceA_GeneralInformation_17F_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='17F')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 232, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 232, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceA_GeneralInformation_17F_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 233, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 233, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceA_GeneralInformation_17F_Type = MT300_SequenceA_GeneralInformation_17F_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceA_GeneralInformation_17F_Type', MT300_SequenceA_GeneralInformation_17F_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceA_GeneralInformation_17O_Type with content type SIMPLE
class MT300_SequenceA_GeneralInformation_17O_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceA_GeneralInformation_17O_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceA_GeneralInformation_17O_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceA_GeneralInformation_17O_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 242, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceA_GeneralInformation_17O_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceA_GeneralInformation_17O_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='17O')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 245, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 245, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceA_GeneralInformation_17O_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 246, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 246, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceA_GeneralInformation_17O_Type = MT300_SequenceA_GeneralInformation_17O_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceA_GeneralInformation_17O_Type', MT300_SequenceA_GeneralInformation_17O_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceA_GeneralInformation_32E_Type with content type SIMPLE
class MT300_SequenceA_GeneralInformation_32E_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceA_GeneralInformation_32E_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceA_GeneralInformation_32E_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceA_GeneralInformation_32E_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 255, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceA_GeneralInformation_32E_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceA_GeneralInformation_32E_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='32E')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 258, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 258, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceA_GeneralInformation_32E_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 259, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 259, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceA_GeneralInformation_32E_Type = MT300_SequenceA_GeneralInformation_32E_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceA_GeneralInformation_32E_Type', MT300_SequenceA_GeneralInformation_32E_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceA_GeneralInformation_30U_Type with content type SIMPLE
class MT300_SequenceA_GeneralInformation_30U_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceA_GeneralInformation_30U_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceA_GeneralInformation_30U_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceA_GeneralInformation_30U_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 268, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceA_GeneralInformation_30U_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceA_GeneralInformation_30U_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='30U')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 271, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 271, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceA_GeneralInformation_30U_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 272, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 272, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceA_GeneralInformation_30U_Type = MT300_SequenceA_GeneralInformation_30U_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceA_GeneralInformation_30U_Type', MT300_SequenceA_GeneralInformation_30U_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceA_GeneralInformation_14S_Type with content type SIMPLE
class MT300_SequenceA_GeneralInformation_14S_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceA_GeneralInformation_14S_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceA_GeneralInformation_14S_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceA_GeneralInformation_14S_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 281, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceA_GeneralInformation_14S_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceA_GeneralInformation_14S_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='14S')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 284, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 284, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceA_GeneralInformation_14S_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 285, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 285, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceA_GeneralInformation_14S_Type = MT300_SequenceA_GeneralInformation_14S_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceA_GeneralInformation_14S_Type', MT300_SequenceA_GeneralInformation_14S_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceA_GeneralInformation_21A_Type with content type SIMPLE
class MT300_SequenceA_GeneralInformation_21A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceA_GeneralInformation_21A_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceA_GeneralInformation_21A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceA_GeneralInformation_21A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 294, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceA_GeneralInformation_21A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceA_GeneralInformation_21A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='21A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 297, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 297, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceA_GeneralInformation_21A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 298, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 298, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceA_GeneralInformation_21A_Type = MT300_SequenceA_GeneralInformation_21A_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceA_GeneralInformation_21A_Type', MT300_SequenceA_GeneralInformation_21A_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceA_GeneralInformation_14E_Type with content type SIMPLE
class MT300_SequenceA_GeneralInformation_14E_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceA_GeneralInformation_14E_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceA_GeneralInformation_14E_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceA_GeneralInformation_14E_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 307, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceA_GeneralInformation_14E_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceA_GeneralInformation_14E_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='14E')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 310, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 310, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceA_GeneralInformation_14E_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 311, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 311, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceA_GeneralInformation_14E_Type = MT300_SequenceA_GeneralInformation_14E_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceA_GeneralInformation_14E_Type', MT300_SequenceA_GeneralInformation_14E_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceB_TransactionDetails_30T_Type with content type SIMPLE
class MT300_SequenceB_TransactionDetails_30T_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceB_TransactionDetails_30T_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceB_TransactionDetails_30T_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceB_TransactionDetails_30T_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 320, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceB_TransactionDetails_30T_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceB_TransactionDetails_30T_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='30T')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 323, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 323, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceB_TransactionDetails_30T_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 324, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 324, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceB_TransactionDetails_30T_Type = MT300_SequenceB_TransactionDetails_30T_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceB_TransactionDetails_30T_Type', MT300_SequenceB_TransactionDetails_30T_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceB_TransactionDetails_30V_Type with content type SIMPLE
class MT300_SequenceB_TransactionDetails_30V_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceB_TransactionDetails_30V_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceB_TransactionDetails_30V_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceB_TransactionDetails_30V_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 333, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceB_TransactionDetails_30V_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceB_TransactionDetails_30V_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='30V')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 336, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 336, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceB_TransactionDetails_30V_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 337, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 337, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceB_TransactionDetails_30V_Type = MT300_SequenceB_TransactionDetails_30V_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceB_TransactionDetails_30V_Type', MT300_SequenceB_TransactionDetails_30V_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceB_TransactionDetails_36_Type with content type SIMPLE
class MT300_SequenceB_TransactionDetails_36_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceB_TransactionDetails_36_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceB_TransactionDetails_36_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceB_TransactionDetails_36_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 346, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceB_TransactionDetails_36_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceB_TransactionDetails_36_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='36')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 349, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 349, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceB_TransactionDetails_36_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 350, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 350, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceB_TransactionDetails_36_Type = MT300_SequenceB_TransactionDetails_36_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceB_TransactionDetails_36_Type', MT300_SequenceB_TransactionDetails_36_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceB_TransactionDetails_39M_Type with content type SIMPLE
class MT300_SequenceB_TransactionDetails_39M_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceB_TransactionDetails_39M_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceB_TransactionDetails_39M_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceB_TransactionDetails_39M_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 359, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceB_TransactionDetails_39M_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceB_TransactionDetails_39M_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='39M')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 362, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 362, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceB_TransactionDetails_39M_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 363, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 363, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceB_TransactionDetails_39M_Type = MT300_SequenceB_TransactionDetails_39M_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceB_TransactionDetails_39M_Type', MT300_SequenceB_TransactionDetails_39M_Type)


# Complex type {http://www.w3schools.com}MT300_SubSequenceB1_AmountBought_32B_Type with content type SIMPLE
class MT300_SubSequenceB1_AmountBought_32B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SubSequenceB1_AmountBought_32B_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SubSequenceB1_AmountBought_32B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SubSequenceB1_AmountBought_32B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 372, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SubSequenceB1_AmountBought_32B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SubSequenceB1_AmountBought_32B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='32B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 375, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 375, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SubSequenceB1_AmountBought_32B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 376, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 376, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SubSequenceB1_AmountBought_32B_Type = MT300_SubSequenceB1_AmountBought_32B_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SubSequenceB1_AmountBought_32B_Type', MT300_SubSequenceB1_AmountBought_32B_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_53A_Type with content type SIMPLE
class MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_53A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_53A_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_53A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_53A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 385, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_53A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_53A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='53A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 388, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 388, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_53A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 389, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 389, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_53A_Type = MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_53A_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_53A_Type', MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_53A_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_53J_Type with content type SIMPLE
class MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_53J_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_53J_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_53J_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_53J_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 398, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_53J_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_53J_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='53J')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 401, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 401, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_53J_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 402, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 402, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_53J_Type = MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_53J_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_53J_Type', MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_53J_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_56A_Type with content type SIMPLE
class MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_56A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_56A_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_56A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_56A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 411, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_56A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_56A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='56A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 414, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 414, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_56A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 415, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 415, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_56A_Type = MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_56A_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_56A_Type', MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_56A_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_56J_Type with content type SIMPLE
class MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_56J_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_56J_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_56J_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_56J_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 424, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_56J_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_56J_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='56J')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 427, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 427, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_56J_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 428, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 428, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_56J_Type = MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_56J_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_56J_Type', MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_56J_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_57A_Type with content type SIMPLE
class MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_57A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_57A_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_57A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_57A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 437, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_57A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_57A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='57A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 440, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 440, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_57A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 441, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 441, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_57A_Type = MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_57A_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_57A_Type', MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_57A_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_57J_Type with content type SIMPLE
class MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_57J_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_57J_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_57J_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_57J_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 450, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_57J_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_57J_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='57J')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 453, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 453, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_57J_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 454, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 454, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_57J_Type = MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_57J_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_57J_Type', MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_57J_Type)


# Complex type {http://www.w3schools.com}MT300_SubSequenceB2_AmountSold_33B_Type with content type SIMPLE
class MT300_SubSequenceB2_AmountSold_33B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SubSequenceB2_AmountSold_33B_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SubSequenceB2_AmountSold_33B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SubSequenceB2_AmountSold_33B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 463, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SubSequenceB2_AmountSold_33B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SubSequenceB2_AmountSold_33B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='33B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 466, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 466, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SubSequenceB2_AmountSold_33B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 467, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 467, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SubSequenceB2_AmountSold_33B_Type = MT300_SubSequenceB2_AmountSold_33B_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SubSequenceB2_AmountSold_33B_Type', MT300_SubSequenceB2_AmountSold_33B_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_53A_Type with content type SIMPLE
class MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_53A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_53A_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_53A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_53A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 476, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_53A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_53A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='53A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 479, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 479, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_53A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 480, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 480, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_53A_Type = MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_53A_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_53A_Type', MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_53A_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_53J_Type with content type SIMPLE
class MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_53J_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_53J_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_53J_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_53J_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 489, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_53J_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_53J_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='53J')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 492, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 492, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_53J_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 493, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 493, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_53J_Type = MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_53J_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_53J_Type', MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_53J_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_56A_Type with content type SIMPLE
class MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_56A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_56A_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_56A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_56A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 502, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_56A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_56A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='56A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 505, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 505, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_56A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 506, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 506, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_56A_Type = MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_56A_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_56A_Type', MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_56A_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_56J_Type with content type SIMPLE
class MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_56J_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_56J_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_56J_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_56J_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 515, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_56J_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_56J_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='56J')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 518, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 518, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_56J_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 519, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 519, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_56J_Type = MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_56J_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_56J_Type', MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_56J_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_57A_Type with content type SIMPLE
class MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_57A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_57A_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_57A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_57A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 528, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_57A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_57A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='57A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 531, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 531, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_57A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 532, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 532, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_57A_Type = MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_57A_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_57A_Type', MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_57A_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_57J_Type with content type SIMPLE
class MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_57J_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_57J_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_57J_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_57J_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 541, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_57J_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_57J_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='57J')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 544, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 544, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_57J_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 545, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 545, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_57J_Type = MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_57J_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_57J_Type', MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_57J_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_58A_Type with content type SIMPLE
class MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_58A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_58A_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_58A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_58A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 554, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_58A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_58A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='58A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 557, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 557, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_58A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 558, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 558, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_58A_Type = MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_58A_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_58A_Type', MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_58A_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_58J_Type with content type SIMPLE
class MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_58J_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_58J_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_58J_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_58J_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 567, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_58J_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_58J_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='58J')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 570, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 570, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_58J_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 571, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 571, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_58J_Type = MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_58J_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_58J_Type', MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_58J_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceC_OptionalGeneralInformation_29A_Type with content type SIMPLE
class MT300_SequenceC_OptionalGeneralInformation_29A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceC_OptionalGeneralInformation_29A_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceC_OptionalGeneralInformation_29A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceC_OptionalGeneralInformation_29A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 580, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceC_OptionalGeneralInformation_29A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceC_OptionalGeneralInformation_29A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='29A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 583, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 583, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceC_OptionalGeneralInformation_29A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 584, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 584, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceC_OptionalGeneralInformation_29A_Type = MT300_SequenceC_OptionalGeneralInformation_29A_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceC_OptionalGeneralInformation_29A_Type', MT300_SequenceC_OptionalGeneralInformation_29A_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceC_OptionalGeneralInformation_24D_Type with content type SIMPLE
class MT300_SequenceC_OptionalGeneralInformation_24D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceC_OptionalGeneralInformation_24D_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceC_OptionalGeneralInformation_24D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceC_OptionalGeneralInformation_24D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 593, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceC_OptionalGeneralInformation_24D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceC_OptionalGeneralInformation_24D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='24D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 596, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 596, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceC_OptionalGeneralInformation_24D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 597, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 597, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceC_OptionalGeneralInformation_24D_Type = MT300_SequenceC_OptionalGeneralInformation_24D_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceC_OptionalGeneralInformation_24D_Type', MT300_SequenceC_OptionalGeneralInformation_24D_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceC_OptionalGeneralInformation_84A_Type with content type SIMPLE
class MT300_SequenceC_OptionalGeneralInformation_84A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceC_OptionalGeneralInformation_84A_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceC_OptionalGeneralInformation_84A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceC_OptionalGeneralInformation_84A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 606, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceC_OptionalGeneralInformation_84A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceC_OptionalGeneralInformation_84A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='84A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 609, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 609, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceC_OptionalGeneralInformation_84A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 610, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 610, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceC_OptionalGeneralInformation_84A_Type = MT300_SequenceC_OptionalGeneralInformation_84A_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceC_OptionalGeneralInformation_84A_Type', MT300_SequenceC_OptionalGeneralInformation_84A_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceC_OptionalGeneralInformation_84B_Type with content type SIMPLE
class MT300_SequenceC_OptionalGeneralInformation_84B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceC_OptionalGeneralInformation_84B_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceC_OptionalGeneralInformation_84B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceC_OptionalGeneralInformation_84B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 619, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceC_OptionalGeneralInformation_84B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceC_OptionalGeneralInformation_84B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='84B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 622, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 622, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceC_OptionalGeneralInformation_84B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 623, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 623, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceC_OptionalGeneralInformation_84B_Type = MT300_SequenceC_OptionalGeneralInformation_84B_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceC_OptionalGeneralInformation_84B_Type', MT300_SequenceC_OptionalGeneralInformation_84B_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceC_OptionalGeneralInformation_84D_Type with content type SIMPLE
class MT300_SequenceC_OptionalGeneralInformation_84D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceC_OptionalGeneralInformation_84D_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceC_OptionalGeneralInformation_84D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceC_OptionalGeneralInformation_84D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 632, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceC_OptionalGeneralInformation_84D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceC_OptionalGeneralInformation_84D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='84D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 635, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 635, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceC_OptionalGeneralInformation_84D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 636, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 636, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceC_OptionalGeneralInformation_84D_Type = MT300_SequenceC_OptionalGeneralInformation_84D_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceC_OptionalGeneralInformation_84D_Type', MT300_SequenceC_OptionalGeneralInformation_84D_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceC_OptionalGeneralInformation_84J_Type with content type SIMPLE
class MT300_SequenceC_OptionalGeneralInformation_84J_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceC_OptionalGeneralInformation_84J_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceC_OptionalGeneralInformation_84J_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceC_OptionalGeneralInformation_84J_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 645, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceC_OptionalGeneralInformation_84J_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceC_OptionalGeneralInformation_84J_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='84J')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 648, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 648, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceC_OptionalGeneralInformation_84J_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 649, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 649, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceC_OptionalGeneralInformation_84J_Type = MT300_SequenceC_OptionalGeneralInformation_84J_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceC_OptionalGeneralInformation_84J_Type', MT300_SequenceC_OptionalGeneralInformation_84J_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceC_OptionalGeneralInformation_85A_Type with content type SIMPLE
class MT300_SequenceC_OptionalGeneralInformation_85A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceC_OptionalGeneralInformation_85A_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceC_OptionalGeneralInformation_85A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceC_OptionalGeneralInformation_85A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 658, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceC_OptionalGeneralInformation_85A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceC_OptionalGeneralInformation_85A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='85A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 661, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 661, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceC_OptionalGeneralInformation_85A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 662, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 662, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceC_OptionalGeneralInformation_85A_Type = MT300_SequenceC_OptionalGeneralInformation_85A_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceC_OptionalGeneralInformation_85A_Type', MT300_SequenceC_OptionalGeneralInformation_85A_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceC_OptionalGeneralInformation_85B_Type with content type SIMPLE
class MT300_SequenceC_OptionalGeneralInformation_85B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceC_OptionalGeneralInformation_85B_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceC_OptionalGeneralInformation_85B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceC_OptionalGeneralInformation_85B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 671, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceC_OptionalGeneralInformation_85B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceC_OptionalGeneralInformation_85B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='85B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 674, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 674, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceC_OptionalGeneralInformation_85B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 675, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 675, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceC_OptionalGeneralInformation_85B_Type = MT300_SequenceC_OptionalGeneralInformation_85B_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceC_OptionalGeneralInformation_85B_Type', MT300_SequenceC_OptionalGeneralInformation_85B_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceC_OptionalGeneralInformation_85D_Type with content type SIMPLE
class MT300_SequenceC_OptionalGeneralInformation_85D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceC_OptionalGeneralInformation_85D_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceC_OptionalGeneralInformation_85D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceC_OptionalGeneralInformation_85D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 684, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceC_OptionalGeneralInformation_85D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceC_OptionalGeneralInformation_85D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='85D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 687, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 687, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceC_OptionalGeneralInformation_85D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 688, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 688, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceC_OptionalGeneralInformation_85D_Type = MT300_SequenceC_OptionalGeneralInformation_85D_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceC_OptionalGeneralInformation_85D_Type', MT300_SequenceC_OptionalGeneralInformation_85D_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceC_OptionalGeneralInformation_85J_Type with content type SIMPLE
class MT300_SequenceC_OptionalGeneralInformation_85J_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceC_OptionalGeneralInformation_85J_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceC_OptionalGeneralInformation_85J_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceC_OptionalGeneralInformation_85J_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 697, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceC_OptionalGeneralInformation_85J_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceC_OptionalGeneralInformation_85J_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='85J')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 700, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 700, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceC_OptionalGeneralInformation_85J_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 701, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 701, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceC_OptionalGeneralInformation_85J_Type = MT300_SequenceC_OptionalGeneralInformation_85J_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceC_OptionalGeneralInformation_85J_Type', MT300_SequenceC_OptionalGeneralInformation_85J_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceC_OptionalGeneralInformation_88A_Type with content type SIMPLE
class MT300_SequenceC_OptionalGeneralInformation_88A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceC_OptionalGeneralInformation_88A_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceC_OptionalGeneralInformation_88A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceC_OptionalGeneralInformation_88A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 710, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceC_OptionalGeneralInformation_88A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceC_OptionalGeneralInformation_88A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='88A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 713, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 713, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceC_OptionalGeneralInformation_88A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 714, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 714, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceC_OptionalGeneralInformation_88A_Type = MT300_SequenceC_OptionalGeneralInformation_88A_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceC_OptionalGeneralInformation_88A_Type', MT300_SequenceC_OptionalGeneralInformation_88A_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceC_OptionalGeneralInformation_88D_Type with content type SIMPLE
class MT300_SequenceC_OptionalGeneralInformation_88D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceC_OptionalGeneralInformation_88D_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceC_OptionalGeneralInformation_88D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceC_OptionalGeneralInformation_88D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 723, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceC_OptionalGeneralInformation_88D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceC_OptionalGeneralInformation_88D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='88D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 726, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 726, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceC_OptionalGeneralInformation_88D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 727, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 727, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceC_OptionalGeneralInformation_88D_Type = MT300_SequenceC_OptionalGeneralInformation_88D_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceC_OptionalGeneralInformation_88D_Type', MT300_SequenceC_OptionalGeneralInformation_88D_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceC_OptionalGeneralInformation_88J_Type with content type SIMPLE
class MT300_SequenceC_OptionalGeneralInformation_88J_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceC_OptionalGeneralInformation_88J_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceC_OptionalGeneralInformation_88J_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceC_OptionalGeneralInformation_88J_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 736, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceC_OptionalGeneralInformation_88J_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceC_OptionalGeneralInformation_88J_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='88J')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 739, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 739, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceC_OptionalGeneralInformation_88J_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 740, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 740, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceC_OptionalGeneralInformation_88J_Type = MT300_SequenceC_OptionalGeneralInformation_88J_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceC_OptionalGeneralInformation_88J_Type', MT300_SequenceC_OptionalGeneralInformation_88J_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceC_OptionalGeneralInformation_71F_Type with content type SIMPLE
class MT300_SequenceC_OptionalGeneralInformation_71F_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceC_OptionalGeneralInformation_71F_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceC_OptionalGeneralInformation_71F_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceC_OptionalGeneralInformation_71F_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 749, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceC_OptionalGeneralInformation_71F_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceC_OptionalGeneralInformation_71F_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='71F')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 752, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 752, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceC_OptionalGeneralInformation_71F_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 753, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 753, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceC_OptionalGeneralInformation_71F_Type = MT300_SequenceC_OptionalGeneralInformation_71F_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceC_OptionalGeneralInformation_71F_Type', MT300_SequenceC_OptionalGeneralInformation_71F_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceC_OptionalGeneralInformation_26H_Type with content type SIMPLE
class MT300_SequenceC_OptionalGeneralInformation_26H_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceC_OptionalGeneralInformation_26H_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceC_OptionalGeneralInformation_26H_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceC_OptionalGeneralInformation_26H_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 762, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceC_OptionalGeneralInformation_26H_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceC_OptionalGeneralInformation_26H_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='26H')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 765, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 765, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceC_OptionalGeneralInformation_26H_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 766, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 766, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceC_OptionalGeneralInformation_26H_Type = MT300_SequenceC_OptionalGeneralInformation_26H_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceC_OptionalGeneralInformation_26H_Type', MT300_SequenceC_OptionalGeneralInformation_26H_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceC_OptionalGeneralInformation_21G_Type with content type SIMPLE
class MT300_SequenceC_OptionalGeneralInformation_21G_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceC_OptionalGeneralInformation_21G_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceC_OptionalGeneralInformation_21G_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceC_OptionalGeneralInformation_21G_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 775, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceC_OptionalGeneralInformation_21G_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceC_OptionalGeneralInformation_21G_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='21G')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 778, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 778, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceC_OptionalGeneralInformation_21G_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 779, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 779, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceC_OptionalGeneralInformation_21G_Type = MT300_SequenceC_OptionalGeneralInformation_21G_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceC_OptionalGeneralInformation_21G_Type', MT300_SequenceC_OptionalGeneralInformation_21G_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceC_OptionalGeneralInformation_72_Type with content type SIMPLE
class MT300_SequenceC_OptionalGeneralInformation_72_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceC_OptionalGeneralInformation_72_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceC_OptionalGeneralInformation_72_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceC_OptionalGeneralInformation_72_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 788, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceC_OptionalGeneralInformation_72_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceC_OptionalGeneralInformation_72_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='72')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 791, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 791, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceC_OptionalGeneralInformation_72_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 792, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 792, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceC_OptionalGeneralInformation_72_Type = MT300_SequenceC_OptionalGeneralInformation_72_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceC_OptionalGeneralInformation_72_Type', MT300_SequenceC_OptionalGeneralInformation_72_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceD_SplitSettlementDetails_SettlementDetails_17A_Type with content type SIMPLE
class MT300_SequenceD_SplitSettlementDetails_SettlementDetails_17A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceD_SplitSettlementDetails_SettlementDetails_17A_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceD_SplitSettlementDetails_SettlementDetails_17A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceD_SplitSettlementDetails_SettlementDetails_17A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 801, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceD_SplitSettlementDetails_SettlementDetails_17A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceD_SplitSettlementDetails_SettlementDetails_17A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='17A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 804, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 804, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceD_SplitSettlementDetails_SettlementDetails_17A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 805, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 805, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceD_SplitSettlementDetails_SettlementDetails_17A_Type = MT300_SequenceD_SplitSettlementDetails_SettlementDetails_17A_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceD_SplitSettlementDetails_SettlementDetails_17A_Type', MT300_SequenceD_SplitSettlementDetails_SettlementDetails_17A_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceD_SplitSettlementDetails_SettlementDetails_32B_Type with content type SIMPLE
class MT300_SequenceD_SplitSettlementDetails_SettlementDetails_32B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceD_SplitSettlementDetails_SettlementDetails_32B_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceD_SplitSettlementDetails_SettlementDetails_32B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceD_SplitSettlementDetails_SettlementDetails_32B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 814, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceD_SplitSettlementDetails_SettlementDetails_32B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceD_SplitSettlementDetails_SettlementDetails_32B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='32B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 817, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 817, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceD_SplitSettlementDetails_SettlementDetails_32B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 818, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 818, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceD_SplitSettlementDetails_SettlementDetails_32B_Type = MT300_SequenceD_SplitSettlementDetails_SettlementDetails_32B_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceD_SplitSettlementDetails_SettlementDetails_32B_Type', MT300_SequenceD_SplitSettlementDetails_SettlementDetails_32B_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceD_SplitSettlementDetails_SettlementDetails_53A_Type with content type SIMPLE
class MT300_SequenceD_SplitSettlementDetails_SettlementDetails_53A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceD_SplitSettlementDetails_SettlementDetails_53A_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceD_SplitSettlementDetails_SettlementDetails_53A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceD_SplitSettlementDetails_SettlementDetails_53A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 827, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceD_SplitSettlementDetails_SettlementDetails_53A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceD_SplitSettlementDetails_SettlementDetails_53A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='53A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 830, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 830, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceD_SplitSettlementDetails_SettlementDetails_53A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 831, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 831, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceD_SplitSettlementDetails_SettlementDetails_53A_Type = MT300_SequenceD_SplitSettlementDetails_SettlementDetails_53A_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceD_SplitSettlementDetails_SettlementDetails_53A_Type', MT300_SequenceD_SplitSettlementDetails_SettlementDetails_53A_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceD_SplitSettlementDetails_SettlementDetails_53D_Type with content type SIMPLE
class MT300_SequenceD_SplitSettlementDetails_SettlementDetails_53D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceD_SplitSettlementDetails_SettlementDetails_53D_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceD_SplitSettlementDetails_SettlementDetails_53D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceD_SplitSettlementDetails_SettlementDetails_53D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 840, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceD_SplitSettlementDetails_SettlementDetails_53D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceD_SplitSettlementDetails_SettlementDetails_53D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='53D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 843, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 843, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceD_SplitSettlementDetails_SettlementDetails_53D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 844, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 844, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceD_SplitSettlementDetails_SettlementDetails_53D_Type = MT300_SequenceD_SplitSettlementDetails_SettlementDetails_53D_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceD_SplitSettlementDetails_SettlementDetails_53D_Type', MT300_SequenceD_SplitSettlementDetails_SettlementDetails_53D_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceD_SplitSettlementDetails_SettlementDetails_53J_Type with content type SIMPLE
class MT300_SequenceD_SplitSettlementDetails_SettlementDetails_53J_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceD_SplitSettlementDetails_SettlementDetails_53J_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceD_SplitSettlementDetails_SettlementDetails_53J_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceD_SplitSettlementDetails_SettlementDetails_53J_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 853, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceD_SplitSettlementDetails_SettlementDetails_53J_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceD_SplitSettlementDetails_SettlementDetails_53J_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='53J')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 856, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 856, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceD_SplitSettlementDetails_SettlementDetails_53J_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 857, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 857, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceD_SplitSettlementDetails_SettlementDetails_53J_Type = MT300_SequenceD_SplitSettlementDetails_SettlementDetails_53J_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceD_SplitSettlementDetails_SettlementDetails_53J_Type', MT300_SequenceD_SplitSettlementDetails_SettlementDetails_53J_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceD_SplitSettlementDetails_SettlementDetails_56A_Type with content type SIMPLE
class MT300_SequenceD_SplitSettlementDetails_SettlementDetails_56A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceD_SplitSettlementDetails_SettlementDetails_56A_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceD_SplitSettlementDetails_SettlementDetails_56A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceD_SplitSettlementDetails_SettlementDetails_56A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 866, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceD_SplitSettlementDetails_SettlementDetails_56A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceD_SplitSettlementDetails_SettlementDetails_56A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='56A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 869, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 869, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceD_SplitSettlementDetails_SettlementDetails_56A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 870, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 870, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceD_SplitSettlementDetails_SettlementDetails_56A_Type = MT300_SequenceD_SplitSettlementDetails_SettlementDetails_56A_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceD_SplitSettlementDetails_SettlementDetails_56A_Type', MT300_SequenceD_SplitSettlementDetails_SettlementDetails_56A_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceD_SplitSettlementDetails_SettlementDetails_56D_Type with content type SIMPLE
class MT300_SequenceD_SplitSettlementDetails_SettlementDetails_56D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceD_SplitSettlementDetails_SettlementDetails_56D_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceD_SplitSettlementDetails_SettlementDetails_56D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceD_SplitSettlementDetails_SettlementDetails_56D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 879, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceD_SplitSettlementDetails_SettlementDetails_56D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceD_SplitSettlementDetails_SettlementDetails_56D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='56D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 882, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 882, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceD_SplitSettlementDetails_SettlementDetails_56D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 883, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 883, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceD_SplitSettlementDetails_SettlementDetails_56D_Type = MT300_SequenceD_SplitSettlementDetails_SettlementDetails_56D_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceD_SplitSettlementDetails_SettlementDetails_56D_Type', MT300_SequenceD_SplitSettlementDetails_SettlementDetails_56D_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceD_SplitSettlementDetails_SettlementDetails_56J_Type with content type SIMPLE
class MT300_SequenceD_SplitSettlementDetails_SettlementDetails_56J_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceD_SplitSettlementDetails_SettlementDetails_56J_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceD_SplitSettlementDetails_SettlementDetails_56J_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceD_SplitSettlementDetails_SettlementDetails_56J_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 892, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceD_SplitSettlementDetails_SettlementDetails_56J_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceD_SplitSettlementDetails_SettlementDetails_56J_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='56J')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 895, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 895, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceD_SplitSettlementDetails_SettlementDetails_56J_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 896, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 896, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceD_SplitSettlementDetails_SettlementDetails_56J_Type = MT300_SequenceD_SplitSettlementDetails_SettlementDetails_56J_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceD_SplitSettlementDetails_SettlementDetails_56J_Type', MT300_SequenceD_SplitSettlementDetails_SettlementDetails_56J_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceD_SplitSettlementDetails_SettlementDetails_57A_Type with content type SIMPLE
class MT300_SequenceD_SplitSettlementDetails_SettlementDetails_57A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceD_SplitSettlementDetails_SettlementDetails_57A_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceD_SplitSettlementDetails_SettlementDetails_57A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceD_SplitSettlementDetails_SettlementDetails_57A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 905, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceD_SplitSettlementDetails_SettlementDetails_57A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceD_SplitSettlementDetails_SettlementDetails_57A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='57A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 908, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 908, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceD_SplitSettlementDetails_SettlementDetails_57A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 909, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 909, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceD_SplitSettlementDetails_SettlementDetails_57A_Type = MT300_SequenceD_SplitSettlementDetails_SettlementDetails_57A_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceD_SplitSettlementDetails_SettlementDetails_57A_Type', MT300_SequenceD_SplitSettlementDetails_SettlementDetails_57A_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceD_SplitSettlementDetails_SettlementDetails_57D_Type with content type SIMPLE
class MT300_SequenceD_SplitSettlementDetails_SettlementDetails_57D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceD_SplitSettlementDetails_SettlementDetails_57D_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceD_SplitSettlementDetails_SettlementDetails_57D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceD_SplitSettlementDetails_SettlementDetails_57D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 918, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceD_SplitSettlementDetails_SettlementDetails_57D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceD_SplitSettlementDetails_SettlementDetails_57D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='57D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 921, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 921, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceD_SplitSettlementDetails_SettlementDetails_57D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 922, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 922, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceD_SplitSettlementDetails_SettlementDetails_57D_Type = MT300_SequenceD_SplitSettlementDetails_SettlementDetails_57D_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceD_SplitSettlementDetails_SettlementDetails_57D_Type', MT300_SequenceD_SplitSettlementDetails_SettlementDetails_57D_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceD_SplitSettlementDetails_SettlementDetails_57J_Type with content type SIMPLE
class MT300_SequenceD_SplitSettlementDetails_SettlementDetails_57J_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceD_SplitSettlementDetails_SettlementDetails_57J_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceD_SplitSettlementDetails_SettlementDetails_57J_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceD_SplitSettlementDetails_SettlementDetails_57J_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 931, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceD_SplitSettlementDetails_SettlementDetails_57J_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceD_SplitSettlementDetails_SettlementDetails_57J_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='57J')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 934, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 934, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceD_SplitSettlementDetails_SettlementDetails_57J_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 935, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 935, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceD_SplitSettlementDetails_SettlementDetails_57J_Type = MT300_SequenceD_SplitSettlementDetails_SettlementDetails_57J_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceD_SplitSettlementDetails_SettlementDetails_57J_Type', MT300_SequenceD_SplitSettlementDetails_SettlementDetails_57J_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceD_SplitSettlementDetails_SettlementDetails_58A_Type with content type SIMPLE
class MT300_SequenceD_SplitSettlementDetails_SettlementDetails_58A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceD_SplitSettlementDetails_SettlementDetails_58A_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceD_SplitSettlementDetails_SettlementDetails_58A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceD_SplitSettlementDetails_SettlementDetails_58A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 944, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceD_SplitSettlementDetails_SettlementDetails_58A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceD_SplitSettlementDetails_SettlementDetails_58A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='58A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 947, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 947, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceD_SplitSettlementDetails_SettlementDetails_58A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 948, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 948, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceD_SplitSettlementDetails_SettlementDetails_58A_Type = MT300_SequenceD_SplitSettlementDetails_SettlementDetails_58A_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceD_SplitSettlementDetails_SettlementDetails_58A_Type', MT300_SequenceD_SplitSettlementDetails_SettlementDetails_58A_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceD_SplitSettlementDetails_SettlementDetails_58D_Type with content type SIMPLE
class MT300_SequenceD_SplitSettlementDetails_SettlementDetails_58D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceD_SplitSettlementDetails_SettlementDetails_58D_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceD_SplitSettlementDetails_SettlementDetails_58D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceD_SplitSettlementDetails_SettlementDetails_58D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 957, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceD_SplitSettlementDetails_SettlementDetails_58D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceD_SplitSettlementDetails_SettlementDetails_58D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='58D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 960, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 960, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceD_SplitSettlementDetails_SettlementDetails_58D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 961, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 961, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceD_SplitSettlementDetails_SettlementDetails_58D_Type = MT300_SequenceD_SplitSettlementDetails_SettlementDetails_58D_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceD_SplitSettlementDetails_SettlementDetails_58D_Type', MT300_SequenceD_SplitSettlementDetails_SettlementDetails_58D_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceD_SplitSettlementDetails_SettlementDetails_58J_Type with content type SIMPLE
class MT300_SequenceD_SplitSettlementDetails_SettlementDetails_58J_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceD_SplitSettlementDetails_SettlementDetails_58J_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceD_SplitSettlementDetails_SettlementDetails_58J_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceD_SplitSettlementDetails_SettlementDetails_58J_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 970, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceD_SplitSettlementDetails_SettlementDetails_58J_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceD_SplitSettlementDetails_SettlementDetails_58J_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='58J')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 973, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 973, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceD_SplitSettlementDetails_SettlementDetails_58J_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 974, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 974, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceD_SplitSettlementDetails_SettlementDetails_58J_Type = MT300_SequenceD_SplitSettlementDetails_SettlementDetails_58J_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceD_SplitSettlementDetails_SettlementDetails_58J_Type', MT300_SequenceD_SplitSettlementDetails_SettlementDetails_58J_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceD_SplitSettlementDetails_16A_Type with content type SIMPLE
class MT300_SequenceD_SplitSettlementDetails_16A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceD_SplitSettlementDetails_16A_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceD_SplitSettlementDetails_16A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceD_SplitSettlementDetails_16A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 983, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceD_SplitSettlementDetails_16A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceD_SplitSettlementDetails_16A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='16A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 986, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 986, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceD_SplitSettlementDetails_16A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 987, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 987, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceD_SplitSettlementDetails_16A_Type = MT300_SequenceD_SplitSettlementDetails_16A_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceD_SplitSettlementDetails_16A_Type', MT300_SequenceD_SplitSettlementDetails_16A_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_22L_Type with content type SIMPLE
class MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_22L_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_22L_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_22L_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_22L_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 996, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_22L_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_22L_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='22L')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 999, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 999, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_22L_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1000, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1000, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_22L_Type = MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_22L_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_22L_Type', MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_22L_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_91A_Type with content type SIMPLE
class MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_91A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_91A_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_91A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_91A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1009, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_91A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_91A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='91A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1012, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1012, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_91A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1013, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1013, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_91A_Type = MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_91A_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_91A_Type', MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_91A_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_91D_Type with content type SIMPLE
class MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_91D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_91D_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_91D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_91D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1022, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_91D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_91D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='91D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1025, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1025, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_91D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1026, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1026, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_91D_Type = MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_91D_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_91D_Type', MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_91D_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_91J_Type with content type SIMPLE
class MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_91J_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_91J_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_91J_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_91J_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1035, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_91J_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_91J_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='91J')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1038, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1038, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_91J_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1039, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1039, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_91J_Type = MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_91J_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_91J_Type', MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_91J_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_22M_Type with content type SIMPLE
class MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_22M_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_22M_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_22M_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_22M_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1048, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_22M_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_22M_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='22M')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1051, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1051, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_22M_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1052, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1052, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_22M_Type = MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_22M_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_22M_Type', MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_22M_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_22N_Type with content type SIMPLE
class MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_22N_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_22N_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_22N_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_22N_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1061, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_22N_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_22N_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='22N')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1064, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1064, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_22N_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1065, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1065, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_22N_Type = MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_22N_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_22N_Type', MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_22N_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_SubSequenceE1a1_PriorUniqueTransactionIdentifier_22P_Type with content type SIMPLE
class MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_SubSequenceE1a1_PriorUniqueTransactionIdentifier_22P_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_SubSequenceE1a1_PriorUniqueTransactionIdentifier_22P_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_SubSequenceE1a1_PriorUniqueTransactionIdentifier_22P_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_SubSequenceE1a1_PriorUniqueTransactionIdentifier_22P_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1074, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_SubSequenceE1a1_PriorUniqueTransactionIdentifier_22P_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_SubSequenceE1a1_PriorUniqueTransactionIdentifier_22P_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='22P')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1077, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1077, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_SubSequenceE1a1_PriorUniqueTransactionIdentifier_22P_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1078, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1078, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_SubSequenceE1a1_PriorUniqueTransactionIdentifier_22P_Type = MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_SubSequenceE1a1_PriorUniqueTransactionIdentifier_22P_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_SubSequenceE1a1_PriorUniqueTransactionIdentifier_22P_Type', MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_SubSequenceE1a1_PriorUniqueTransactionIdentifier_22P_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_SubSequenceE1a1_PriorUniqueTransactionIdentifier_22R_Type with content type SIMPLE
class MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_SubSequenceE1a1_PriorUniqueTransactionIdentifier_22R_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_SubSequenceE1a1_PriorUniqueTransactionIdentifier_22R_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_SubSequenceE1a1_PriorUniqueTransactionIdentifier_22R_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_SubSequenceE1a1_PriorUniqueTransactionIdentifier_22R_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1087, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_SubSequenceE1a1_PriorUniqueTransactionIdentifier_22R_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_SubSequenceE1a1_PriorUniqueTransactionIdentifier_22R_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='22R')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1090, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1090, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_SubSequenceE1a1_PriorUniqueTransactionIdentifier_22R_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1091, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1091, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_SubSequenceE1a1_PriorUniqueTransactionIdentifier_22R_Type = MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_SubSequenceE1a1_PriorUniqueTransactionIdentifier_22R_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_SubSequenceE1a1_PriorUniqueTransactionIdentifier_22R_Type', MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_SubSequenceE1a1_PriorUniqueTransactionIdentifier_22R_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_81A_Type with content type SIMPLE
class MT300_SequenceE_ReportingInformation_81A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_81A_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceE_ReportingInformation_81A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceE_ReportingInformation_81A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1100, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceE_ReportingInformation_81A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_81A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='81A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1103, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1103, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_81A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1104, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1104, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceE_ReportingInformation_81A_Type = MT300_SequenceE_ReportingInformation_81A_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceE_ReportingInformation_81A_Type', MT300_SequenceE_ReportingInformation_81A_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_81D_Type with content type SIMPLE
class MT300_SequenceE_ReportingInformation_81D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_81D_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceE_ReportingInformation_81D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceE_ReportingInformation_81D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1113, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceE_ReportingInformation_81D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_81D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='81D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1116, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1116, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_81D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1117, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1117, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceE_ReportingInformation_81D_Type = MT300_SequenceE_ReportingInformation_81D_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceE_ReportingInformation_81D_Type', MT300_SequenceE_ReportingInformation_81D_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_81J_Type with content type SIMPLE
class MT300_SequenceE_ReportingInformation_81J_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_81J_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceE_ReportingInformation_81J_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceE_ReportingInformation_81J_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1126, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceE_ReportingInformation_81J_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_81J_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='81J')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1129, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1129, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_81J_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1130, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1130, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceE_ReportingInformation_81J_Type = MT300_SequenceE_ReportingInformation_81J_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceE_ReportingInformation_81J_Type', MT300_SequenceE_ReportingInformation_81J_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_89A_Type with content type SIMPLE
class MT300_SequenceE_ReportingInformation_89A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_89A_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceE_ReportingInformation_89A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceE_ReportingInformation_89A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1139, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceE_ReportingInformation_89A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_89A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='89A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1142, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1142, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_89A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1143, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1143, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceE_ReportingInformation_89A_Type = MT300_SequenceE_ReportingInformation_89A_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceE_ReportingInformation_89A_Type', MT300_SequenceE_ReportingInformation_89A_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_89D_Type with content type SIMPLE
class MT300_SequenceE_ReportingInformation_89D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_89D_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceE_ReportingInformation_89D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceE_ReportingInformation_89D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1152, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceE_ReportingInformation_89D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_89D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='89D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1155, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1155, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_89D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1156, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1156, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceE_ReportingInformation_89D_Type = MT300_SequenceE_ReportingInformation_89D_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceE_ReportingInformation_89D_Type', MT300_SequenceE_ReportingInformation_89D_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_89J_Type with content type SIMPLE
class MT300_SequenceE_ReportingInformation_89J_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_89J_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceE_ReportingInformation_89J_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceE_ReportingInformation_89J_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1165, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceE_ReportingInformation_89J_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_89J_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='89J')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1168, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1168, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_89J_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1169, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1169, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceE_ReportingInformation_89J_Type = MT300_SequenceE_ReportingInformation_89J_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceE_ReportingInformation_89J_Type', MT300_SequenceE_ReportingInformation_89J_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_96A_Type with content type SIMPLE
class MT300_SequenceE_ReportingInformation_96A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_96A_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceE_ReportingInformation_96A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceE_ReportingInformation_96A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1178, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceE_ReportingInformation_96A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_96A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='96A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1181, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1181, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_96A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1182, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1182, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceE_ReportingInformation_96A_Type = MT300_SequenceE_ReportingInformation_96A_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceE_ReportingInformation_96A_Type', MT300_SequenceE_ReportingInformation_96A_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_96D_Type with content type SIMPLE
class MT300_SequenceE_ReportingInformation_96D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_96D_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceE_ReportingInformation_96D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceE_ReportingInformation_96D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1191, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceE_ReportingInformation_96D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_96D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='96D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1194, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1194, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_96D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1195, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1195, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceE_ReportingInformation_96D_Type = MT300_SequenceE_ReportingInformation_96D_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceE_ReportingInformation_96D_Type', MT300_SequenceE_ReportingInformation_96D_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_96J_Type with content type SIMPLE
class MT300_SequenceE_ReportingInformation_96J_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_96J_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceE_ReportingInformation_96J_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceE_ReportingInformation_96J_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1204, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceE_ReportingInformation_96J_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_96J_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='96J')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1207, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1207, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_96J_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1208, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1208, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceE_ReportingInformation_96J_Type = MT300_SequenceE_ReportingInformation_96J_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceE_ReportingInformation_96J_Type', MT300_SequenceE_ReportingInformation_96J_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_22S_Type with content type SIMPLE
class MT300_SequenceE_ReportingInformation_22S_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_22S_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceE_ReportingInformation_22S_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceE_ReportingInformation_22S_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1217, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceE_ReportingInformation_22S_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_22S_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='22S')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1220, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1220, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_22S_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1221, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1221, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceE_ReportingInformation_22S_Type = MT300_SequenceE_ReportingInformation_22S_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceE_ReportingInformation_22S_Type', MT300_SequenceE_ReportingInformation_22S_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_22T_Type with content type SIMPLE
class MT300_SequenceE_ReportingInformation_22T_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_22T_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceE_ReportingInformation_22T_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceE_ReportingInformation_22T_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1230, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceE_ReportingInformation_22T_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_22T_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='22T')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1233, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1233, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_22T_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1234, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1234, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceE_ReportingInformation_22T_Type = MT300_SequenceE_ReportingInformation_22T_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceE_ReportingInformation_22T_Type', MT300_SequenceE_ReportingInformation_22T_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_17E_Type with content type SIMPLE
class MT300_SequenceE_ReportingInformation_17E_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_17E_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceE_ReportingInformation_17E_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceE_ReportingInformation_17E_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1243, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceE_ReportingInformation_17E_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_17E_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='17E')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1246, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1246, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_17E_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1247, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1247, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceE_ReportingInformation_17E_Type = MT300_SequenceE_ReportingInformation_17E_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceE_ReportingInformation_17E_Type', MT300_SequenceE_ReportingInformation_17E_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_22U_Type with content type SIMPLE
class MT300_SequenceE_ReportingInformation_22U_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_22U_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceE_ReportingInformation_22U_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceE_ReportingInformation_22U_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1256, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceE_ReportingInformation_22U_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_22U_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='22U')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1259, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1259, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_22U_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1260, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1260, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceE_ReportingInformation_22U_Type = MT300_SequenceE_ReportingInformation_22U_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceE_ReportingInformation_22U_Type', MT300_SequenceE_ReportingInformation_22U_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_35B_Type with content type SIMPLE
class MT300_SequenceE_ReportingInformation_35B_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_35B_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceE_ReportingInformation_35B_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceE_ReportingInformation_35B_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1269, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceE_ReportingInformation_35B_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_35B_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='35B')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1272, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1272, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_35B_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1273, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1273, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceE_ReportingInformation_35B_Type = MT300_SequenceE_ReportingInformation_35B_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceE_ReportingInformation_35B_Type', MT300_SequenceE_ReportingInformation_35B_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_17H_Type with content type SIMPLE
class MT300_SequenceE_ReportingInformation_17H_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_17H_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceE_ReportingInformation_17H_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceE_ReportingInformation_17H_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1282, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceE_ReportingInformation_17H_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_17H_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='17H')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1285, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1285, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_17H_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1286, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1286, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceE_ReportingInformation_17H_Type = MT300_SequenceE_ReportingInformation_17H_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceE_ReportingInformation_17H_Type', MT300_SequenceE_ReportingInformation_17H_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_17P_Type with content type SIMPLE
class MT300_SequenceE_ReportingInformation_17P_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_17P_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceE_ReportingInformation_17P_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceE_ReportingInformation_17P_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1295, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceE_ReportingInformation_17P_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_17P_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='17P')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1298, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1298, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_17P_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1299, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1299, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceE_ReportingInformation_17P_Type = MT300_SequenceE_ReportingInformation_17P_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceE_ReportingInformation_17P_Type', MT300_SequenceE_ReportingInformation_17P_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_22V_Type with content type SIMPLE
class MT300_SequenceE_ReportingInformation_22V_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_22V_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceE_ReportingInformation_22V_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceE_ReportingInformation_22V_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1308, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceE_ReportingInformation_22V_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_22V_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='22V')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1311, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1311, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_22V_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1312, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1312, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceE_ReportingInformation_22V_Type = MT300_SequenceE_ReportingInformation_22V_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceE_ReportingInformation_22V_Type', MT300_SequenceE_ReportingInformation_22V_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_98D_Type with content type SIMPLE
class MT300_SequenceE_ReportingInformation_98D_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_98D_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceE_ReportingInformation_98D_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceE_ReportingInformation_98D_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1321, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceE_ReportingInformation_98D_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_98D_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='98D')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1324, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1324, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_98D_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1325, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1325, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceE_ReportingInformation_98D_Type = MT300_SequenceE_ReportingInformation_98D_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceE_ReportingInformation_98D_Type', MT300_SequenceE_ReportingInformation_98D_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_17W_Type with content type SIMPLE
class MT300_SequenceE_ReportingInformation_17W_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_17W_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceE_ReportingInformation_17W_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceE_ReportingInformation_17W_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1334, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceE_ReportingInformation_17W_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_17W_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='17W')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1337, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1337, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_17W_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1338, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1338, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceE_ReportingInformation_17W_Type = MT300_SequenceE_ReportingInformation_17W_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceE_ReportingInformation_17W_Type', MT300_SequenceE_ReportingInformation_17W_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_22W_Type with content type SIMPLE
class MT300_SequenceE_ReportingInformation_22W_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_22W_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceE_ReportingInformation_22W_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceE_ReportingInformation_22W_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1347, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceE_ReportingInformation_22W_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_22W_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='22W')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1350, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1350, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_22W_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1351, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1351, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceE_ReportingInformation_22W_Type = MT300_SequenceE_ReportingInformation_22W_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceE_ReportingInformation_22W_Type', MT300_SequenceE_ReportingInformation_22W_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_17Y_Type with content type SIMPLE
class MT300_SequenceE_ReportingInformation_17Y_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_17Y_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceE_ReportingInformation_17Y_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceE_ReportingInformation_17Y_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1360, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceE_ReportingInformation_17Y_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_17Y_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='17Y')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1363, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1363, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_17Y_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1364, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1364, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceE_ReportingInformation_17Y_Type = MT300_SequenceE_ReportingInformation_17Y_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceE_ReportingInformation_17Y_Type', MT300_SequenceE_ReportingInformation_17Y_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_17Z_Type with content type SIMPLE
class MT300_SequenceE_ReportingInformation_17Z_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_17Z_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceE_ReportingInformation_17Z_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceE_ReportingInformation_17Z_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1373, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceE_ReportingInformation_17Z_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_17Z_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='17Z')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1376, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1376, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_17Z_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1377, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1377, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceE_ReportingInformation_17Z_Type = MT300_SequenceE_ReportingInformation_17Z_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceE_ReportingInformation_17Z_Type', MT300_SequenceE_ReportingInformation_17Z_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_22Q_Type with content type SIMPLE
class MT300_SequenceE_ReportingInformation_22Q_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_22Q_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceE_ReportingInformation_22Q_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceE_ReportingInformation_22Q_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1386, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceE_ReportingInformation_22Q_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_22Q_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='22Q')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1389, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1389, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_22Q_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1390, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1390, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceE_ReportingInformation_22Q_Type = MT300_SequenceE_ReportingInformation_22Q_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceE_ReportingInformation_22Q_Type', MT300_SequenceE_ReportingInformation_22Q_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_17L_Type with content type SIMPLE
class MT300_SequenceE_ReportingInformation_17L_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_17L_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceE_ReportingInformation_17L_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceE_ReportingInformation_17L_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1399, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceE_ReportingInformation_17L_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_17L_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='17L')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1402, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1402, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_17L_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1403, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1403, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceE_ReportingInformation_17L_Type = MT300_SequenceE_ReportingInformation_17L_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceE_ReportingInformation_17L_Type', MT300_SequenceE_ReportingInformation_17L_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_17M_Type with content type SIMPLE
class MT300_SequenceE_ReportingInformation_17M_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_17M_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceE_ReportingInformation_17M_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceE_ReportingInformation_17M_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1412, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceE_ReportingInformation_17M_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_17M_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='17M')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1415, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1415, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_17M_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1416, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1416, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceE_ReportingInformation_17M_Type = MT300_SequenceE_ReportingInformation_17M_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceE_ReportingInformation_17M_Type', MT300_SequenceE_ReportingInformation_17M_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_17Q_Type with content type SIMPLE
class MT300_SequenceE_ReportingInformation_17Q_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_17Q_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceE_ReportingInformation_17Q_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceE_ReportingInformation_17Q_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1425, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceE_ReportingInformation_17Q_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_17Q_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='17Q')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1428, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1428, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_17Q_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1429, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1429, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceE_ReportingInformation_17Q_Type = MT300_SequenceE_ReportingInformation_17Q_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceE_ReportingInformation_17Q_Type', MT300_SequenceE_ReportingInformation_17Q_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_17S_Type with content type SIMPLE
class MT300_SequenceE_ReportingInformation_17S_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_17S_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceE_ReportingInformation_17S_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceE_ReportingInformation_17S_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1438, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceE_ReportingInformation_17S_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_17S_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='17S')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1441, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1441, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_17S_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1442, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1442, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceE_ReportingInformation_17S_Type = MT300_SequenceE_ReportingInformation_17S_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceE_ReportingInformation_17S_Type', MT300_SequenceE_ReportingInformation_17S_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_17X_Type with content type SIMPLE
class MT300_SequenceE_ReportingInformation_17X_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_17X_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceE_ReportingInformation_17X_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceE_ReportingInformation_17X_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1451, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceE_ReportingInformation_17X_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_17X_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='17X')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1454, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1454, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_17X_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1455, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1455, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceE_ReportingInformation_17X_Type = MT300_SequenceE_ReportingInformation_17X_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceE_ReportingInformation_17X_Type', MT300_SequenceE_ReportingInformation_17X_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_98G_Type with content type SIMPLE
class MT300_SequenceE_ReportingInformation_98G_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_98G_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceE_ReportingInformation_98G_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceE_ReportingInformation_98G_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1464, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceE_ReportingInformation_98G_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_98G_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='98G')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1467, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1467, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_98G_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1468, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1468, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceE_ReportingInformation_98G_Type = MT300_SequenceE_ReportingInformation_98G_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceE_ReportingInformation_98G_Type', MT300_SequenceE_ReportingInformation_98G_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_98H_Type with content type SIMPLE
class MT300_SequenceE_ReportingInformation_98H_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_98H_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceE_ReportingInformation_98H_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceE_ReportingInformation_98H_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1477, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceE_ReportingInformation_98H_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_98H_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='98H')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1480, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1480, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_98H_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1481, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1481, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceE_ReportingInformation_98H_Type = MT300_SequenceE_ReportingInformation_98H_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceE_ReportingInformation_98H_Type', MT300_SequenceE_ReportingInformation_98H_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_34C_Type with content type SIMPLE
class MT300_SequenceE_ReportingInformation_34C_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_34C_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceE_ReportingInformation_34C_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceE_ReportingInformation_34C_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1490, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceE_ReportingInformation_34C_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_34C_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='34C')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1493, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1493, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_34C_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1494, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1494, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceE_ReportingInformation_34C_Type = MT300_SequenceE_ReportingInformation_34C_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceE_ReportingInformation_34C_Type', MT300_SequenceE_ReportingInformation_34C_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_77A_Type with content type SIMPLE
class MT300_SequenceE_ReportingInformation_77A_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceE_ReportingInformation_77A_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceE_ReportingInformation_77A_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceE_ReportingInformation_77A_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1503, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceE_ReportingInformation_77A_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_77A_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='77A')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1506, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1506, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceE_ReportingInformation_77A_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1507, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1507, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceE_ReportingInformation_77A_Type = MT300_SequenceE_ReportingInformation_77A_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceE_ReportingInformation_77A_Type', MT300_SequenceE_ReportingInformation_77A_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceF_PostTradeEvents_21H_Type with content type SIMPLE
class MT300_SequenceF_PostTradeEvents_21H_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceF_PostTradeEvents_21H_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceF_PostTradeEvents_21H_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceF_PostTradeEvents_21H_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1516, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceF_PostTradeEvents_21H_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceF_PostTradeEvents_21H_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='21H')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1519, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1519, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceF_PostTradeEvents_21H_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='True')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1520, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1520, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceF_PostTradeEvents_21H_Type = MT300_SequenceF_PostTradeEvents_21H_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceF_PostTradeEvents_21H_Type', MT300_SequenceF_PostTradeEvents_21H_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceF_PostTradeEvents_21F_Type with content type SIMPLE
class MT300_SequenceF_PostTradeEvents_21F_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceF_PostTradeEvents_21F_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceF_PostTradeEvents_21F_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceF_PostTradeEvents_21F_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1529, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceF_PostTradeEvents_21F_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceF_PostTradeEvents_21F_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='21F')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1532, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1532, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceF_PostTradeEvents_21F_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1533, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1533, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceF_PostTradeEvents_21F_Type = MT300_SequenceF_PostTradeEvents_21F_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceF_PostTradeEvents_21F_Type', MT300_SequenceF_PostTradeEvents_21F_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceF_PostTradeEvents_30F_Type with content type SIMPLE
class MT300_SequenceF_PostTradeEvents_30F_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceF_PostTradeEvents_30F_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceF_PostTradeEvents_30F_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceF_PostTradeEvents_30F_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1542, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceF_PostTradeEvents_30F_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceF_PostTradeEvents_30F_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='30F')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1545, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1545, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceF_PostTradeEvents_30F_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1546, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1546, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceF_PostTradeEvents_30F_Type = MT300_SequenceF_PostTradeEvents_30F_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceF_PostTradeEvents_30F_Type', MT300_SequenceF_PostTradeEvents_30F_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceF_PostTradeEvents_32H_Type with content type SIMPLE
class MT300_SequenceF_PostTradeEvents_32H_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceF_PostTradeEvents_32H_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceF_PostTradeEvents_32H_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceF_PostTradeEvents_32H_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1555, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceF_PostTradeEvents_32H_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceF_PostTradeEvents_32H_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='32H')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1558, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1558, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceF_PostTradeEvents_32H_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1559, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1559, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceF_PostTradeEvents_32H_Type = MT300_SequenceF_PostTradeEvents_32H_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceF_PostTradeEvents_32H_Type', MT300_SequenceF_PostTradeEvents_32H_Type)


# Complex type {http://www.w3schools.com}MT300_SequenceF_PostTradeEvents_33E_Type with content type SIMPLE
class MT300_SequenceF_PostTradeEvents_33E_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.w3schools.com}MT300_SequenceF_PostTradeEvents_33E_Type with content type SIMPLE"""
    _TypeDefinition = MT300_SequenceF_PostTradeEvents_33E_Type_Pattern
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MT300_SequenceF_PostTradeEvents_33E_Type')
    _XSDLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1568, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is MT300_SequenceF_PostTradeEvents_33E_Type_Pattern
    
    # Attribute swiftTag uses Python identifier swiftTag
    __swiftTag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'swiftTag'), 'swiftTag', '__httpwww_w3schools_com_MT300_SequenceF_PostTradeEvents_33E_Type_swiftTag', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='33E')
    __swiftTag._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1571, 4)
    __swiftTag._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1571, 4)
    
    swiftTag = property(__swiftTag.value, __swiftTag.set, None, None)

    
    # Attribute isMandatory uses Python identifier isMandatory
    __isMandatory = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isMandatory'), 'isMandatory', '__httpwww_w3schools_com_MT300_SequenceF_PostTradeEvents_33E_Type_isMandatory', pyxb.binding.datatypes.anySimpleType, unicode_default='False')
    __isMandatory._DeclarationLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1572, 4)
    __isMandatory._UseLocation = pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1572, 4)
    
    isMandatory = property(__isMandatory.value, __isMandatory.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __swiftTag.name() : __swiftTag,
        __isMandatory.name() : __isMandatory
    })
_module_typeBindings.MT300_SequenceF_PostTradeEvents_33E_Type = MT300_SequenceF_PostTradeEvents_33E_Type
Namespace.addCategoryObject('typeBinding', 'MT300_SequenceF_PostTradeEvents_33E_Type', MT300_SequenceF_PostTradeEvents_33E_Type)


MT300 = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'MT300'), CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1826, 1))
Namespace.addCategoryObject('elementBinding', MT300.name().localName(), MT300)



MT300_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SendersReference'), MT300_SequenceA_GeneralInformation_20_Type, scope=MT300_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1593, 3)))

MT300_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'RelatedReference'), MT300_SequenceA_GeneralInformation_21_Type, scope=MT300_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1594, 3)))

MT300_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'TypeOfOperation'), MT300_SequenceA_GeneralInformation_22A_Type, scope=MT300_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1595, 3)))

MT300_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ScopeOfOperation'), MT300_SequenceA_GeneralInformation_94A_Type, scope=MT300_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1596, 3)))

MT300_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'CommonReference'), MT300_SequenceA_GeneralInformation_22C_Type, scope=MT300_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1597, 3)))

MT300_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'BlockTradeIndicator'), MT300_SequenceA_GeneralInformation_17T_Type, scope=MT300_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1598, 3)))

MT300_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SplitSettlementIndicator'), MT300_SequenceA_GeneralInformation_17U_Type, scope=MT300_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1599, 3)))

MT300_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PaymentVersusPaymentSettlementIndicator'), MT300_SequenceA_GeneralInformation_17I_Type, scope=MT300_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1600, 3)))

MT300_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PartyA_A'), MT300_SequenceA_GeneralInformation_82A_Type, scope=MT300_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1602, 4)))

MT300_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PartyA_J'), MT300_SequenceA_GeneralInformation_82J_Type, scope=MT300_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1603, 4)))

MT300_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PartyB_A'), MT300_SequenceA_GeneralInformation_87A_Type, scope=MT300_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1606, 4)))

MT300_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PartyB_J'), MT300_SequenceA_GeneralInformation_87J_Type, scope=MT300_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1607, 4)))

MT300_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'FundOrBeneficiaryCustomer_A'), MT300_SequenceA_GeneralInformation_83A_Type, scope=MT300_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1610, 4)))

MT300_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'FundOrBeneficiaryCustomer_J'), MT300_SequenceA_GeneralInformation_83J_Type, scope=MT300_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1611, 4)))

MT300_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'TypeDateVersionOfAgreement'), MT300_SequenceA_GeneralInformation_77H_Type, scope=MT300_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1613, 3)))

MT300_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'TermsAndConditions'), MT300_SequenceA_GeneralInformation_77D_Type, scope=MT300_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1614, 3)))

MT300_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'YearOfDefinitions'), MT300_SequenceA_GeneralInformation_14C_Type, scope=MT300_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1615, 3)))

MT300_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Non-DeliverableIndicator'), MT300_SequenceA_GeneralInformation_17F_Type, scope=MT300_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1616, 3)))

MT300_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'NDFOpenIndicator'), MT300_SequenceA_GeneralInformation_17O_Type, scope=MT300_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1617, 3)))

MT300_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SettlementCurrency'), MT300_SequenceA_GeneralInformation_32E_Type, scope=MT300_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1618, 3)))

MT300_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ValuationDate'), MT300_SequenceA_GeneralInformation_30U_Type, scope=MT300_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1619, 3)))

MT300_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SettlementRateSource'), MT300_SequenceA_GeneralInformation_14S_Type, scope=MT300_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1620, 3)))

MT300_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ReferenceToOpeningConfirmation'), MT300_SequenceA_GeneralInformation_21A_Type, scope=MT300_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1621, 3)))

MT300_SequenceA_GeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ClearingOrSettlementSession'), MT300_SequenceA_GeneralInformation_14E_Type, scope=MT300_SequenceA_GeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1622, 3)))

def _BuildAutomaton ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1594, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1596, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1598, 3))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1599, 3))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1600, 3))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1609, 3))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1610, 4))
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1611, 4))
    counters.add(cc_7)
    cc_8 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1613, 3))
    counters.add(cc_8)
    cc_9 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1614, 3))
    counters.add(cc_9)
    cc_10 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1615, 3))
    counters.add(cc_10)
    cc_11 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1616, 3))
    counters.add(cc_11)
    cc_12 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1617, 3))
    counters.add(cc_12)
    cc_13 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1618, 3))
    counters.add(cc_13)
    cc_14 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1619, 3))
    counters.add(cc_14)
    cc_15 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1620, 3))
    counters.add(cc_15)
    cc_16 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1621, 3))
    counters.add(cc_16)
    cc_17 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1622, 3))
    counters.add(cc_17)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SendersReference')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1593, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'RelatedReference')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1594, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'TypeOfOperation')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1595, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ScopeOfOperation')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1596, 3))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'CommonReference')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1597, 3))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'BlockTradeIndicator')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1598, 3))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SplitSettlementIndicator')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1599, 3))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PaymentVersusPaymentSettlementIndicator')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1600, 3))
    st_7 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PartyA_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1602, 4))
    st_8 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PartyA_J')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1603, 4))
    st_9 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PartyB_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1606, 4))
    st_10 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_10)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PartyB_J')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1607, 4))
    st_11 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_11)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_5, False))
    final_update.add(fac.UpdateInstruction(cc_6, False))
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'FundOrBeneficiaryCustomer_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1610, 4))
    st_12 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_12)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_5, False))
    final_update.add(fac.UpdateInstruction(cc_7, False))
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'FundOrBeneficiaryCustomer_J')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1611, 4))
    st_13 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_13)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_8, False))
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'TypeDateVersionOfAgreement')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1613, 3))
    st_14 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_14)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_9, False))
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'TermsAndConditions')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1614, 3))
    st_15 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_15)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_10, False))
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'YearOfDefinitions')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1615, 3))
    st_16 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_16)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_11, False))
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Non-DeliverableIndicator')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1616, 3))
    st_17 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_17)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_12, False))
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'NDFOpenIndicator')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1617, 3))
    st_18 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_18)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_13, False))
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SettlementCurrency')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1618, 3))
    st_19 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_19)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_14, False))
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ValuationDate')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1619, 3))
    st_20 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_20)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_15, False))
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SettlementRateSource')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1620, 3))
    st_21 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_21)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_16, False))
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ReferenceToOpeningConfirmation')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1621, 3))
    st_22 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_22)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_17, False))
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceA_GeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ClearingOrSettlementSession')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1622, 3))
    st_23 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_23)
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
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_3, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_3, False) ]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_4, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_4, False) ]))
    st_7._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_10, [
         ]))
    transitions.append(fac.Transition(st_11, [
         ]))
    st_8._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_10, [
         ]))
    transitions.append(fac.Transition(st_11, [
         ]))
    st_9._set_transitionSet(transitions)
    transitions = []
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
    st_10._set_transitionSet(transitions)
    transitions = []
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
    st_11._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_5, True),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_6, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_5, True),
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
    st_12._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_5, True),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_5, True),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_7, True) ]))
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
    st_13._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_8, True) ]))
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
    st_14._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_9, True) ]))
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
    st_15._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_10, True) ]))
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
    st_16._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_11, True) ]))
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
    st_17._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_12, True) ]))
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
    st_18._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_13, True) ]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_13, False) ]))
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_13, False) ]))
    transitions.append(fac.Transition(st_22, [
        fac.UpdateInstruction(cc_13, False) ]))
    transitions.append(fac.Transition(st_23, [
        fac.UpdateInstruction(cc_13, False) ]))
    st_19._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_14, True) ]))
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_14, False) ]))
    transitions.append(fac.Transition(st_22, [
        fac.UpdateInstruction(cc_14, False) ]))
    transitions.append(fac.Transition(st_23, [
        fac.UpdateInstruction(cc_14, False) ]))
    st_20._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_15, True) ]))
    transitions.append(fac.Transition(st_22, [
        fac.UpdateInstruction(cc_15, False) ]))
    transitions.append(fac.Transition(st_23, [
        fac.UpdateInstruction(cc_15, False) ]))
    st_21._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_22, [
        fac.UpdateInstruction(cc_16, True) ]))
    transitions.append(fac.Transition(st_23, [
        fac.UpdateInstruction(cc_16, False) ]))
    st_22._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_23, [
        fac.UpdateInstruction(cc_17, True) ]))
    st_23._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
MT300_SequenceA_GeneralInformation._Automaton = _BuildAutomaton()




MT300_SequenceB_TransactionDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'TradeDate'), MT300_SequenceB_TransactionDetails_30T_Type, scope=MT300_SequenceB_TransactionDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1630, 3)))

MT300_SequenceB_TransactionDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ValueDate'), MT300_SequenceB_TransactionDetails_30V_Type, scope=MT300_SequenceB_TransactionDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1631, 3)))

MT300_SequenceB_TransactionDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ExchangeRate'), MT300_SequenceB_TransactionDetails_36_Type, scope=MT300_SequenceB_TransactionDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1632, 3)))

MT300_SequenceB_TransactionDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PaymentClearingCentre'), MT300_SequenceB_TransactionDetails_39M_Type, scope=MT300_SequenceB_TransactionDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1633, 3)))

MT300_SequenceB_TransactionDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SubSequenceB1_AmountBought'), MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought, scope=MT300_SequenceB_TransactionDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1634, 3)))

MT300_SequenceB_TransactionDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SubSequenceB2_AmountSold'), MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold, scope=MT300_SequenceB_TransactionDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1635, 3)))

def _BuildAutomaton_ ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_
    del _BuildAutomaton_
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1633, 3))
    counters.add(cc_0)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceB_TransactionDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'TradeDate')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1630, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceB_TransactionDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ValueDate')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1631, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceB_TransactionDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ExchangeRate')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1632, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceB_TransactionDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PaymentClearingCentre')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1633, 3))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceB_TransactionDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SubSequenceB1_AmountBought')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1634, 3))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceB_TransactionDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SubSequenceB2_AmountSold')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1635, 3))
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
MT300_SequenceB_TransactionDetails._Automaton = _BuildAutomaton_()




MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'CurrencyAmount'), MT300_SubSequenceB1_AmountBought_32B_Type, scope=MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1643, 3)))

MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_A'), MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_53A_Type, scope=MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1645, 4)))

MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_J'), MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_53J_Type, scope=MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1646, 4)))

MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_A'), MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_56A_Type, scope=MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1649, 4)))

MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_J'), MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_56J_Type, scope=MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1650, 4)))

MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_A'), MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_57A_Type, scope=MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1653, 4)))

MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_J'), MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought_57J_Type, scope=MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1654, 4)))

def _BuildAutomaton_2 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_2
    del _BuildAutomaton_2
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1644, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1645, 4))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1646, 4))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1648, 3))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1649, 4))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1650, 4))
    counters.add(cc_5)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'CurrencyAmount')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1643, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1645, 4))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_J')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1646, 4))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1649, 4))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_J')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1650, 4))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1653, 4))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_J')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1654, 4))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
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
    st_5._set_transitionSet(transitions)
    transitions = []
    st_6._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
MT300_SequenceB_TransactionDetails_SubSequenceB1_AmountBought._Automaton = _BuildAutomaton_2()




MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'CurrencyAmount'), MT300_SubSequenceB2_AmountSold_33B_Type, scope=MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1660, 3)))

MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_A'), MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_53A_Type, scope=MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1662, 4)))

MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_J'), MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_53J_Type, scope=MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1663, 4)))

MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_A'), MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_56A_Type, scope=MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1666, 4)))

MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_J'), MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_56J_Type, scope=MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1667, 4)))

MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_A'), MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_57A_Type, scope=MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1670, 4)))

MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_J'), MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_57J_Type, scope=MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1671, 4)))

MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_A'), MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_58A_Type, scope=MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1674, 4)))

MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_J'), MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold_58J_Type, scope=MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1675, 4)))

def _BuildAutomaton_3 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_3
    del _BuildAutomaton_3
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1661, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1662, 4))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1663, 4))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1665, 3))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1666, 4))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1667, 4))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1673, 3))
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1674, 4))
    counters.add(cc_7)
    cc_8 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1675, 4))
    counters.add(cc_8)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'CurrencyAmount')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1660, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1662, 4))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_J')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1663, 4))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1666, 4))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_J')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1667, 4))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1670, 4))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_J')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1671, 4))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_6, False))
    final_update.add(fac.UpdateInstruction(cc_7, False))
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1674, 4))
    st_7 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_6, False))
    final_update.add(fac.UpdateInstruction(cc_8, False))
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_J')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1675, 4))
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
MT300_SequenceB_TransactionDetails_SubSequenceB2_AmountSold._Automaton = _BuildAutomaton_3()




MT300_SequenceC_OptionalGeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ContactInformation'), MT300_SequenceC_OptionalGeneralInformation_29A_Type, scope=MT300_SequenceC_OptionalGeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1681, 3)))

MT300_SequenceC_OptionalGeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DealingMethod'), MT300_SequenceC_OptionalGeneralInformation_24D_Type, scope=MT300_SequenceC_OptionalGeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1682, 3)))

MT300_SequenceC_OptionalGeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DealingBranchPartyA_A'), MT300_SequenceC_OptionalGeneralInformation_84A_Type, scope=MT300_SequenceC_OptionalGeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1684, 4)))

MT300_SequenceC_OptionalGeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DealingBranchPartyA_B'), MT300_SequenceC_OptionalGeneralInformation_84B_Type, scope=MT300_SequenceC_OptionalGeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1685, 4)))

MT300_SequenceC_OptionalGeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DealingBranchPartyA_D'), MT300_SequenceC_OptionalGeneralInformation_84D_Type, scope=MT300_SequenceC_OptionalGeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1686, 4)))

MT300_SequenceC_OptionalGeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DealingBranchPartyA_J'), MT300_SequenceC_OptionalGeneralInformation_84J_Type, scope=MT300_SequenceC_OptionalGeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1687, 4)))

MT300_SequenceC_OptionalGeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DealingBranchPartyB_A'), MT300_SequenceC_OptionalGeneralInformation_85A_Type, scope=MT300_SequenceC_OptionalGeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1690, 4)))

MT300_SequenceC_OptionalGeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DealingBranchPartyB_B'), MT300_SequenceC_OptionalGeneralInformation_85B_Type, scope=MT300_SequenceC_OptionalGeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1691, 4)))

MT300_SequenceC_OptionalGeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DealingBranchPartyB_D'), MT300_SequenceC_OptionalGeneralInformation_85D_Type, scope=MT300_SequenceC_OptionalGeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1692, 4)))

MT300_SequenceC_OptionalGeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DealingBranchPartyB_J'), MT300_SequenceC_OptionalGeneralInformation_85J_Type, scope=MT300_SequenceC_OptionalGeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1693, 4)))

MT300_SequenceC_OptionalGeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'BrokerIdentification_A'), MT300_SequenceC_OptionalGeneralInformation_88A_Type, scope=MT300_SequenceC_OptionalGeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1696, 4)))

MT300_SequenceC_OptionalGeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'BrokerIdentification_D'), MT300_SequenceC_OptionalGeneralInformation_88D_Type, scope=MT300_SequenceC_OptionalGeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1697, 4)))

MT300_SequenceC_OptionalGeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'BrokerIdentification_J'), MT300_SequenceC_OptionalGeneralInformation_88J_Type, scope=MT300_SequenceC_OptionalGeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1698, 4)))

MT300_SequenceC_OptionalGeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'BrokersCommission'), MT300_SequenceC_OptionalGeneralInformation_71F_Type, scope=MT300_SequenceC_OptionalGeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1700, 3)))

MT300_SequenceC_OptionalGeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'CounterpartysReference'), MT300_SequenceC_OptionalGeneralInformation_26H_Type, scope=MT300_SequenceC_OptionalGeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1701, 3)))

MT300_SequenceC_OptionalGeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'BrokersReference'), MT300_SequenceC_OptionalGeneralInformation_21G_Type, scope=MT300_SequenceC_OptionalGeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1702, 3)))

MT300_SequenceC_OptionalGeneralInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SenderToReceiverInformation'), MT300_SequenceC_OptionalGeneralInformation_72_Type, scope=MT300_SequenceC_OptionalGeneralInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1703, 3)))

def _BuildAutomaton_4 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_4
    del _BuildAutomaton_4
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1681, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1682, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1683, 3))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1684, 4))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1685, 4))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1686, 4))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1687, 4))
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1689, 3))
    counters.add(cc_7)
    cc_8 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1690, 4))
    counters.add(cc_8)
    cc_9 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1691, 4))
    counters.add(cc_9)
    cc_10 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1692, 4))
    counters.add(cc_10)
    cc_11 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1693, 4))
    counters.add(cc_11)
    cc_12 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1695, 3))
    counters.add(cc_12)
    cc_13 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1696, 4))
    counters.add(cc_13)
    cc_14 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1697, 4))
    counters.add(cc_14)
    cc_15 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1698, 4))
    counters.add(cc_15)
    cc_16 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1700, 3))
    counters.add(cc_16)
    cc_17 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1701, 3))
    counters.add(cc_17)
    cc_18 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1702, 3))
    counters.add(cc_18)
    cc_19 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1703, 3))
    counters.add(cc_19)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceC_OptionalGeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ContactInformation')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1681, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceC_OptionalGeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'DealingMethod')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1682, 3))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceC_OptionalGeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'DealingBranchPartyA_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1684, 4))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceC_OptionalGeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'DealingBranchPartyA_B')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1685, 4))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    final_update.add(fac.UpdateInstruction(cc_5, False))
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceC_OptionalGeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'DealingBranchPartyA_D')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1686, 4))
    st_4 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    final_update.add(fac.UpdateInstruction(cc_6, False))
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceC_OptionalGeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'DealingBranchPartyA_J')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1687, 4))
    st_5 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_7, False))
    final_update.add(fac.UpdateInstruction(cc_8, False))
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceC_OptionalGeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'DealingBranchPartyB_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1690, 4))
    st_6 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_7, False))
    final_update.add(fac.UpdateInstruction(cc_9, False))
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceC_OptionalGeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'DealingBranchPartyB_B')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1691, 4))
    st_7 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_7, False))
    final_update.add(fac.UpdateInstruction(cc_10, False))
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceC_OptionalGeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'DealingBranchPartyB_D')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1692, 4))
    st_8 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_7, False))
    final_update.add(fac.UpdateInstruction(cc_11, False))
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceC_OptionalGeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'DealingBranchPartyB_J')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1693, 4))
    st_9 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_12, False))
    final_update.add(fac.UpdateInstruction(cc_13, False))
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceC_OptionalGeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'BrokerIdentification_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1696, 4))
    st_10 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_10)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_12, False))
    final_update.add(fac.UpdateInstruction(cc_14, False))
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceC_OptionalGeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'BrokerIdentification_D')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1697, 4))
    st_11 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_11)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_12, False))
    final_update.add(fac.UpdateInstruction(cc_15, False))
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceC_OptionalGeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'BrokerIdentification_J')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1698, 4))
    st_12 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_12)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_16, False))
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceC_OptionalGeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'BrokersCommission')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1700, 3))
    st_13 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_13)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_17, False))
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceC_OptionalGeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'CounterpartysReference')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1701, 3))
    st_14 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_14)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_18, False))
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceC_OptionalGeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'BrokersReference')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1702, 3))
    st_15 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_15)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_19, False))
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceC_OptionalGeneralInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SenderToReceiverInformation')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1703, 3))
    st_16 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_16)
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
    st_13._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_17, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_17, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_17, False) ]))
    st_14._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_18, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_18, False) ]))
    st_15._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_19, True) ]))
    st_16._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
MT300_SequenceC_OptionalGeneralInformation._Automaton = _BuildAutomaton_4()




MT300_SequenceD_SplitSettlementDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SettlementDetails'), MT300_SequenceD_SplitSettlementDetails_SettlementDetails, scope=MT300_SequenceD_SplitSettlementDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1711, 3)))

MT300_SequenceD_SplitSettlementDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'NumberOfSettlements'), MT300_SequenceD_SplitSettlementDetails_16A_Type, scope=MT300_SequenceD_SplitSettlementDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1712, 3)))

def _BuildAutomaton_5 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_5
    del _BuildAutomaton_5
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceD_SplitSettlementDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SettlementDetails')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1711, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceD_SplitSettlementDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'NumberOfSettlements')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1712, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
MT300_SequenceD_SplitSettlementDetails._Automaton = _BuildAutomaton_5()




MT300_SequenceD_SplitSettlementDetails_SettlementDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'BuySellIndicator'), MT300_SequenceD_SplitSettlementDetails_SettlementDetails_17A_Type, scope=MT300_SequenceD_SplitSettlementDetails_SettlementDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1720, 3)))

MT300_SequenceD_SplitSettlementDetails_SettlementDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'CurrencyAmount'), MT300_SequenceD_SplitSettlementDetails_SettlementDetails_32B_Type, scope=MT300_SequenceD_SplitSettlementDetails_SettlementDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1721, 3)))

MT300_SequenceD_SplitSettlementDetails_SettlementDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_A'), MT300_SequenceD_SplitSettlementDetails_SettlementDetails_53A_Type, scope=MT300_SequenceD_SplitSettlementDetails_SettlementDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1723, 4)))

MT300_SequenceD_SplitSettlementDetails_SettlementDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_D'), MT300_SequenceD_SplitSettlementDetails_SettlementDetails_53D_Type, scope=MT300_SequenceD_SplitSettlementDetails_SettlementDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1724, 4)))

MT300_SequenceD_SplitSettlementDetails_SettlementDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_J'), MT300_SequenceD_SplitSettlementDetails_SettlementDetails_53J_Type, scope=MT300_SequenceD_SplitSettlementDetails_SettlementDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1725, 4)))

MT300_SequenceD_SplitSettlementDetails_SettlementDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_A'), MT300_SequenceD_SplitSettlementDetails_SettlementDetails_56A_Type, scope=MT300_SequenceD_SplitSettlementDetails_SettlementDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1728, 4)))

MT300_SequenceD_SplitSettlementDetails_SettlementDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_D'), MT300_SequenceD_SplitSettlementDetails_SettlementDetails_56D_Type, scope=MT300_SequenceD_SplitSettlementDetails_SettlementDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1729, 4)))

MT300_SequenceD_SplitSettlementDetails_SettlementDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_J'), MT300_SequenceD_SplitSettlementDetails_SettlementDetails_56J_Type, scope=MT300_SequenceD_SplitSettlementDetails_SettlementDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1730, 4)))

MT300_SequenceD_SplitSettlementDetails_SettlementDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_A'), MT300_SequenceD_SplitSettlementDetails_SettlementDetails_57A_Type, scope=MT300_SequenceD_SplitSettlementDetails_SettlementDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1733, 4)))

MT300_SequenceD_SplitSettlementDetails_SettlementDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_D'), MT300_SequenceD_SplitSettlementDetails_SettlementDetails_57D_Type, scope=MT300_SequenceD_SplitSettlementDetails_SettlementDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1734, 4)))

MT300_SequenceD_SplitSettlementDetails_SettlementDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_J'), MT300_SequenceD_SplitSettlementDetails_SettlementDetails_57J_Type, scope=MT300_SequenceD_SplitSettlementDetails_SettlementDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1735, 4)))

MT300_SequenceD_SplitSettlementDetails_SettlementDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_A'), MT300_SequenceD_SplitSettlementDetails_SettlementDetails_58A_Type, scope=MT300_SequenceD_SplitSettlementDetails_SettlementDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1738, 4)))

MT300_SequenceD_SplitSettlementDetails_SettlementDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_D'), MT300_SequenceD_SplitSettlementDetails_SettlementDetails_58D_Type, scope=MT300_SequenceD_SplitSettlementDetails_SettlementDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1739, 4)))

MT300_SequenceD_SplitSettlementDetails_SettlementDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_J'), MT300_SequenceD_SplitSettlementDetails_SettlementDetails_58J_Type, scope=MT300_SequenceD_SplitSettlementDetails_SettlementDetails, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1740, 4)))

def _BuildAutomaton_6 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_6
    del _BuildAutomaton_6
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1722, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1723, 4))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1724, 4))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1725, 4))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1727, 3))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1728, 4))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1729, 4))
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1730, 4))
    counters.add(cc_7)
    cc_8 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1737, 3))
    counters.add(cc_8)
    cc_9 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1738, 4))
    counters.add(cc_9)
    cc_10 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1739, 4))
    counters.add(cc_10)
    cc_11 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1740, 4))
    counters.add(cc_11)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceD_SplitSettlementDetails_SettlementDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'BuySellIndicator')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1720, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceD_SplitSettlementDetails_SettlementDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'CurrencyAmount')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1721, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceD_SplitSettlementDetails_SettlementDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1723, 4))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceD_SplitSettlementDetails_SettlementDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_D')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1724, 4))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceD_SplitSettlementDetails_SettlementDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'DeliveryAgent_J')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1725, 4))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceD_SplitSettlementDetails_SettlementDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1728, 4))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceD_SplitSettlementDetails_SettlementDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_D')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1729, 4))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceD_SplitSettlementDetails_SettlementDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Intermediary_J')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1730, 4))
    st_7 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceD_SplitSettlementDetails_SettlementDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1733, 4))
    st_8 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceD_SplitSettlementDetails_SettlementDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_D')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1734, 4))
    st_9 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceD_SplitSettlementDetails_SettlementDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ReceivingAgent_J')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1735, 4))
    st_10 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_10)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_8, False))
    final_update.add(fac.UpdateInstruction(cc_9, False))
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceD_SplitSettlementDetails_SettlementDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1738, 4))
    st_11 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_11)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_8, False))
    final_update.add(fac.UpdateInstruction(cc_10, False))
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceD_SplitSettlementDetails_SettlementDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_D')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1739, 4))
    st_12 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_12)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_8, False))
    final_update.add(fac.UpdateInstruction(cc_11, False))
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceD_SplitSettlementDetails_SettlementDetails._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'BeneficiaryInstitution_J')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1740, 4))
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
    st_7._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_11, [
         ]))
    transitions.append(fac.Transition(st_12, [
         ]))
    transitions.append(fac.Transition(st_13, [
         ]))
    st_8._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_11, [
         ]))
    transitions.append(fac.Transition(st_12, [
         ]))
    transitions.append(fac.Transition(st_13, [
         ]))
    st_9._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_11, [
         ]))
    transitions.append(fac.Transition(st_12, [
         ]))
    transitions.append(fac.Transition(st_13, [
         ]))
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
        fac.UpdateInstruction(cc_8, True),
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
        fac.UpdateInstruction(cc_8, True),
        fac.UpdateInstruction(cc_10, False) ]))
    st_12._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_8, True),
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_8, True),
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_8, True),
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_11, True) ]))
    st_13._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
MT300_SequenceD_SplitSettlementDetails_SettlementDetails._Automaton = _BuildAutomaton_6()




MT300_SequenceE_ReportingInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SubSequenceE1_ReportingParties'), MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties, scope=MT300_SequenceE_ReportingInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1746, 3)))

MT300_SequenceE_ReportingInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'CentralCounterpartyClearingHouse_A'), MT300_SequenceE_ReportingInformation_81A_Type, scope=MT300_SequenceE_ReportingInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1748, 4)))

MT300_SequenceE_ReportingInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'CentralCounterpartyClearingHouse_D'), MT300_SequenceE_ReportingInformation_81D_Type, scope=MT300_SequenceE_ReportingInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1749, 4)))

MT300_SequenceE_ReportingInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'CentralCounterpartyClearingHouse_J'), MT300_SequenceE_ReportingInformation_81J_Type, scope=MT300_SequenceE_ReportingInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1750, 4)))

MT300_SequenceE_ReportingInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ClearingBroker_A'), MT300_SequenceE_ReportingInformation_89A_Type, scope=MT300_SequenceE_ReportingInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1753, 4)))

MT300_SequenceE_ReportingInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ClearingBroker_D'), MT300_SequenceE_ReportingInformation_89D_Type, scope=MT300_SequenceE_ReportingInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1754, 4)))

MT300_SequenceE_ReportingInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ClearingBroker_J'), MT300_SequenceE_ReportingInformation_89J_Type, scope=MT300_SequenceE_ReportingInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1755, 4)))

MT300_SequenceE_ReportingInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ClearingExceptionParty_A'), MT300_SequenceE_ReportingInformation_96A_Type, scope=MT300_SequenceE_ReportingInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1758, 4)))

MT300_SequenceE_ReportingInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ClearingExceptionParty_D'), MT300_SequenceE_ReportingInformation_96D_Type, scope=MT300_SequenceE_ReportingInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1759, 4)))

MT300_SequenceE_ReportingInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ClearingExceptionParty_J'), MT300_SequenceE_ReportingInformation_96J_Type, scope=MT300_SequenceE_ReportingInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1760, 4)))

MT300_SequenceE_ReportingInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ClearingBrokerIdentification'), MT300_SequenceE_ReportingInformation_22S_Type, scope=MT300_SequenceE_ReportingInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1762, 3)))

MT300_SequenceE_ReportingInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ClearedProductIdentification'), MT300_SequenceE_ReportingInformation_22T_Type, scope=MT300_SequenceE_ReportingInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1763, 3)))

MT300_SequenceE_ReportingInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ClearingThresholdIndicator'), MT300_SequenceE_ReportingInformation_17E_Type, scope=MT300_SequenceE_ReportingInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1764, 3)))

MT300_SequenceE_ReportingInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'UnderlyingProductIdentifier'), MT300_SequenceE_ReportingInformation_22U_Type, scope=MT300_SequenceE_ReportingInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1765, 3)))

MT300_SequenceE_ReportingInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'IdentificationOfFinancialInstrument'), MT300_SequenceE_ReportingInformation_35B_Type, scope=MT300_SequenceE_ReportingInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1766, 3)))

MT300_SequenceE_ReportingInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'AllocationIndicator'), MT300_SequenceE_ReportingInformation_17H_Type, scope=MT300_SequenceE_ReportingInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1767, 3)))

MT300_SequenceE_ReportingInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'CollateralisationIndicator'), MT300_SequenceE_ReportingInformation_17P_Type, scope=MT300_SequenceE_ReportingInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1768, 3)))

MT300_SequenceE_ReportingInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ExecutionVenue'), MT300_SequenceE_ReportingInformation_22V_Type, scope=MT300_SequenceE_ReportingInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1769, 3)))

MT300_SequenceE_ReportingInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ExecutionTimestamp'), MT300_SequenceE_ReportingInformation_98D_Type, scope=MT300_SequenceE_ReportingInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1770, 3)))

MT300_SequenceE_ReportingInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'NonStandardFlag'), MT300_SequenceE_ReportingInformation_17W_Type, scope=MT300_SequenceE_ReportingInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1771, 3)))

MT300_SequenceE_ReportingInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'LinkSwapIdentification'), MT300_SequenceE_ReportingInformation_22W_Type, scope=MT300_SequenceE_ReportingInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1772, 3)))

MT300_SequenceE_ReportingInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'FinancialNatureOfCounterpartyIndicator'), MT300_SequenceE_ReportingInformation_17Y_Type, scope=MT300_SequenceE_ReportingInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1773, 3)))

MT300_SequenceE_ReportingInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'CollateralPortfolioIndicator'), MT300_SequenceE_ReportingInformation_17Z_Type, scope=MT300_SequenceE_ReportingInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1774, 3)))

MT300_SequenceE_ReportingInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'CollateralPortfolioCode'), MT300_SequenceE_ReportingInformation_22Q_Type, scope=MT300_SequenceE_ReportingInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1775, 3)))

MT300_SequenceE_ReportingInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PortfolioCompressionIndicator'), MT300_SequenceE_ReportingInformation_17L_Type, scope=MT300_SequenceE_ReportingInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1776, 3)))

MT300_SequenceE_ReportingInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'CorporateSectorIndicator'), MT300_SequenceE_ReportingInformation_17M_Type, scope=MT300_SequenceE_ReportingInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1777, 3)))

MT300_SequenceE_ReportingInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'TradeWithNonEEACounterpartyIndicator'), MT300_SequenceE_ReportingInformation_17Q_Type, scope=MT300_SequenceE_ReportingInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1778, 3)))

MT300_SequenceE_ReportingInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'IntragroupTradeIndicator'), MT300_SequenceE_ReportingInformation_17S_Type, scope=MT300_SequenceE_ReportingInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1779, 3)))

MT300_SequenceE_ReportingInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'CommercialOrTreasuryFinancingIndicator'), MT300_SequenceE_ReportingInformation_17X_Type, scope=MT300_SequenceE_ReportingInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1780, 3)))

MT300_SequenceE_ReportingInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ConfirmationTimestamp'), MT300_SequenceE_ReportingInformation_98G_Type, scope=MT300_SequenceE_ReportingInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1781, 3)))

MT300_SequenceE_ReportingInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ClearingTimestamp'), MT300_SequenceE_ReportingInformation_98H_Type, scope=MT300_SequenceE_ReportingInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1782, 3)))

MT300_SequenceE_ReportingInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'CommissionAndFees'), MT300_SequenceE_ReportingInformation_34C_Type, scope=MT300_SequenceE_ReportingInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1783, 3)))

MT300_SequenceE_ReportingInformation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'AdditionalReportingInformation'), MT300_SequenceE_ReportingInformation_77A_Type, scope=MT300_SequenceE_ReportingInformation, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1784, 3)))

def _BuildAutomaton_7 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_7
    del _BuildAutomaton_7
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1746, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1747, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1748, 4))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1749, 4))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1750, 4))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1752, 3))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1753, 4))
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1754, 4))
    counters.add(cc_7)
    cc_8 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1755, 4))
    counters.add(cc_8)
    cc_9 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1757, 3))
    counters.add(cc_9)
    cc_10 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1758, 4))
    counters.add(cc_10)
    cc_11 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1759, 4))
    counters.add(cc_11)
    cc_12 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1760, 4))
    counters.add(cc_12)
    cc_13 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1762, 3))
    counters.add(cc_13)
    cc_14 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1763, 3))
    counters.add(cc_14)
    cc_15 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1764, 3))
    counters.add(cc_15)
    cc_16 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1765, 3))
    counters.add(cc_16)
    cc_17 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1766, 3))
    counters.add(cc_17)
    cc_18 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1767, 3))
    counters.add(cc_18)
    cc_19 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1768, 3))
    counters.add(cc_19)
    cc_20 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1769, 3))
    counters.add(cc_20)
    cc_21 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1770, 3))
    counters.add(cc_21)
    cc_22 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1771, 3))
    counters.add(cc_22)
    cc_23 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1772, 3))
    counters.add(cc_23)
    cc_24 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1773, 3))
    counters.add(cc_24)
    cc_25 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1774, 3))
    counters.add(cc_25)
    cc_26 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1775, 3))
    counters.add(cc_26)
    cc_27 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1776, 3))
    counters.add(cc_27)
    cc_28 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1777, 3))
    counters.add(cc_28)
    cc_29 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1778, 3))
    counters.add(cc_29)
    cc_30 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1779, 3))
    counters.add(cc_30)
    cc_31 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1780, 3))
    counters.add(cc_31)
    cc_32 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1781, 3))
    counters.add(cc_32)
    cc_33 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1782, 3))
    counters.add(cc_33)
    cc_34 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1783, 3))
    counters.add(cc_34)
    cc_35 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1784, 3))
    counters.add(cc_35)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceE_ReportingInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SubSequenceE1_ReportingParties')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1746, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceE_ReportingInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'CentralCounterpartyClearingHouse_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1748, 4))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceE_ReportingInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'CentralCounterpartyClearingHouse_D')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1749, 4))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceE_ReportingInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'CentralCounterpartyClearingHouse_J')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1750, 4))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_5, False))
    final_update.add(fac.UpdateInstruction(cc_6, False))
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceE_ReportingInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ClearingBroker_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1753, 4))
    st_4 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_5, False))
    final_update.add(fac.UpdateInstruction(cc_7, False))
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceE_ReportingInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ClearingBroker_D')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1754, 4))
    st_5 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_5, False))
    final_update.add(fac.UpdateInstruction(cc_8, False))
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceE_ReportingInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ClearingBroker_J')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1755, 4))
    st_6 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_9, False))
    final_update.add(fac.UpdateInstruction(cc_10, False))
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceE_ReportingInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ClearingExceptionParty_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1758, 4))
    st_7 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_9, False))
    final_update.add(fac.UpdateInstruction(cc_11, False))
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceE_ReportingInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ClearingExceptionParty_D')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1759, 4))
    st_8 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_9, False))
    final_update.add(fac.UpdateInstruction(cc_12, False))
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceE_ReportingInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ClearingExceptionParty_J')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1760, 4))
    st_9 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_13, False))
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceE_ReportingInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ClearingBrokerIdentification')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1762, 3))
    st_10 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_10)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_14, False))
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceE_ReportingInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ClearedProductIdentification')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1763, 3))
    st_11 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_11)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_15, False))
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceE_ReportingInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ClearingThresholdIndicator')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1764, 3))
    st_12 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_12)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_16, False))
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceE_ReportingInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'UnderlyingProductIdentifier')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1765, 3))
    st_13 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_13)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_17, False))
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceE_ReportingInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'IdentificationOfFinancialInstrument')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1766, 3))
    st_14 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_14)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_18, False))
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceE_ReportingInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'AllocationIndicator')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1767, 3))
    st_15 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_15)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_19, False))
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceE_ReportingInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'CollateralisationIndicator')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1768, 3))
    st_16 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_16)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_20, False))
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceE_ReportingInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ExecutionVenue')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1769, 3))
    st_17 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_17)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_21, False))
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceE_ReportingInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ExecutionTimestamp')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1770, 3))
    st_18 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_18)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_22, False))
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceE_ReportingInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'NonStandardFlag')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1771, 3))
    st_19 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_19)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_23, False))
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceE_ReportingInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'LinkSwapIdentification')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1772, 3))
    st_20 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_20)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_24, False))
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceE_ReportingInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'FinancialNatureOfCounterpartyIndicator')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1773, 3))
    st_21 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_21)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_25, False))
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceE_ReportingInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'CollateralPortfolioIndicator')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1774, 3))
    st_22 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_22)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_26, False))
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceE_ReportingInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'CollateralPortfolioCode')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1775, 3))
    st_23 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_23)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_27, False))
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceE_ReportingInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PortfolioCompressionIndicator')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1776, 3))
    st_24 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_24)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_28, False))
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceE_ReportingInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'CorporateSectorIndicator')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1777, 3))
    st_25 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_25)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_29, False))
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceE_ReportingInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'TradeWithNonEEACounterpartyIndicator')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1778, 3))
    st_26 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_26)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_30, False))
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceE_ReportingInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'IntragroupTradeIndicator')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1779, 3))
    st_27 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_27)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_31, False))
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceE_ReportingInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'CommercialOrTreasuryFinancingIndicator')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1780, 3))
    st_28 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_28)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_32, False))
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceE_ReportingInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ConfirmationTimestamp')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1781, 3))
    st_29 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_29)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_33, False))
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceE_ReportingInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ClearingTimestamp')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1782, 3))
    st_30 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_30)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_34, False))
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceE_ReportingInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'CommissionAndFees')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1783, 3))
    st_31 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_31)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_35, False))
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceE_ReportingInformation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'AdditionalReportingInformation')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1784, 3))
    st_32 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_32)
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
    transitions.append(fac.Transition(st_30, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_31, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_32, [
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
    transitions.append(fac.Transition(st_30, [
        fac.UpdateInstruction(cc_1, False),
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_31, [
        fac.UpdateInstruction(cc_1, False),
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_32, [
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
    transitions.append(fac.Transition(st_30, [
        fac.UpdateInstruction(cc_1, False),
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_31, [
        fac.UpdateInstruction(cc_1, False),
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_32, [
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
    transitions.append(fac.Transition(st_30, [
        fac.UpdateInstruction(cc_1, False),
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_31, [
        fac.UpdateInstruction(cc_1, False),
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_32, [
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
    transitions.append(fac.Transition(st_30, [
        fac.UpdateInstruction(cc_5, False),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_31, [
        fac.UpdateInstruction(cc_5, False),
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_32, [
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
    transitions.append(fac.Transition(st_30, [
        fac.UpdateInstruction(cc_5, False),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_31, [
        fac.UpdateInstruction(cc_5, False),
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_32, [
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
    transitions.append(fac.Transition(st_30, [
        fac.UpdateInstruction(cc_5, False),
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_31, [
        fac.UpdateInstruction(cc_5, False),
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_32, [
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
    transitions.append(fac.Transition(st_30, [
        fac.UpdateInstruction(cc_9, False),
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_31, [
        fac.UpdateInstruction(cc_9, False),
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_32, [
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
    transitions.append(fac.Transition(st_30, [
        fac.UpdateInstruction(cc_9, False),
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_31, [
        fac.UpdateInstruction(cc_9, False),
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_32, [
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
    transitions.append(fac.Transition(st_30, [
        fac.UpdateInstruction(cc_9, False),
        fac.UpdateInstruction(cc_12, False) ]))
    transitions.append(fac.Transition(st_31, [
        fac.UpdateInstruction(cc_9, False),
        fac.UpdateInstruction(cc_12, False) ]))
    transitions.append(fac.Transition(st_32, [
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
    transitions.append(fac.Transition(st_30, [
        fac.UpdateInstruction(cc_13, False) ]))
    transitions.append(fac.Transition(st_31, [
        fac.UpdateInstruction(cc_13, False) ]))
    transitions.append(fac.Transition(st_32, [
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
    transitions.append(fac.Transition(st_30, [
        fac.UpdateInstruction(cc_14, False) ]))
    transitions.append(fac.Transition(st_31, [
        fac.UpdateInstruction(cc_14, False) ]))
    transitions.append(fac.Transition(st_32, [
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
    transitions.append(fac.Transition(st_30, [
        fac.UpdateInstruction(cc_15, False) ]))
    transitions.append(fac.Transition(st_31, [
        fac.UpdateInstruction(cc_15, False) ]))
    transitions.append(fac.Transition(st_32, [
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
    transitions.append(fac.Transition(st_30, [
        fac.UpdateInstruction(cc_16, False) ]))
    transitions.append(fac.Transition(st_31, [
        fac.UpdateInstruction(cc_16, False) ]))
    transitions.append(fac.Transition(st_32, [
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
    transitions.append(fac.Transition(st_30, [
        fac.UpdateInstruction(cc_17, False) ]))
    transitions.append(fac.Transition(st_31, [
        fac.UpdateInstruction(cc_17, False) ]))
    transitions.append(fac.Transition(st_32, [
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
    transitions.append(fac.Transition(st_30, [
        fac.UpdateInstruction(cc_18, False) ]))
    transitions.append(fac.Transition(st_31, [
        fac.UpdateInstruction(cc_18, False) ]))
    transitions.append(fac.Transition(st_32, [
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
    transitions.append(fac.Transition(st_30, [
        fac.UpdateInstruction(cc_19, False) ]))
    transitions.append(fac.Transition(st_31, [
        fac.UpdateInstruction(cc_19, False) ]))
    transitions.append(fac.Transition(st_32, [
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
    transitions.append(fac.Transition(st_30, [
        fac.UpdateInstruction(cc_20, False) ]))
    transitions.append(fac.Transition(st_31, [
        fac.UpdateInstruction(cc_20, False) ]))
    transitions.append(fac.Transition(st_32, [
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
    transitions.append(fac.Transition(st_30, [
        fac.UpdateInstruction(cc_21, False) ]))
    transitions.append(fac.Transition(st_31, [
        fac.UpdateInstruction(cc_21, False) ]))
    transitions.append(fac.Transition(st_32, [
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
    transitions.append(fac.Transition(st_30, [
        fac.UpdateInstruction(cc_22, False) ]))
    transitions.append(fac.Transition(st_31, [
        fac.UpdateInstruction(cc_22, False) ]))
    transitions.append(fac.Transition(st_32, [
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
    transitions.append(fac.Transition(st_30, [
        fac.UpdateInstruction(cc_23, False) ]))
    transitions.append(fac.Transition(st_31, [
        fac.UpdateInstruction(cc_23, False) ]))
    transitions.append(fac.Transition(st_32, [
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
    transitions.append(fac.Transition(st_30, [
        fac.UpdateInstruction(cc_24, False) ]))
    transitions.append(fac.Transition(st_31, [
        fac.UpdateInstruction(cc_24, False) ]))
    transitions.append(fac.Transition(st_32, [
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
    transitions.append(fac.Transition(st_30, [
        fac.UpdateInstruction(cc_25, False) ]))
    transitions.append(fac.Transition(st_31, [
        fac.UpdateInstruction(cc_25, False) ]))
    transitions.append(fac.Transition(st_32, [
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
    transitions.append(fac.Transition(st_30, [
        fac.UpdateInstruction(cc_26, False) ]))
    transitions.append(fac.Transition(st_31, [
        fac.UpdateInstruction(cc_26, False) ]))
    transitions.append(fac.Transition(st_32, [
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
    transitions.append(fac.Transition(st_30, [
        fac.UpdateInstruction(cc_27, False) ]))
    transitions.append(fac.Transition(st_31, [
        fac.UpdateInstruction(cc_27, False) ]))
    transitions.append(fac.Transition(st_32, [
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
    transitions.append(fac.Transition(st_30, [
        fac.UpdateInstruction(cc_28, False) ]))
    transitions.append(fac.Transition(st_31, [
        fac.UpdateInstruction(cc_28, False) ]))
    transitions.append(fac.Transition(st_32, [
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
    transitions.append(fac.Transition(st_30, [
        fac.UpdateInstruction(cc_29, False) ]))
    transitions.append(fac.Transition(st_31, [
        fac.UpdateInstruction(cc_29, False) ]))
    transitions.append(fac.Transition(st_32, [
        fac.UpdateInstruction(cc_29, False) ]))
    st_26._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_27, [
        fac.UpdateInstruction(cc_30, True) ]))
    transitions.append(fac.Transition(st_28, [
        fac.UpdateInstruction(cc_30, False) ]))
    transitions.append(fac.Transition(st_29, [
        fac.UpdateInstruction(cc_30, False) ]))
    transitions.append(fac.Transition(st_30, [
        fac.UpdateInstruction(cc_30, False) ]))
    transitions.append(fac.Transition(st_31, [
        fac.UpdateInstruction(cc_30, False) ]))
    transitions.append(fac.Transition(st_32, [
        fac.UpdateInstruction(cc_30, False) ]))
    st_27._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_28, [
        fac.UpdateInstruction(cc_31, True) ]))
    transitions.append(fac.Transition(st_29, [
        fac.UpdateInstruction(cc_31, False) ]))
    transitions.append(fac.Transition(st_30, [
        fac.UpdateInstruction(cc_31, False) ]))
    transitions.append(fac.Transition(st_31, [
        fac.UpdateInstruction(cc_31, False) ]))
    transitions.append(fac.Transition(st_32, [
        fac.UpdateInstruction(cc_31, False) ]))
    st_28._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_29, [
        fac.UpdateInstruction(cc_32, True) ]))
    transitions.append(fac.Transition(st_30, [
        fac.UpdateInstruction(cc_32, False) ]))
    transitions.append(fac.Transition(st_31, [
        fac.UpdateInstruction(cc_32, False) ]))
    transitions.append(fac.Transition(st_32, [
        fac.UpdateInstruction(cc_32, False) ]))
    st_29._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_30, [
        fac.UpdateInstruction(cc_33, True) ]))
    transitions.append(fac.Transition(st_31, [
        fac.UpdateInstruction(cc_33, False) ]))
    transitions.append(fac.Transition(st_32, [
        fac.UpdateInstruction(cc_33, False) ]))
    st_30._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_31, [
        fac.UpdateInstruction(cc_34, True) ]))
    transitions.append(fac.Transition(st_32, [
        fac.UpdateInstruction(cc_34, False) ]))
    st_31._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_32, [
        fac.UpdateInstruction(cc_35, True) ]))
    st_32._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
MT300_SequenceE_ReportingInformation._Automaton = _BuildAutomaton_7()




MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ReportingJurisdiction'), MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_22L_Type, scope=MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1792, 3)))

MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ReportingParty_A'), MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_91A_Type, scope=MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1794, 4)))

MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ReportingParty_D'), MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_91D_Type, scope=MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1795, 4)))

MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ReportingParty_J'), MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_91J_Type, scope=MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1796, 4)))

MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SubSequenceE1a_UniqueTransactionIdentifier'), MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier, scope=MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1798, 3)))

def _BuildAutomaton_8 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_8
    del _BuildAutomaton_8
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1793, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1794, 4))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1795, 4))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1796, 4))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1798, 3))
    counters.add(cc_4)
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ReportingJurisdiction')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1792, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ReportingParty_A')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1794, 4))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ReportingParty_D')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1795, 4))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ReportingParty_J')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1796, 4))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SubSequenceE1a_UniqueTransactionIdentifier')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1798, 3))
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
MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties._Automaton = _BuildAutomaton_8()




MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'UTINamespaceIssuerCode'), MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_22M_Type, scope=MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1803, 3)))

MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'TransactionIdentifier'), MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_22N_Type, scope=MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1804, 3)))

MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SubSequenceE1a1_PriorUniqueTransactionIdentifier'), MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_SubSequenceE1a1_PriorUniqueTransactionIdentifier, scope=MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1805, 3)))

def _BuildAutomaton_9 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_9
    del _BuildAutomaton_9
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1805, 3))
    counters.add(cc_0)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'UTINamespaceIssuerCode')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1803, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'TransactionIdentifier')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1804, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SubSequenceE1a1_PriorUniqueTransactionIdentifier')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1805, 3))
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
MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier._Automaton = _BuildAutomaton_9()




MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_SubSequenceE1a1_PriorUniqueTransactionIdentifier._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PUTINamespaceIssuerCode'), MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_SubSequenceE1a1_PriorUniqueTransactionIdentifier_22P_Type, scope=MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_SubSequenceE1a1_PriorUniqueTransactionIdentifier, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1810, 3)))

MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_SubSequenceE1a1_PriorUniqueTransactionIdentifier._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PriorTransactionIdentifier'), MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_SubSequenceE1a1_PriorUniqueTransactionIdentifier_22R_Type, scope=MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_SubSequenceE1a1_PriorUniqueTransactionIdentifier, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1811, 3)))

def _BuildAutomaton_10 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_10
    del _BuildAutomaton_10
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_SubSequenceE1a1_PriorUniqueTransactionIdentifier._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PUTINamespaceIssuerCode')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1810, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_SubSequenceE1a1_PriorUniqueTransactionIdentifier._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PriorTransactionIdentifier')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1811, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
MT300_SequenceE_ReportingInformation_SubSequenceE1_ReportingParties_SubSequenceE1a_UniqueTransactionIdentifier_SubSequenceE1a1_PriorUniqueTransactionIdentifier._Automaton = _BuildAutomaton_10()




MT300_SequenceF_PostTradeEvents._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'EventTypeAndReference'), MT300_SequenceF_PostTradeEvents_21H_Type, scope=MT300_SequenceF_PostTradeEvents, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1816, 3)))

MT300_SequenceF_PostTradeEvents._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'UnderlyingLiabilityReference'), MT300_SequenceF_PostTradeEvents_21F_Type, scope=MT300_SequenceF_PostTradeEvents, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1817, 3)))

MT300_SequenceF_PostTradeEvents._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ProfitAndLossSettlementDate'), MT300_SequenceF_PostTradeEvents_30F_Type, scope=MT300_SequenceF_PostTradeEvents, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1818, 3)))

MT300_SequenceF_PostTradeEvents._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ProfitAndLossSettlementAmount'), MT300_SequenceF_PostTradeEvents_32H_Type, scope=MT300_SequenceF_PostTradeEvents, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1819, 3)))

MT300_SequenceF_PostTradeEvents._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'OutstandingSettlementAmount'), MT300_SequenceF_PostTradeEvents_33E_Type, scope=MT300_SequenceF_PostTradeEvents, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1820, 3)))

def _BuildAutomaton_11 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_11
    del _BuildAutomaton_11
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1817, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1818, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1819, 3))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1820, 3))
    counters.add(cc_3)
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceF_PostTradeEvents._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'EventTypeAndReference')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1816, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceF_PostTradeEvents._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'UnderlyingLiabilityReference')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1817, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceF_PostTradeEvents._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ProfitAndLossSettlementDate')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1818, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceF_PostTradeEvents._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ProfitAndLossSettlementAmount')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1819, 3))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(MT300_SequenceF_PostTradeEvents._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'OutstandingSettlementAmount')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1820, 3))
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
MT300_SequenceF_PostTradeEvents._Automaton = _BuildAutomaton_11()




CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SequenceA_GeneralInformation'), MT300_SequenceA_GeneralInformation, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1829, 4)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SequenceB_TransactionDetails'), MT300_SequenceB_TransactionDetails, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1830, 4)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SequenceC_OptionalGeneralInformation'), MT300_SequenceC_OptionalGeneralInformation, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1831, 4)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SequenceD_SplitSettlementDetails'), MT300_SequenceD_SplitSettlementDetails, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1832, 4)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SequenceE_ReportingInformation'), MT300_SequenceE_ReportingInformation, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1833, 4)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SequenceF_PostTradeEvents'), MT300_SequenceF_PostTradeEvents, scope=CTD_ANON, location=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1834, 4)))

def _BuildAutomaton_12 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_12
    del _BuildAutomaton_12
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1831, 4))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1832, 4))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1833, 4))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1834, 4))
    counters.add(cc_3)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SequenceA_GeneralInformation')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1829, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SequenceB_TransactionDetails')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1830, 4))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SequenceC_OptionalGeneralInformation')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1831, 4))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SequenceD_SplitSettlementDetails')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1832, 4))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SequenceE_ReportingInformation')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1833, 4))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SequenceF_PostTradeEvents')), pyxb.utils.utility.Location('C:\\Projects\\Code\\SwiftMessagingSolution_Python3\\base\\extensions\\SwiftIntegration\\Utilities\\XSD\\MT300.xsd', 1834, 4))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
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
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_3, True) ]))
    st_5._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON._Automaton = _BuildAutomaton_12()


