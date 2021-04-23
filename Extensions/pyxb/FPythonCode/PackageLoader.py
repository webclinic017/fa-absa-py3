'''
PackageLoader
'''

import acm
import imp
import sys
import os

def _init_name(fullname):
    """Return the name of the __init__ module for a given package name."""
    if fullname.endswith('.__init__'):
        return fullname
    return fullname + '.__init__'

def _key_name(fullname, extension):
    """Look in an extension module for fullname or fullname.__init__, return the name found."""
    init_name = _init_name(fullname)
    if init_name in extension:
        return init_name

    if fullname in extension:
        return fullname
    return None
    
class ExtensionManager(object):
    """Find modules collected in a Extension Module."""
    
    def __init__(self, prefix):
        self.prefix = prefix
        self.extension_names = [ str(module.Name()) for module in acm.GetDefaultContext().GetAllExtensions('FPythonCode')
                if str(module.Name()).startswith(self.prefix + '.') ]
        
    def __str__(self):
        return '<%s for "%s">' % (self.__class__.__name__, self.prefix)
        
    def find_module(self, fullname, path=None):
        if path:
            path = path
        else:
            path = [self.prefix]

        if fullname.startswith(self.prefix) and (fullname in self.extension_names or _init_name(fullname) in self.extension_names):
            return ExtensionLoader(path, self.extension_names)
        return None


class ExtensionLoader(object):
    """Load Extension Module source and compile them."""
    
    def __init__(self, path, extension_names):
        self.path = path
        self.extension_names = extension_names

        return

    def get_source(self, fullname):
        key_name = _key_name(fullname, self.extension_names)

        pyt = acm.GetDefaultContext().GetExtension('FPythonCode', 'FObject', key_name)
        if pyt:
            return str(pyt.Value())
        raise ImportError('could not find source for %s' % fullname)

    def _is_package(self, fullname):
        init_name = _init_name(fullname)
        return init_name in self.extension_names

    def load_module(self, fullname):
        if fullname.endswith(".__init__"): fullname = fullname[:-9] 

        source = self.get_source(fullname)
        if source:
            if fullname in sys.modules:
                #print 'reusing existing module from previous import of "%s"' % fullname
                mod = sys.modules[fullname]
            else:
                mod = sys.modules.setdefault(fullname, imp.new_module(fullname))

            # Set a few properties required by PEP 302
            mod.__name__ = fullname
            mod.__loader__ = self
            
            if self._is_package(fullname):
                #print 'adding path for package', self.path
                # Set __path__ for packages
                # so we can find the sub-modules.
                mod.__path__ = self.path
                mod.__file__ = _init_name(fullname)
            else:
                #print 'imported as regular module'
                mod.__package__ = fullname.rpartition('.')[0]
                mod.__file__ = fullname
            
            #print 'execing source...'
            #print source
            try:
                exec (source, mod.__dict__)
            except Exception as e:
                print("Error while executing source <%s>. Error: %s"%(fullname, str(e)))
            #print 'done'
        return sys.modules.get(fullname)

def activate(name):
    """ activates extension module loading within ACM. Only package starting with name is activated. """
    if len([mod for mod in sys.meta_path if (mod.__class__.__name__ == "ExtensionManager" and mod.prefix == name)]) == 0:
        sys.meta_path=[mod for mod in sys.meta_path if not (mod.__class__.__name__ == "ExtensionManager" and mod.prefix == name)] + [ExtensionManager(name)]

    del sys.modules[name] # Is needed to deactivate the "false" loaded module
    try:
        __import__("%s.__init__"%name) # does set sys.modules[name] without "__init__" when no variable assigned.
    except:
        __import__("%s.__init__"%name, level = 0 ) 

    





