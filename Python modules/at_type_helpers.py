"""
:Author: Andreas Bayer <Andreas.Bayer@absacapital.com; Andreas.Bayer@d-fine.de>
:Version: 0.1, 2014/02/15
:Summary: helper functions for working with python, acm and ael types

History
=======
- 2014-02-15  Andreas Bayer, created

General functions
=================
`dedup(seq)`_
    - return list of elements in sequence seq with duplicates removed
`funcname()`_
    - return name of current function
`short_type_name(type)`_
    - return short name of type *type* with special support
      for ACM and AEL types (ael.ael_table objects and acm classes)
`to_bool(obj)`_
    - converts object to bool with special logic for strings

ACM/AEL functions
=================
`find_unique_or_primary_key(obj)`_ 
    - find name of unique or primary key property for ACM or AEL objects.
`get_property(obj, name, *args)`_
    - get property (ACM) or attribute (AEL)
`get_unique_or_primary_key(obj, *args)`_ 
    - return value of unique or primary key property found by 
      find_unique_or_primary_key()
`is_acm(obj)`_
    - return True if obj is an ACM object, False otherwise
`is_acm_class(obj)`_ 
    - return True if obj is an ACM class, False otherwise.
`isinstance(obj, classinfo)`_ 
    - acm-aware version of isinstance()
`to_acm(e, acm_class = None)`_
    - convert e to an acm_class
`to_ael(obj, ael_class=None)`_
    - convert e to an ael_class
`xrepr(obj)`_
    - ACM/AEL aware version of repr()
`xstr(obj, none_string='None')`_
    - ACM/AEL aware version of str()
"""

import inspect
import re
import sys

try:
    import acm
    import ael
except ImportError:
    pass


__all__ = [
    # general functions
    'dedup',
    'funcname',
    'short_type_name',
    'to_bool',

    # acm/ael functions
    'find_unique_or_primary_key',
    'get_property',
    'get_unique_or_primary_key',
    'is_acm',
    'is_acm_class',
    'isinstance',
    'to_acm',
    'to_ael',
    'xrepr',
    'xstr',
]


# ----------------------------------------------------------------------------
# Global variables
# ----------------------------------------------------------------------------

# create a module-local reference to the isinstance() function in the
# __builtin__ module. This reference is used in the isinstance() function.

try:
    _saved_builtins
except NameError:
    _saved_builtins = {}

def _fill_saved_builtins_():
    """Copy some built-in functions to _saved_builtins"""    
    for name in ('isinstance', 'repr', 'str'):
        if name not in _saved_builtins:
            _saved_builtins[name] = getattr(sys.modules['__builtin__'], name)

_fill_saved_builtins_()

_undefined = object()

# ----------------------------------------------------------------------------
# General Functions
# ----------------------------------------------------------------------------

def dedup(seq):
    """.. _`dedup(seq)`:
    
    Return list of elements in sequence seq with duplicate elements removed.
    The returned list is a newly created list, seq is not modified.
    """

    return list(set(seq))

def funcname():
    """
    .. _`funcname()`:
    
    Return name of current function

    >>> def foo_func():
    ...     return funcname()
    >>> foo_func()
    'foo_func'
    >>> funcname()
    '<module>'
    >>> def foo():
    ...     print repr(funcname())
    >>> foo()
    'foo'
    """
    
    try:
        frame = inspect.currentframe().f_back
        return inspect.getframeinfo(frame).function
    except:
        return None

def short_type_name(type_):
    """
    .. _`short_type_name(type)`:
    
    Return short name of type type, works for AEL and ACM classes.

    >>> short_type_name(ael.Trade)
    'ael.Trade'
    >>> short_type_name(acm.FTrade)
    'acm.FTrade'
    >>> short_type_name(dict)
    'dict'
    >>> import datetime
    >>> short_type_name(datetime.date)
    'datetime.date'
    """
    name = str(type_)
    if 'ael' in sys.modules:
        if isinstance(type_, ael.ael_table):
            # whacky hack to extract name of AEL class from type.
            # Since the name is hopefully only used for error reporting,
            # failures are not a big problem
            try:
                # str(ael.Trade) is something like
                # '<ael table, Trade at 2449250>', so we split by comma (','),
                # strip spaces and finally split by white space.
                name = 'ael.' + name.split(',')[1].strip().split()[0]
            except:
                # some error: Just keep the original type_name
                pass
    if is_acm_class(type_):
        name = 'acm.' + str(type_.Name())
    elif name.startswith('<type'):
        name = re.sub(r"<type *\'(.*)\'>", r'\1', name)
    elif name.startswith('<class'):
        name = re.sub(r"<class *\'(.*)\'>", r'\1', name)
    return name

def to_bool(obj):
    """
    .. _`to_bool(obj)`:
    
    Return boolean value of obj.

    If obj is not a string then the built-in bool() function is used.
    For strings the input string obj is stripped (leading and trailing
    whitespace are removed) and converted to lowercase. Then the following
    tests are done:
    - return False if the string is one of '0', '0.0', 'f', 'false', 'no',
    or 'off'
    - return True if the string is one of '1', 't', 'true', 'yes', or 'on'
    - otherwise a ValueError exception is raised

    >>> to_bool(True)
    True
    >>> to_bool(False)
    False
    >>> to_bool(None)
    False
    >>> to_bool([])
    False
    >>> to_bool([1, 2])
    True
    >>> to_bool(())
    False
    >>> to_bool((1, 2))
    True
    >>> to_bool(1)
    True
    >>> to_bool(0)
    False
    >>> to_bool(0.0)
    False
    >>> to_bool('trUE')
    True
    >>> to_bool('')
    Traceback (most recent call last):
        ...
    ValueError: Can not convert '' to bool
    >>> to_bool(' f ')
    False
    >>> to_bool(' t ')
    True
    """
    if isinstance(obj, basestring):
        lstring = obj.lower().strip()
        if lstring in ('0', '0.0', 'f', 'false', 'no', 'off'):
            return False
        elif lstring in ('1', 't', 'true', 'yes', 'on'):
            return True
        else:
            raise ValueError('Can not convert %r to bool' % obj)
    else:
        return bool(obj)


# ----------------------------------------------------------------------------
# ACM/AEL Functions
# ----------------------------------------------------------------------------

def find_unique_or_primary_key(obj):
    """
    .. _`find_unique_or_primary_key(obj)`:
    
    Find unique or primary key property for ACM or AEL object

    >>> find_unique_or_primary_key(ael.Instrument['ZAR/MTN'])
    'insid'
    >>> find_unique_or_primary_key(acm.FInstrument['ZAR/MTN'])
    'Name'
    >>> find_unique_or_primary_key(ael.Instrument)
    'insid'
    >>> find_unique_or_primary_key(ael.Trade)
    'trdnbr'
    >>> find_unique_or_primary_key(acm.FTrade)
    'Name'
    """
    if is_acm_class(obj):
        try:
            uprop = str(obj.UniqueProperty())
            if uprop:
                return uprop
        except:
            pass
        if hasattr(obj, 'Name'):
            return 'Name'
        elif hasattr(obj, 'Oid'):
            return 'Oid'
    elif is_acm(obj):
        try:
            uprop = str(obj.Class().UniqueProperty())
            if uprop:
                return uprop
        except:
            pass
        if hasattr(obj, 'StringKey'):
            return 'StringKey'
        elif hasattr(obj, 'Name'):
            return 'Name'
        elif hasattr(obj, 'Oid'):
            return 'Oid'
    else:
        try:
            if isinstance(obj, ael.ael_table):
                table = obj
            else:
                table = getattr(ael, obj.record_type)
            pkey = None
            for key in table.keys():
                if key[1] == 'unique':
                    return key[0]
                elif key[1] == 'primary':
                    pkey = key[0]
            if pkey:
                return pkey
        except:
            pass
    raise TypeError('No AEL/ACM unique or primary key for %r' % obj)

def get_property(obj, name, default=None):
    """
    .. _`get_property(obj, name, default)`:
    
    Return named property / attribute of obj for ACM and AEL objects.

    If the named property (attribute for AEL objects) does not exist,
    default is returned. If default is not provided then an
    AttributeError is raised.

    >>> get_property(acm.FInstrument['ZAR/MTN'], 'Name')
    'ZAR/MTN'
    >>> get_property(ael.Instrument['ZAR/MTN'], 'insid')
    'ZAR/MTN'
    """
    try:
        if is_acm(obj):
            return obj.GetProperty(name)
        else:
            return getattr(obj, name)
    except:
        if default:
            return default
        try:
            if is_acm(obj):
                cls_name = short_type_name(obj.Class())
            elif isinstance(obj, ael.ael_entity):
                cls_name = short_type_name(getattr(ael, obj.record_type))
            else:
                cls_name = short_type_name(type(obj))
        except:
            cls_name = short_type_name(type(obj))
        raise AttributeError('%r object has no attribute %r'
                             % (cls_name, name))

def get_unique_or_primary_key(obj, default=None):
    """
    .. _`get_unique_or_primary_key(obj, *args)`:
    
    Return value of unique or primary key property

    >>> get_unique_or_primary_key(ael.Instrument['ZAR/MTN'])
    'ZAR/MTN'
    >>> get_unique_or_primary_key(acm.FInstrument['ZAR/MTN'])
    'ZAR/MTN'
    >>> get_unique_or_primary_key(None, None) is None
    Traceback (most recent call last):
        ...
    TypeError: No AEL/ACM unique or primary key for None
    >>> get_unique_or_primary_key(None) is None
    Traceback (most recent call last):
        ...
    TypeError: No AEL/ACM unique or primary key for None
    """
    try:
        key = find_unique_or_primary_key(obj)
    except Exception, e:
        if not default:
            raise
        key = None

    return get_property(obj, key, default)

def is_acm(obj):
    """
    .. _`is_acm(obj)`:
    
    Check if obj is an ACM object

    >>> is_acm(acm.FInstrument['ZAR/MTN'])
    True
    >>> is_acm(None)
    False
    >>> is_acm(ael.Instrument['ZAR/MTN'])
    False
    >>> is_acm(acm.FObject)
    True
    >>> is_acm(acm.FEnumeration['enum(InsType)'].Enumerators())
    True
    """
    try:
        return obj.IsKindOf(acm.FObject)
    except:
        return False
    #return hasattr(obj, 'Oid')

def is_acm_class(obj):
    """
    .. _`is_acm_class(obj)`:
    
    Return True if obj is an ACM class, e.g., acm.FTrade

    >>> is_acm_class(acm.FTrade)
    True
    >>> is_acm_class(acm.FObject)
    True
    >>> is_acm_class(acm.FClass)
    True
    >>> is_acm_class(None)
    False
    >>> is_acm_class(13)
    False
    >>> is_acm_class(ael.Trade)
    False
    >>> is_acm_class(object)
    False
    >>> is_acm_class(acm.FInstrument['ZAR/MTN'])
    False
    """
    try:
        return obj.IsKindOf(acm.FObject) and obj.IsClass()
    except:
        return False

def isinstance(obj, classinfo):
    """
    .. _`isinstance(obj, classinfo)`:
    
    >>> std_isinstance = _saved_builtins['isinstance']
    >>> std_isinstance(acm.FTrade, acm.FObject) #doctest: +ELLIPSIS
    Traceback (most recent call last):
        ...
    TypeError: isinstance() arg 2 must be a class, type, or tuple of ...
    >>> isinstance(acm.FTrade, acm.FObject)
    True
    >>> isinstance(acm.FTrade, acm.FClass)
    True
    >>> ins = acm.FInstrument['ZAR/MTN']
    >>> ins2 = ael.Instrument['ZAR/MTN']
    >>> isinstance(ins, acm.FInstrument)
    True
    >>> isinstance(ins, acm.FStock)
    True
    >>> isinstance(ins, (acm.FStock, acm.FOption))
    True
    >>> isinstance(ins, acm.FOption)
    False
    >>> isinstance(ins, (acm.FOption, acm.FFuture, acm.FSecurityLoan))
    False
    >>> isinstance(ins, acm.FTrade)
    False
    >>> isinstance(ins, acm.FClass)
    False
    >>> isinstance(ins, object)
    True
    >>> isinstance(ins2, ael.ael_entity)
    True
    >>> isinstance(ins2, acm.FObject)
    False
    >>> isinstance(ins2, object)
    True

    >>> isinstance(13, int)
    True
    >>> isinstance(13, (int, long, float))
    True
    >>> isinstance(13.0, (int, long, float))
    True
    >>> isinstance(13L, (int, long, float))
    True
    >>> isinstance(13j, (int, long, float))
    False
    >>> isinstance(13j, complex)
    True
    >>> isinstance(13j, object)
    True
    >>> isinstance(13, object)
    True
    >>> isinstance('foo', str)
    True
    >>> isinstance('foo', unicode)
    False
    >>> isinstance('foo', basestring)
    True
    >>> isinstance('foo', object)
    True
    >>> isinstance('foo', (unicode, str))
    True
    >>> isinstance(u'foo', str)
    False
    >>> isinstance(u'foo', unicode)
    True
    >>> isinstance(u'foo', basestring)
    True
    >>> isinstance(u'foo', (unicode, str))
    True

    >>> import types
    >>> isinstance(None, types.NoneType)
    True
    >>> isinstance(types.NoneType, type)
    True
    >>> isinstance(types.NoneType, object)
    True
    >>> isinstance(None, object)
    True
    >>> isinstance(None, int)
    False
    """
    _builtin_isinstance = _saved_builtins['isinstance']
    if _builtin_isinstance(classinfo, tuple):
        return any(isinstance(obj, t) for t in classinfo)
    elif is_acm_class(classinfo):
        try:
            return obj.IsKindOf(classinfo)
        except:
            return False
    else:
        return _builtin_isinstance(obj, classinfo)

def to_ael(obj, ael_class=None):
    """
    .. _`to_ael(obj, ael_class=None)`:
    
    Convert obj to an AEL object

    >>> to_ael(acm.FInstrument['ZAR/MTN']).insid
    'ZAR/MTN'
    >>> isinstance(to_ael(acm.FInstrument['ZAR/MTN']), ael.ael_entity)
    True

    Returns None if obj is None and returns obj if obj already is an AEL
    object (i.e., instance of ael.ael_entity).

    >>> to_ael(None) is None
    True
    >>> i = ael.Instrument['ZAR/MTN']
    >>> id(to_ael(i)) == id(i)
    True

    If obj is None, an ACM object or an AEL object then the parameter
    ael_class is ignored. If ael_class is given and obj is a string or an
    integer (int or long) then to_ael() returns ael_class[obj]:

    >>> i = to_ael('ZAR/MTN', ael.Instrument)
    >>> i.record_type
    'Instrument'
    >>> i.insid
    'ZAR/MTN'

    Note that AEL objects are single instances:

    >>> i = ael.Instrument['ZAR/MTN']
    >>> id(to_ael(to_acm(i))) == id(i)
    True

    """

    if obj is None:
        return None
    elif isinstance(obj, (ael.ael_entity)):
        return obj
    elif ael_class:
        if hasattr(obj, 'Oid'): # ACM object
            return ael_class[obj.Oid()]
        elif isinstance(obj, (str, int, int)):
            return ael_class[obj]
        else:
            raise ValueError('Can not convert %r to %r' % (obj, ael_class))
    elif hasattr(obj, 'Oid'): # ACM object
        return getattr(ael, obj.RecordType())[obj.Oid()]
    else:
        raise ValueError('Can not convert %r to an AEL object' % obj)

def to_acm(e, acm_class = None):
    """
    .. _`to_acm(e, acm_class = None)`:
    
    Convert e to an ACM FObject.

    >>> to_acm('ZAR/MTN', acm.FInstrument).Name()
    'ZAR/MTN'
    >>> to_acm(ael.Instrument['ZAR/MTN']).Name()
    'ZAR/MTN'
    >>> to_acm(acm.FInstrument['ZAR/MTN']).Name()
    'ZAR/MTN'
    >>> to_acm(None) is None
    True
    """

    if e is None:
        return None
    elif is_acm(e):
        return e
    elif isinstance(e, ael.ael_entity):
        return acm.Ael.AelToFObject(e)
    elif acm_class:
        try:
            return acm_class[e]
        except Exception, exc:
            try:
                cls_s = acm_class.Name()
            except:
                cls_s = str(acm_class)
            raise ValueError('Can not convert %r to %s: %s' % (e, cls_s, exc))
    else:
        raise ValueError('Can not convert %r to an ACM object' % e)

def xrepr(obj):
    """
    .. _`xrepr(obj)`:
    
    AEL/ACM enabled version of repr()

    >>> xrepr(None)
    'None'
    >>> xrepr(2.0)
    '2.0'
    >>> xrepr('foo')
    "'foo'"
    >>> repr([1,2,3])
    '[1, 2, 3]'
    >>> xrepr([1,2,3])
    '[1, 2, 3]'
    >>> repr(ael.Instrument['ZAR/MTN']) #doctest: +ELLIPSIS
    '<ael entity, Instrument at ...>'
    >>> xrepr(ael.Instrument['ZAR/MTN'])
    "ael.Instrument['ZAR/MTN']"
    >>> xrepr(acm.FInstrument['ZAR/MTN'])
    "acm.FStock['ZAR/MTN']"

    """
    if isinstance(obj, list):
        return '[' + ', '.join([xrepr(o) for o in obj]) + ']'
    elif isinstance(obj, tuple):
        if len(obj) == 1:
            return '(%s,)' % xrepr(obj[0])
        else:
            return '(' + ', '.join([xrepr(o) for o in obj]) + ')'
    elif isinstance(obj, dict):
        return '{' + ', '.join(
            [ '%s: %s' % (xrepr(key), xrepr(obj[key]))
              for key in sorted(obj.iterkeys()) ]) + '}'
    else:
        if 'ael' in sys.modules:
            if isinstance(obj, ael.ael_date):
                return 'ael.date_from_string(%r)' % \
                    obj.to_string(ael.DATE_ISO)
            elif isinstance(obj, ael.ael_entity):
                key = find_unique_or_primary_key(obj)
                return 'ael.%s[%r]' % (obj.record_type, getattr(obj, key))
        if hasattr(obj, 'ClassName') and hasattr(obj, 'StringKey'):
            return 'acm.%s[%r]' % (obj.ClassName(), obj.StringKey())
        else:
            _builtin_repr = _saved_builtins['repr']
            return _builtin_repr(obj)

def xstr(obj, none_string='None'):
    """
    .. _`xstr(obj, none_string='None')`:
    
    AEL/ACM enabled version of str()

    >>> xstr(None)
    'None'
    >>> xstr(None, none_string='')
    ''
    >>> xstr(2.0)
    '2.0'
    >>> xstr('foo')
    'foo'
    >>> str([1,2,3])
    '[1, 2, 3]'
    >>> xstr([1,2,3])
    '[1, 2, 3]'
    >>> str(ael.Instrument['ZAR/MTN']) #doctest: +ELLIPSIS
    '<ael entity, Instrument at ...>'
    >>> xstr(ael.Instrument['ZAR/MTN'])
    'ZAR/MTN'
    >>> xstr(acm.FInstrument['ZAR/MTN'])
    'ZAR/MTN'
    >>> insname = 'ZAR/MTN'
    >>> xstr(acm.FInstrument[insname], none_string='')
    'ZAR/MTN'
    >>> insname = 'BLABLA'
    >>> xstr(acm.FInstrument[insname], none_string='')
    ''
    """
    if obj is None:
        return none_string
    elif isinstance(obj, list):
        return '[' + ', '.join([xstr(o) for o in obj]) + ']'
    elif isinstance(obj, tuple):
        if len(obj) == 1:
            return '(%s,)' % xstr(obj[0])
        else:
            return '(' + ', '.join([xstr(o) for o in obj]) + ')'
    elif isinstance(obj, dict):
        return '{' + ', '.join(
            [ '%s: %s' % (xrepr(key), xrepr(obj[key]))
              for key in sorted(obj.iterkeys()) ]) + '}'
    else:
        if 'ael' in sys.modules:
            if isinstance(obj, ael.ael_date):
                return obj.to_string(ael.DATE_ISO)
            elif isinstance(obj, ael.ael_entity):
                return get_unique_or_primary_key(obj)
        if hasattr(obj, 'ClassName') and hasattr(obj, 'StringKey'):
            return obj.StringKey()
        elif is_acm(obj):
            return get_unique_or_primary_key(obj)
        else:
            return _saved_builtins['str'](obj)

# ----------------------------------------------------------------------------
# Main program
# ----------------------------------------------------------------------------

def testmain(argv=None):
    import doctest
    doctest.testmod(verbose=True)

if __name__ == '__main__':
    sys.exit(testmain(argv=sys.argv))