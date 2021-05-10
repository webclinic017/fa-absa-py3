# -*- coding: utf-8 -*-
# Copyright 2009-2013, Peter A. Bigot
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain a
# copy of the License at:
#
#            http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""Binding classes for types referenced by the attribute and attribute
group declarations in the XML namespace
(http://www.w3.org/XML/1998/namespace).

The content of this module was generated by PyXB and is coupled to the
components defined in L{pyxb.namespace.builtin._XML}.

"""

# ./pyxb/standard/bindings/raw/xml_.py
# PyXB bindings for NamespaceModule
# Generated 2009-07-25 13:37:53.257717 by PyXB version 0.5.2
import pyxb
import pyxb.binding
import pyxb.utils.utility
import pyxb.utils.domutils
from pyxb.utils import six

# Unique identifier for bindings created at the same time
_GenerationUID = pyxb.namespace.builtin.BuiltInObjectUID

# Import bindings for namespaces imported into schema

Namespace = pyxb.namespace.NamespaceForURI('http://www.w3.org/XML/1998/namespace', create_if_missing=True)

# Atomic SimpleTypeDefinition
class STD_ANON_space (pyxb.binding.datatypes.NCName, pyxb.binding.basis.enumeration_mixin):
    """No information"""

    _ExpandedName = None
STD_ANON_space._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_space, enum_prefix=None)
STD_ANON_space.default = STD_ANON_space._CF_enumeration.addEnumeration(unicode_value=six.u('default'))
STD_ANON_space.preserve = STD_ANON_space._CF_enumeration.addEnumeration(unicode_value=six.u('preserve'))
STD_ANON_space._InitializeFacetMap(STD_ANON_space._CF_enumeration)

# Atomic SimpleTypeDefinition
class STD_ANON_emptyString (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):
    """No information"""

    _ExpandedName = None
STD_ANON_emptyString._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_emptyString, enum_prefix=None)
STD_ANON_emptyString.emptyString = STD_ANON_emptyString._CF_enumeration.addEnumeration(unicode_value=six.u(''))
STD_ANON_emptyString._InitializeFacetMap(STD_ANON_emptyString._CF_enumeration)

# Union SimpleTypeDefinition
# superclasses pyxb.binding.datatypes.anySimpleType
class STD_ANON_lang (pyxb.binding.basis.STD_union):
    """Simple type that is a union of pyxb.binding.datatypes.language, STD_ANON_emptyString"""

    _ExpandedName = None
    _MemberTypes = ( pyxb.binding.datatypes.language, STD_ANON_emptyString, )
STD_ANON_lang._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_lang)
STD_ANON_lang._CF_pattern = pyxb.binding.facets.CF_pattern()
STD_ANON_lang._InitializeFacetMap(STD_ANON_lang._CF_enumeration,
   STD_ANON_lang._CF_pattern)

