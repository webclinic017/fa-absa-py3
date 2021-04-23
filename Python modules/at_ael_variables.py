"""A helper class for easy handling of ael_variables and run script gui hooks.

Example of usage:

def check_party(selected_variable):
    value = selected_variable.value
    output_path = ael_variables.get('output_path')
    output_path.value = 'y:/' + value

    party = acm.FParty[value]
    if party and party.Name() == 'S A B':
        print "What a nice party!"

ael_variables = AelVariableHandler()

ael_variables.add('output_path',
                  mandatory=False,
                  label='Output path')

ael_variables.add('party',
                  label='Party name',
                  collection=acm.FParty.Select(''),
                  hook=check_party)

def ael_main(params):
    # Do stuff here.
    pass

"""
try:
    from FRunScriptGUI import InputFileSelection, OutputFileSelection, DirectorySelection
except Exception, e:
    print(e)

import FBDPGui

if hasattr(FBDPGui.AelVariables, "_OtherAttributes"):
    if "value" not in FBDPGui.AelVariables._OtherAttributes:
        FBDPGui.AelVariables._OtherAttributes = ('oldTooltip', 'sequenceNumber', 'value')


class AelVariableHandler(list):
    """This class makes the use of ael_variables more convenient.

    It is used for building of the parameters which can then be accessed by name.
    Parameters of the variables can be changed as well as the values.

    For example of usage see FA wiki (team site).

    """

    # The names of all the parameters that can be set for an ael_variable.
    COLUMNS = ['name', 'label', 'cls', 'collection', 'default', 'mandatory',
               'multiple', 'alt', 'hook', 'enabled', 'tab']

    class AelVariable(list):
        """Represents one ael_variables row."""

        def __init__(self,
                     var_handler,
                     name,
                     label,
                     cls='string',
                     collection=None,
                     default=None,
                     mandatory=True,
                     multiple=False,
                     alt=None,
                     hook=None,
                     enabled=True,
                     tab=None,
                     callback=None):
            """Initializer of the variable.

            If a hook is specified, it is called when this variable is changed.
            It needs to have one parameter which receives this variable instance.

            """
            assert (hook is None or
                    callback is None), ('Either hook or callback '
                                        'can be specified, but not both.')
            # reference to the variable handler
            self.handler = var_handler

            if hook:
                # Set up the hook to hide the magical field_values
                hook = self.wrap_hook(hook)
            elif callback:
                # The callback is used as is
                hook = callback

            # Append tab to label name for proper interpretation by FA.
            label = '_'.join([label, tab]) if tab else label

            # Fill the list that's going to be used by FA.
            self[:] = [name, label, cls, collection, default, int(mandatory), multiple, alt, hook, enabled]

        def wrap_hook(self, hook):
            """Wraps the hook so that it doesn't need to handle the default parameters."""

            def wrapped(index, field_values):
                self.handler._set_field_values(field_values)
                hook(self)
                field_values = self.handler._get_field_values()
                self.handler._clear_field_values()
                return field_values

            return wrapped

        def __getattr__(self, name):
            """Accesses the variable parameters if a valid param name is passed."""

            if name in AelVariableHandler.COLUMNS:
                return self[AelVariableHandler._index_of_param(name)]
            else:
                # no attribute was found
                raise AttributeError(name)

        def __setattr__(self, name, value):
            """Sets the variable parameters if a valid param name is passed."""

            if name in AelVariableHandler.COLUMNS:
                self[AelVariableHandler._index_of_param(name)] = value
            else:
                self.__dict__[name] = value

    class FileSelectionAelVariable(AelVariable):
        """A variable used for defining an input or output file via a dialog."""

        def __init__(self, var_handler, name, label, input_output, file_filter=None, **kwargs):
            """Initialize the variable.

            The cls and multiple options will be overriden so that the
            dialog for navigating the filesystem is shown.

            input_output -- needs to be one of: 'input', 'output'.
            file_filter -- defines the accepted file types.
                Example: 'TXT Files (*.txt)|*.txt'.

            """

            if input_output == 'input':
                selection_class = InputFileSelection
            elif input_output == 'output':
                selection_class = OutputFileSelection
            else:
                raise ValueError('Wrong file type: {0}'.format(input_output))

            if file_filter is not None:
                selection = selection_class(file_filter)
            else:
                selection = selection_class()

            kwargs['cls'] = selection
            kwargs['multiple'] = True

            super(AelVariableHandler.FileSelectionAelVariable, self).__init__(var_handler, name, label, **kwargs)

    class DirectorySelection(AelVariable):
        """A variable used for locating a filesystem path via a dialog."""
        def __init__(self, *args, **kwargs):
            """Initialize the variable.

            The cls and multiple options will be overriden.
            """

            selection = DirectorySelection()
            if 'default' in kwargs:
                selection.SelectedDirectory(kwargs['default'])

            kwargs['cls'] = selection
            kwargs['default'] = selection
            kwargs['multiple'] = True

            super(AelVariableHandler.DirectorySelection, self).__init__(*args, **kwargs)

    class BooleanVariable(AelVariable):
        """A checkbox variable."""
        def __init__(self, *args, **kwargs):
            """Initialize the variable.

            The cls and collection options will be overriden.
            """
            kwargs['cls'] = 'bool'
            kwargs['collection'] = [True, False]

            super(AelVariableHandler.BooleanVariable, self).__init__(*args, **kwargs)

    @classmethod
    def _index_of_param(cls, param):
        """Returns the index of the variable parameter in the list representation."""
        return cls.COLUMNS.index(param)

    def _index_of_var(self, name):
        """Returns the index of the variable."""
        for i, v in enumerate(self):
            if v.name == name:
                return i
        raise KeyError("{0} not present.".format(name))

    def add(self, *args, **kwargs):
        """Creates an AelVariable instance and appends to self."""
        ael_var = self.AelVariable(self, *args, **kwargs)
        self.append(ael_var)
        return ael_var

    def add_input_file(self, name, label, file_filter=None, **kwargs):
        """Convenience method for input file adding.

        See FileSelectionAelVariable for details.
        """
        return self._add_file_selection(name, label, input_output='input', file_filter=file_filter, **kwargs)

    def add_output_file(self, name, label, file_filter=None, **kwargs):
        """Convenience method for output file adding.

        See FileSelectionAelVariable for details.
        """
        return self._add_file_selection(name, label, input_output='output', file_filter=file_filter, **kwargs)

    def _add_file_selection(self, name, label, input_output, file_filter, **kwargs):
        """Add a file selection.

        This just creates a FileSelectionAelVariable instance (see docstring for details)
        and appends it.
        """
        ael_var = self.FileSelectionAelVariable(self, name, label, input_output, file_filter, **kwargs)
        self.append(ael_var)
        return ael_var

    def add_directory(self, *args, **kwargs):
        """Convenience method for directory selection variable adding.

        See DirectorySelection for details.
        """
        ael_var = self.DirectorySelection(self, *args, **kwargs)
        self.append(ael_var)
        return ael_var

    def add_bool(self, *args, **kwargs):
        """Convenience method for checkbox variable adding.

        See BooleanVariable for details.
        """
        ael_var = self.BooleanVariable(self, *args, **kwargs)
        self.append(ael_var)
        return ael_var

    def get(self, name):
        """Finds and returns a variable by name."""
        try:
            return filter(lambda v: v.name == name, self)[0]
        except IndexError:
            raise KeyError("{0} not present.".format(name))

    def _get_field_values(self):
        """Gets a list of values from the variables.

        Internally used in hook handling.

        """
        return map(lambda var: var.value, self)

    def _set_field_values(self, field_values):
        """Sets the current values of the variables.

        Internally used in hook handling.

        """
        for var, value in zip(self, field_values):
            var.value = value

    def _clear_field_values(self):
        """Clears the temporary internal values all variables.

        Internally used in hook handling.

        """
        for var in self:
            del var.value


class AelVariableProvider(object):
    """A class for providing class-specific ael variables.

    This class works with an instance of AelVariableHandler.
    Use this as a superclass for a class which has specific ael variables.
    This is useful if you have a class hierarchy with shared ael variables.
    For example of usage, see at_feed_processing and collateral_cashflow_upload.

    """

    @classmethod
    def _populate_ael_variables(cls, variables, defaults):
        """Add any class-specific ael variable declaration into variables.

        defaults -- a dictionary with default values.

        If defaults contains a default value for one of the variables specified
        here, it must be popped from the dictionary.

        """
        pass

    @classmethod
    def ael_variables(cls, **defaults):
        """Creates an AelVariableHandler instance with requried variables.

        This calls _populate_ael_variables and sets the default values.

        """
        variables = AelVariableHandler()
        cls._populate_ael_variables(variables, defaults)

        # The defaults should all have been consumed.
        if defaults:
            raise ValueError("Default values not recognized: {0}".format(
                defaults))

        return variables
