"""A convenience class for dict-like handling of FParameters

History
C1024176    Jan Sinkora         Initial deployment.

"""

import acm
from at_functools import cache_first_result

class FParametersDict(object):
    """FParameters-encompassing configuration class."""

    PARAM_TPL = "FObject:{0} =\n{1}\n"
    EXT_TYPE = 'FParameters'
    EXT_CLASS = 'FObject'

    class DoesNotExist(ValueError):
        pass

    @classmethod
    @cache_first_result
    def _ext_context(cls):
        return acm.GetDefaultContext()

    @classmethod
    def apply_if_exists(cls, method, value):
        """Apply the method to the value if it is defined (in a subclass)."""
        if hasattr(cls, method):
            value = getattr(cls, method)(value)
        return value

    def __init__(self, name, module, create=False):
        """Initializer.

        name - the name of the FParameters object.
        create - if True, the FParameters ext will be created if not existing.

        """

        self.name = name
        self._module = self._ext_context().GetModule(module)
        self._data = {}
        self._load(create)

    def _read_ext(self):
        """Read the FParameters object contents."""
        return self._module.GetExtension(self.EXT_TYPE, self.EXT_CLASS, self.name)

    def _load(self, create=False):
        """Load or create the FParameters object."""
        ext = self._read_ext()
        if not ext:
            if create:
                self._data = self._default_values()
                self._save()
                ext = self._read_ext()
            else:
                raise self.DoesNotExist("Parameters not found in the DB.")

        params = ext.Value()
        for key in params.Keys():
            key = key.AsString()
            load_method = '_load_{0}'.format(key)
            value = self.apply_if_exists(load_method, params[key].AsString())
            self._data[key] = value

    def _default_values(self):
        """Default values for the FParameters object.

        Override this in subclasses.

        """
        return {'empty': 'True'}

    def _save(self):
        """Save the extension."""
        if self._data:
            self._ext_context().EditImport('FParameters', self._formatted_ext(), True, self._module)
        else:
            self._module.RemoveExtension(self.EXT_TYPE, self.EXT_CLASS, self.name)
        self._module.Commit()

    def delete(self):
        """Delete the extension."""
        self._data = {}
        self._save()

    def _formatted_ext(self):
        """Get the extension-formatted representation."""
        lines = []
        for k, v in self._data.items():
            line = "{0}={1}"
            save_method = '_save_{0}'.format(k)
            v = self.apply_if_exists(save_method, v)
            lines.append(line.format(k, str(v)))

        return self.PARAM_TPL.format(self.name, "\n".join(lines))

    def __setitem__(self, key, value):
        self._data[key] = value
        self._save()

    def __getitem__(self, key):
        return self._data[key]

    def __delitem__(self, key):
        del self._data[key]
        self._save()

    def __contains__(self, key):
        return key in self._data

    def __repr__(self):
        return "({0}) {1}".format(self.name, self._data)

    def update(self, data):
        self._data.update(data)
        self._save()

    @classmethod
    def _all_dict_names(cls, module):
        """Get names of all the dictionaries saved in the given module."""
        return module.ExtensionNames(cls.EXT_TYPE, cls.EXT_CLASS, False, True)

