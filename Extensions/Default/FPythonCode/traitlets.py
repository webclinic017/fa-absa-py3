# encoding: utf-8
from __future__ import print_function
"""
A lightweight Traits like module.

This is designed to provide a lightweight, simple, pure Python version of
many of the capabilities of enthought.traits.  This includes:

* Validation
* Type specification with defaults
* Static and dynamic notification
* Basic predefined types
* An API that is similar to enthought.traits

We don't support:

* Delegation
* Automatic GUI generation
* A full set of trait types.  Most importantly, we don't provide container
  traits (list, dict, tuple) that can trigger notifications if their
  contents change.
* API compatibility with enthought.traits

There are also some important difference in our design:

* enthought.traits does not validate default values.  We do.

We choose to create this module because we need these capabilities, but
we need them to be pure Python so they work in all Python implementations,
including Jython and IronPython.

Inheritance diagram:

.. inheritance-diagram:: IPython.utils.traitlets
   :parts: 3

Authors:

* Brian Granger
* Enthought, Inc.  Some of the code in this file comes from enthought.traits
  and is licensed under the BSD license.  Also, many of the ideas also come
  from enthought.traits even though our implementation is very different.
"""

#-----------------------------------------------------------------------------
#  Copyright (C) 2008-2011  The IPython Development Team
#
#  Distributed under the terms of the BSD License.  The full license is in
#  the file COPYING, distributed as part of this software.
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------


import inspect
import re
import sys
import types
from types import FunctionType
from TraitUtil import ExceptionAccumulator, AttributeException
try:
    from types import ClassType, InstanceType
    ClassTypes = (ClassType, type)
except:
    ClassTypes = (type,)

class AddTraitChangingWithSafeExit(object):
    def __init__(self, hasTraitsInstance, name):
        self._hasTraitsInstance = hasTraitsInstance
        self._name = name
    def __enter__(self):
        if self.__HasTraitsChanging():
            self.__TraitsChanging().append(self._name)
    def __exit__(self, type, value, traceback):
        if self.__HasTraitsChanging():
            traitsChanging = self.__TraitsChanging()
            if len(traitsChanging):
                traitsChanging.pop()

    def __HasTraitsChanging(self):
        return self.__TraitsChanging() is not None
    def __TraitsChanging(self):
        traitsChanging = None
        if hasattr(self._hasTraitsInstance, '_traitsChanging'):
            traitsChanging = self._hasTraitsInstance._traitsChanging
        return traitsChanging

def import_item(name):
    """Import and return ``bar`` given the string ``foo.bar``.

    Calling ``bar = import_item("foo.bar")`` is the functional equivalent of
    executing the code ``from foo import bar``.

    Parameters
    ----------
    name : string
      The fully qualified name of the module/package being imported.

    Returns
    -------
    mod : module object
       The module that was imported.
    """

    parts = name.rsplit('.', 1)
    if len(parts) == 2:
        # called with 'foo.bar....'
        package, obj = parts
        module = __import__(package, fromlist=[obj])
        try:
            pak = module.__dict__[obj]
        except KeyError:
            raise ImportError('No module named %s' % obj)
        return pak
    else:
        # called with un-dotted string
        return __import__(parts[0])


SequenceTypes = (list, tuple, set, frozenset)

#-----------------------------------------------------------------------------
# Basic classes
#-----------------------------------------------------------------------------


class NoDefaultSpecified ( object ): pass
NoDefaultSpecified = NoDefaultSpecified()


class Undefined ( object ): pass
Undefined = Undefined()
    
#-----------------------------------------------------------------------------
# Utilities
#-----------------------------------------------------------------------------


def class_of ( object ):
    """ Returns a string containing the class name of an object with the
    correct indefinite article ('a' or 'an') preceding it (e.g., 'an Image',
    'a PlotValue').
    """
    if isinstance( object, basestring ):
        return add_article( object )

    return add_article( object.__class__.__name__ )


def add_article ( name ):
    """ Returns a string containing the correct indefinite article ('a' or 'an')
    prefixed to the specified string.
    """
    if name[:1].lower() in 'aeiou':
       return 'an ' + name

    return 'a ' + name


def repr_type(obj):
    """ Return a string representation of a value and its type for readable
    error messages.
    """
    the_type = type(obj)
    if the_type is InstanceType:
        # Old-style class.
        the_type = obj.__class__
    msg = '%r %r' % (obj, the_type)
    return msg


def is_trait(t):
    """ Returns whether the given value is an instance or subclass of TraitType.
    """
    return (isinstance(t, TraitType) or
            (isinstance(t, type) and issubclass(t, TraitType)))


def parse_notifier_name(name):
    """Convert the name argument to a list of names.

    Examples
    --------

    >>> parse_notifier_name('a')
    ['a']
    >>> parse_notifier_name(['a','b'])
    ['a', 'b']
    >>> parse_notifier_name(None)
    ['anytrait']
    """
    if isinstance(name, str):
        return [name]
    elif name is None:
        return ['anytrait']
    elif isinstance(name, (list, tuple)):
        for n in name:
            assert isinstance(n, str), "names must be strings"
        return name


def getmembers(obj, predicate=None):
    """A safe version of inspect.getmembers that handles missing attributes.

    This is useful when there are descriptor based attributes that for
    some reason raise AttributeError even though they exist.  This happens
    in zope.inteface with the __provides__ attribute.
    """
    results = []
    for key in dir(obj):
        try:
            value = object.__getattribute__(obj, key)
        except AttributeError:
            pass
        else:
            if not predicate or predicate(value):
                results.append((key, value))
    results.sort()
    return results


#-----------------------------------------------------------------------------
# Base TraitType for all traits
#-----------------------------------------------------------------------------

def static_vars(**kwargs):
    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func
    return decorate

@static_vars(counter=0)
def NextTraitSeqNbr():
    NextTraitSeqNbr.counter += 1
    return NextTraitSeqNbr.counter
    
class TraitType(object):
    """A base class for all trait descriptors.

    Notes
    -----
    Our implementation of traits is based on Python's descriptor
    prototol.  This class is the base class for all such descriptors.  The
    only magic we use is a custom metaclass for the main :class:`HasTraits`
    class that does the following:

    1. Sets the :attr:`name` attribute of every :class:`TraitType`
       instance in the class dict to the name of the attribute.
    2. Sets the :attr:`this_class` attribute of every :class:`TraitType`
       instance in the class dict to the *class* that declared the trait.
       This is used by the :class:`This` trait to allow subclasses to
       accept superclasses for :class:`This` values.
    """


    metadata = {}
    default_value = Undefined
    
    def __init__(self, defaultValue=NoDefaultSpecified, **metadata):
        """Create a TraitType.
        """
        self.creation_seqnbr = NextTraitSeqNbr()
        if defaultValue is not NoDefaultSpecified:
            self.default_value = defaultValue
            self.explicit_default_value = True
        else:
            self.explicit_default_value = False
                
        if len(metadata) > 0:
            if len(self.metadata) > 0:
                self._metadata = self.metadata.copy()
                self._metadata.update(metadata)
            else:
                self._metadata = metadata
        else:
            self._metadata = self.metadata.copy()
        self._metadata = {k: [v] for (k, v) in self._metadata.iteritems()}

        self.init()
        self.dirty = False

    def init(self):
        pass

    def get_default_value(self):
        """Create a new instance of the default value."""
        return self.default_value
        
    def has_explicit_default_value(self):
        """Default value explicit on creation."""
        return self.explicit_default_value
        
    def AttributeExceptionAccumulator(self):
        return self.error_accumulator
        
    def instance_init(self, obj):
        """This is called by :meth:`HasTraits.__new__` to finish init'ing.

        Some stages of initialization must be delayed until the parent
        :class:`HasTraits` instance has been created.  This method is
        called in :meth:`HasTraits.__new__` after the instance has been
        created.

        This method trigger the creation and validation of default values
        and also things like the resolution of str given class names in
        :class:`Type` and :class`Instance`.

        Parameters
        ----------
        obj : :class:`HasTraits` instance
            The parent :class:`HasTraits` instance that has just been
            created.
        """
        self.set_default_value(obj)
        self.error_accumulator = ExceptionAccumulator(obj)
        self._metadata = {k: list(v) for (k, v) in self._metadata.iteritems()}
    
    def get_name(self):
        return self._attr_name
    
    def set_name(self, name):
        self._attr_name = name
    
    def set_default_value(self, obj):
        """Set the default value on a per instance basis.

        This method is called by :meth:`instance_init` to create and
        validate the default value.  The creation and validation of
        default values must be delayed until the parent :class:`HasTraits`
        class has been instantiated.
        """
        # Check for a deferred initializer defined in the same class as the
        # trait declaration or above.
        mro = type(obj).mro()
        
        if self._attr_name.startswith('_'):
            meth_name = '_%s_default' % self._attr_name[1:]
        else:
            meth_name = '_%s_default' % self._attr_name

        for cls in mro[:mro.index(self.this_class)+1]:
            if meth_name in cls.__dict__:
                break
        else:
            # We didn't find one.
            return
        # Complete the dynamic initialization.
        obj._trait_dyn_inits[self._attr_name] = cls.__dict__[meth_name]
        
    def get_value(self, obj):
        """Get the value of the trait by self._attr_name for the instance.

        Default values are instantiated when :meth:`HasTraits.__new__`
        is called.  Thus by the time this method gets called either the
        default value or a user defined value (they called :meth:`__set__`)
        is in the :class:`HasTraits` instance.
        """

        if obj is None:
            return self
        else:
            try:
                if self.dirty and self._attr_name in obj._trait_values:
                    obj._ApplyLatestValueFromObjMapping(self._attr_name)
                    self.dirty = False
                value = obj._trait_values[self._attr_name]
            except KeyError:
                # Check for a dynamic initializer.
                if self._attr_name in obj._trait_dyn_inits:
                    value = obj._trait_dyn_inits[self._attr_name](obj)
                    # FIXME: Do we really validate here?
                    value = self._validate(obj, value)
                    obj._trait_values[self._attr_name] = value
                else:
                    obj.HandleNoDefaultValue(self._attr_name)
                    
                try:
                    value = obj._trait_values[self._attr_name]
                except KeyError:
                    dv = self.get_default_value()
                    obj._trait_values[self._attr_name] = dv
                    return dv
                else:
                    return value
            except Exception:
                # HasTraits should call set_default_value to populate
                # this.  So this should never be reached.
                raise AttributeException('Unexpected error in TraitType: '
                                    'default value not set properly')
            else:
                return value
    
    def set_value(self, obj, new_value):
        old_value = self.get_value(obj)
        new_value = self._transform_validate_applyObjMapping(obj, new_value, old_value)
        self.dirty = False
        self.do_set(obj, new_value, old_value)
        self.AttributeExceptionAccumulator().Clear()
        
    def _transform_validate_applyObjMapping(self, obj, new_value, old_value):
        if obj._applyTraitChangeAndCallObjMappingSetMethod:
            new_value = self._transform(obj, new_value)
            if obj.force_apply_obj_mappings(self._attr_name) or not obj._trait_values_are_equal(new_value, old_value, checkOriginator=False):
                new_value = self._validate(obj, new_value)
                new_value = self._applyObjMapping(obj, new_value)
        return new_value

    def do_set(self, obj, new_value, old_value):
        if not obj._muteNotifications and obj._GetSolverTopValue(self._attr_name):
            obj._SolveForTrait(self._attr_name, new_value)
        else:
            obj._trait_values[self._attr_name] = new_value
            self.dirty = False
            if obj._applyTraitChangeAndCallObjMappingSetMethod and not obj._trait_values_are_equal(new_value, old_value):
                obj._notify_trait(self._attr_name, old_value, new_value)

    def _transform(self, obj, value):
        if hasattr(self, 'transform'):
            value = self.transform(obj, value)
        return value

    def transform(self, obj, value):
        return value
        
    def _applyObjMapping(self, obj, value):
        if hasattr(self, 'applyObjMapping'):
            value = self.applyObjMapping(obj, value)
        return value
        
    def applyObjMapping(self, obj, value):
        return value
    
    def _validate(self, obj, value):
        if hasattr(self, 'validate'):
            return self.validate(obj, value)
        elif hasattr(self, 'is_valid_for'):
            valid = self.is_valid_for(value)
            if valid:
                return value
            else:
                raise AttributeException('invalid value for type: %r' % value)
        elif hasattr(self, 'value_for'):
            return self.value_for(value)
        else:
            return value

    def get_metadata(self, key):
        return self.get_complete_metadata(key)[-1]
        
    def get_complete_metadata(self, key):
        return getattr(self, '_metadata', {}).get(key, [None])

    def set_metadata(self, key, value):
        getattr(self, '_metadata', {})[key] = [value]
    
    def append_metadata(self, obj, key, value):
        if key == 'defaultValue': # Default value handled differently
            self.explicit_default_value = True
            self.default_value = value
            # Fix cached value of default_value. Is earlier set in instance_init
            obj._trait_values[self._attr_name] = self.get_default_value()
        else:
            metadatalist = self._metadata.setdefault(key, [None])
            metadatalist.append(value)
    
    def get_metadata_keys(self):
        return self._metadata.keys()

    def set_dirty(self):
        self.dirty = True

#-----------------------------------------------------------------------------
# The HasTraits implementation
#-----------------------------------------------------------------------------


class MetaHasTraits(type):
    """A metaclass for HasTraits.

    This metaclass makes sure that any TraitType class attributes are
    instantiated and sets their name attribute.
    """

    def __new__(mcls, name, bases, classdict):
        """Create the HasTraits class.

        This instantiates all TraitTypes in the class dict and sets their
        :attr:`name` attribute.
        """
        # print ("MetaHasTraitlets (mcls, name): ", mcls, name)
        # print ("MetaHasTraitlets (bases): ", bases)
        # print ("MetaHasTraitlets (classdict): ", classdict)
        for k, v in classdict.iteritems():
            if isinstance(v, TraitType):
                v._attr_name = k
            elif inspect.isclass(v):
                if issubclass(v, TraitType):
                    vinst = v()
                    vinst._attr_name = k
                    classdict[k] = vinst
        
        return super(MetaHasTraits, mcls).__new__(mcls, name, bases, classdict)

    def __init__(cls, name, bases, classdict):
        """Finish initializing the HasTraits class.

        This sets the :attr:`this_class` attribute of each TraitType in the
        class dict to the newly created class ``cls``.
        """
        for k, v in classdict.iteritems():
            if isinstance(v, TraitType):
                v.this_class = cls
        super(MetaHasTraits, cls).__init__(name, bases, classdict)
    
class HasTraits(object):
    __metaclass__ = MetaHasTraits

    def __new__(cls, *args, **kw):
        # This is needed because in Python 2.6 object.__new__ only accepts
        # the cls argument.
        new_meth = super(HasTraits, cls).__new__
        if new_meth is object.__new__:
            inst = new_meth(cls)
        else:
            inst = new_meth(cls, **kw)
        inst._trait_values = {}
        inst._trait_prioritized_notifiers = {}
        inst._trait_post_notifiers = {}
        inst._trait_notifiers = {}
        inst._trait_dyn_inits = {}
        # Here we tell all the TraitType instances to set their default
        # values on the instance.
        for key in dir(inst):
            # Some descriptors raise AttributeError like zope.interface's
            # __provides__ attributes even though they exist.  This causes
            # AttributeErrors even though they are listed in dir(cls).
            try:
                value = object.__getattribute__(inst, key)
            except AttributeError:
                pass
            else:
                if isinstance(value, TraitType):
                    import copy
                    newValue = copy.copy(value)
                    setattr(inst, key, newValue)
                    newValue.instance_init(inst)
        
        return inst

    def __init__(self, *args, **kw):
        # Allow trait values to be set using keyword arguments.
        # We need to use setattr for this to trigger validation and
        # notifications.
        self._muteNotifications = False
        self._traitsChanging = []
        self._applyTraitChangeAndCallObjMappingSetMethod = True
        self._registeringAllObjMappingsOnNew = False
        
        self.instanceTraits = None
        self.domainDict = {}
        self.classTraits = None
        for key, value in kw.iteritems():
            setattr(self, key, value)

    def _send_notifications(self, userInputTraitName, changedTraitsDict):
        with AddTraitChangingWithSafeExit(self, userInputTraitName):
            for name in changedTraitsDict.iterkeys():
                old_value = changedTraitsDict.get(name)[1]
                current_value = getattr(self, name)
                if not self._trait_values_are_equal(current_value, old_value):
                    with AddTraitChangingWithSafeExit(self, name):
                        self._notify_trait(name, old_value, current_value, userInputTraitName)
        
    def _check_is_nan(self, value):
        # Check Not-A-Number, since #new_value != new_value -> False for float('nan')
        return value != value
        
    def _originator(self, value):
        if hasattr(value, 'Originator'):
            value = value.Originator()
        return value
            
    def _value_originators_are_equal(self, new_value, old_value):
        return self._originator(new_value) == self._originator(old_value)
    
    def _trait_values_are_equal(self, new_value, old_value, checkOriginator=True):
        equal = False
        if old_value == new_value:
            equal = True
        elif isinstance(old_value, float) and isinstance(new_value, float) and abs(old_value - new_value) < 1e-12:
            equal = True
        elif checkOriginator and self._value_originators_are_equal(new_value, old_value):
            equal = True
        else:
            equal = self._check_is_nan(old_value) and self._check_is_nan(new_value)
        return equal 
    
    def HasOnChanged(self, name):
        onChanged = bool(self._trait_notifiers.get(name, []))
        return onChanged or bool(self._underscored_onchanged(name))
    
    def _underscored_onchanged(self, name):
        cb = None
        try:
            if name.startswith('_'):
                cb_name = name[1:]
            else:
                cb_name = name
            cb = getattr(self, '_%s_changed' % cb_name)
        except:
            pass
        return cb
    
    def _notify_trait(self, name, old_value, new_value, userInputTraitName = None):
        
        if self._muteNotifications:
            return
        
        # First dynamic ones
        callables = []
        
        prioritized_callables = self._trait_prioritized_notifiers.get('anytrait', [])
        anytrait_callables = self._trait_notifiers.get('anytrait', [])
        name_specific_callables = self._trait_notifiers.get(name, [])
        callables.extend(prioritized_callables)
        callables.extend(anytrait_callables)
        callables.extend(name_specific_callables)
    
        # Now static ones
        cb = self._underscored_onchanged(name)
        if cb:
            callables.append(cb)

        post_callables = self._trait_post_notifiers.get('anytrait', [])
        callables.extend(post_callables)

        userInputTraitName = None
        if hasattr(self, '_traitsChanging') and self._traitsChanging and len(self._traitsChanging) > 1:
            userInputTraitName = self._traitsChanging[0]
       
        # Call them all now
        for c in callables:
            # Traits catches and logs errors here.  I allow them to raise
            if callable(c):
                allCallArgs = (name, old_value, new_value, userInputTraitName)
                c(*allCallArgs)
            else:
                raise AttributeException('an attribute changed callback '
                                    'must be callable.')


    def _add_notifiers(self, handler, name):
        if name not in self._trait_notifiers:
            nlist = []
            self._trait_notifiers[name] = nlist
        else:
            nlist = self._trait_notifiers[name]
        if handler not in nlist:
            nlist.append(handler)

    def _remove_notifiers(self, handler, name):
        if name in self._trait_notifiers:
            nlist = self._trait_notifiers[name]
            try:
                index = nlist.index(handler)
            except ValueError:
                pass
            else:
                del nlist[index]
    def _add_post_notifiers(self, handler, name):
        if name not in self._trait_post_notifiers:
            nlist = []
            self._trait_post_notifiers[name] = nlist
        else:
            nlist = self._trait_post_notifiers[name]
        if handler not in nlist:
            nlist.append(handler)

    def _remove_post_notifiers(self, handler, name):
        if name in self._trait_post_notifiers:
            nlist = self._trait_post_notifiers[name]
            try:
                index = nlist.index(handler)
            except ValueError:
                pass
            else:
                del nlist[index]

    def _add_prioritized_notifiers(self, handler, name):
        if name not in self._trait_prioritized_notifiers:
            nlist = []
            self._trait_prioritized_notifiers[name] = nlist
        else:
            nlist = self._trait_prioritized_notifiers[name]
        if handler not in nlist:
            nlist.append(handler)
            
    def on_obj_mapping_trait_change(self, handler):
        self._add_prioritized_notifiers(handler, 'anytrait')
        
    def on_trait_change(self, handler, name=None, remove=False):
        """Setup a handler to be called when a trait changes.

        This is used to setup dynamic notifications of trait changes.

        Static handlers can be created by creating methods on a HasTraits
        subclass with the naming convention '_[traitname]_changed'.  Thus,
        to create static handler for the trait 'a', create the method
        _a_changed(self, name, old, new) (fewer arguments can be used, see
        below).

        Parameters
        ----------
        handler : callable
            A callable that is called when a trait changes.  Its
            signature can be handler(), handler(name), handler(name, new)
            or handler(name, old, new).
        name : list, str, None
            If None, the handler will apply to all traits.  If a list
            of str, handler will apply to all names in the list.  If a
            str, the handler will apply just to that name.
        remove : bool
            If False (the default), then install the handler.  If True
            then unintall it.
        """
        if remove:
            names = parse_notifier_name(name)
            for n in names:
                self._remove_notifiers(handler, n)
        else:
            names = parse_notifier_name(name)
            for n in names:
                self._add_notifiers(handler, n)
    
    def on_post_trait_change(self, handler, name=None, remove=False):
       
        if remove:
            names = parse_notifier_name(name)
            for n in names:
                self._remove_post_notifiers(handler, n)
        else:
            names = parse_notifier_name(name)
            for n in names:
                self._add_post_notifiers(handler, n)

    def trait_names(self):
        """Get a list of all the names of this classes traits."""
        return self.traits().keys()

    def UpdateInstanceTraits(self, name, trait):
        self.instanceTraits[name] = trait

    def traits(self):
        """Get a list of all the traits of this class.

        The TraitTypes returned don't know anything about the values
        that the various HasTrait's instances are holding.
        """
        if not self.instanceTraits:
            self.instanceTraits = dict([memb for memb in getmembers(self) if \
                         isinstance(memb[1], TraitType)])
        return self.instanceTraits

    def __trait(self, traitname):
        """Get metadata values for trait by key."""
        try:
            trait = object.__getattribute__(self, traitname)
        except AttributeError:
            raise AttributeException("Class %s does not have an attribute named %s" %
                                (self.__class__.__name__, traitname))
        else:
            return trait

    def HandleNoDefaultValue(self, traitname):
        pass

    def trait_metadata(self, traitname, key):
        return self.__trait(traitname).get_metadata(key)
    
    def complete_trait_metadata(self, traitname, key):
        return self.__trait(traitname).get_complete_metadata(key)
    
    def __getattribute__(self, name):
        obj = super(HasTraits, self).__getattribute__(name)
        if isinstance(obj, TraitType):
            return obj.get_value(self)
        else:
            return obj

    def __setattr__(self, name, value):
        with AddTraitChangingWithSafeExit(self, name):
            if isinstance(value, TraitType):
                super(HasTraits, self).__setattr__(name, value)
            else:
                try:
                    obj = super(HasTraits, self).__getattribute__(name)
                    set_value = obj.set_value
                except AttributeError:
                    super(HasTraits, self).__setattr__(name, value)
                else:
                    set_value(self, value)
                    
    def force_apply_obj_mappings(self, traitName):
        return False
                

#-----------------------------------------------------------------------------
# Actual TraitTypes implementations/subclasses
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# TraitTypes subclasses for handling classes and instances of classes
#-----------------------------------------------------------------------------

class DefaultValueGenerator(object):
    """A class for generating new default value instances."""

    def __init__(self, *args, **kw):
        self.args = args
        self.kw = kw

    def generate(self, klass):
        return klass(*self.args, **self.kw)


class Instance(TraitType):
    """A trait whose value must be an instance of a specified class.

    The value can also be an instance of a subclass of the specified class.
    """

    def __init__(self, klass=None, args=None, kw=None, **metadata ):
        """Construct an Instance trait.

        This trait allows values that are instances of a particular
        class or its sublclasses.  Our implementation is quite different
        from that of enthough.traits as we don't allow instances to be used
        for klass and we handle the ``args`` and ``kw`` arguments differently.

        Parameters
        ----------
        klass : class, str
            The class that forms the basis for the trait.  Class names
            can also be specified as strings, like 'foo.bar.Bar'.
        args : tuple
            Positional arguments for generating the default value.
        kw : dict
            Keyword arguments for generating the default value.
        
        Default Value
        -------------
        If both ``args`` and ``kw`` are None, then the default value is None.
        If ``args`` is a tuple and ``kw`` is a dict, then the default is
        created as ``klass(*args, **kw)``.  If either ``args`` or ``kw`` is
        not (but not both), None is replace by ``()`` or ``{}``.
        """

        if (klass is None) or (not (inspect.isclass(klass) or isinstance(klass, basestring))):
            raise AttributeException('The klass argument must be a class'
                                ' you gave: %r' % klass)
        self.klass = klass

        # self.klass is a class, so handle default_value
        if args is None and kw is None:
            default_value = None
        else:
            if args is None:
                # kw is not None
                args = ()
            elif kw is None:
                # args is not None
                kw = {}

            if not isinstance(kw, dict):
                raise AttributeException("The 'kw' argument must be a dict or None.")
            if not isinstance(args, tuple):
                raise AttributeException("The 'args' argument must be a tuple or None.")

            default_value = DefaultValueGenerator(*args, **kw)

        super(Instance, self).__init__(default_value, **metadata)

    def instance_init(self, obj):
        self._resolve_classes()
        super(Instance, self).instance_init(obj)

    def _resolve_classes(self):
        if isinstance(self.klass, basestring):
            self.klass = import_item(self.klass)

    def has_explicit_default_value(self):
        """Default value explicit on creation."""
        return False
    
    def validate(self, obj, value):
        if isinstance(value, self.klass) or value is None:
            return value
        else:
            e = "The '%s' attribute must be %s, but a value of %r was specified." \
                % (self._attr_name, self.klass, repr_type(value))
            raise AttributeError(e)

    def get_default_value(self):            
        """Instantiate a default value instance.

        This is called when the containing HasTraits classes'
        :meth:`__new__` method is called to ensure that a unique instance
        is created for each HasTraits instance.
        """
        dv  = self.default_value
        if isinstance(dv, DefaultValueGenerator):
            return dv.generate(self.klass)
            
        else:
            return dv

#-----------------------------------------------------------------------------
# Basic TraitTypes implementations/subclasses
#-----------------------------------------------------------------------------


class Any(TraitType):
    default_value = None
    

class Int(TraitType):
    """An int trait."""

    default_value = 0
    

class Float(TraitType):
    """A float trait."""

    default_value = 0.0


# We should always be explicit about whether we're using bytes or unicode, both
# for Python 3 conversion and for reliable unicode behaviour on Python 2. So
# we don't have a Str type.
class Bytes(TraitType):
    """A trait for byte strings."""

    default_value = ''
    

class Bool(TraitType):
    """A boolean (True, False) trait."""

    default_value = False
    

class Container(Instance):
    """An instance of a container (list, set, etc.)

    To be subclassed by overriding klass.
    """
    klass = None
    _valid_defaults = SequenceTypes

    def __init__(self, defaultValue=None, **metadata):
        """Create a container trait type from a list, set, or tuple.

        The default value is created by doing ``List(defaultValue)``,
        which creates a copy of the ``defaultValue``.

        ``c = List([1,2,3])``

        Parameters
        ----------

        defaultValue : SequenceType [ optional ]
            The default value for the Trait.  Must be list/tuple/set, and
            will be cast to the container type.

        **metadata : any
            further keys for extensions to the Trait (e.g. config)

        """
        if defaultValue is None:
            args = ()
        elif isinstance(defaultValue, self._valid_defaults):
            args = (defaultValue,)
        else:
            raise TypeError('default value of %s was %s' %(self.__class__.__name__, defaultValue))

        super(Container, self).__init__(klass=self.klass, args=args, **metadata)


class List(Container):
    """An instance of a Python list."""
    klass = list


class Set(Container):
    """An instance of a Python set."""
    klass = set
