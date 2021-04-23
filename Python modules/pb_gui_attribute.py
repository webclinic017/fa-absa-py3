"""
A module implementing the GUIAttribute class and its subclasses.
"""

from ast import literal_eval
from datetime import datetime

from pb_attr_def import AttributeDefinition
from pb_attribute import ChronicleAttribute
from pb_quirk import (PortfolioSwapBasedQuirk,
                      PortfolioSwapSuggestionQuirk,
                      QuirkAttribute)


class WrongValueError(ValueError):

    """
    Custom exception class which indicates that
    the value is not valid for the desired type.
    """
    pass


def is_choice_list(choice_list_name):
    """
    Return true if a choice list with the provided name exists.
    Otherwise return false.
    """
    import acm
    choice_list = acm.FChoiceList[str(choice_list_name)]
    if choice_list is None:
        return False
    else:
        return True


def is_enum(enum_name):
    """
    Return true if an enum with the provided name exists.
    Otherwise return false.
    """
    import acm
    enumeration = acm.FEnumeration["enum({0})".format(enum_name)]
    if enumeration is None:
        return False
    else:
        return True


def get_bool_value(string_value):
    """
    Return a bool value represented by the provided string.
    """
    try:
        evaluated_value = literal_eval(string_value)
    except ValueError:
        return None # Invalid bool value
    if isinstance(evaluated_value, bool):
        return evaluated_value
    else:
        return None # Invalid bool value


def validate_bool_value(value):
    try:
        evaluated_value = literal_eval(value)
    except ValueError as exc:
        raise WrongValueError(exc)
    if not isinstance(evaluated_value, bool):
        exception_message = "invalid literal for bool(): {0}".format(
            repr(evaluated_value))
        raise WrongValueError(exception_message)


def validate_int_value(value):
    try:
        _int_value = int(value)
    except ValueError as exc:
        raise WrongValueError(exc)


def validate_float_value(value):
    try:
        _float_value = float(value)
    except ValueError as exc:
        raise WrongValueError(exc)


def validate_date_value(value):
    try:
        _date_value = datetime.strptime(value, "%Y-%m-%d")
    except ValueError as exc:
        raise WrongValueError(exc)


def validate_choice_list_value(choice_list_name, value):
    """
    Check if the choice list with the provided name
    can have the provided value.
    """
    import acm
    selection_string = "list='{0}' and name='{1}'".format(
        choice_list_name,
        value)
    choice_list = acm.FChoiceList.Select01(
        selection_string,
        "more than one matching choice list found")
    if choice_list is None:
        exception_message = ("Choice list '{0}' "
                             "cannot have value '{1}'.").format(
                                 choice_list_name,
                                 value)
        raise WrongValueError(exception_message)


def validate_enum_value(enum_name, value):
    """
    Check if the provided value is valid
    for an enum with the provided name.
    """
    import acm
    enumeration = acm.FEnumeration["enum({0})".format(enum_name)]
    if enumeration is None:
        exception_message = ("Enum '{0}' does not "
                             "seem to exist.").format(enum_name)
        raise WrongValueError(exception_message)
    enumerators = enumeration.Enumerators()
    if value not in enumerators:
        exception_message = ("Enum '{0}' "
                             "cannot have value '{1}'.").format(
                                 enum_name, value)
        raise WrongValueError(exception_message)


def validate_acm_class_value(acm_class_name, value):
    """
    Try to create an instance of the acm class
    with the provided name from the provided value.
    """
    import acm
    acm_class = acm.GetClass(str(acm_class_name))
    if acm_class is None:
        exception_message = ("An acm class with name {0} "
                             "does not seem to exist.").format(
                                 repr(acm_class_name))
        raise WrongValueError(exception_message)
    if value == "":
        acm_class_instance = None
    else:
        try:
            acm_class_instance = acm_class[value]
        except TypeError as exc:
            raise WrongValueError(exc)
    if acm_class_instance is None:
        exception_message = ("Value {0} cannot be used to get "
                             "an instance of {1}.").format(
                                 repr(value),
                                 acm_class)
        raise WrongValueError(exception_message)


def get_checked_state(ux_checkbox):
    """
    Get the checked state of the provied object of type FUxCheckBox.

    Return True if it is checked, False if it is unchecked
    and None if its check state is 'Indeterminate'.
    """
    check_state = ux_checkbox.GetCheck()
    if check_state == "Checked":
        return True
    elif check_state == "Unchecked":
        return False
    else: # check_state == "Indeterminate"
        return None


def set_checked_state(ux_checkbox, value):
    """
    Set the checked state of the provided object of type FUxCheckBox
    to the provided value.

    If the provided value is True, set the checked state to 'Checked'.
    If the provided value is False, set the checked state to 'Unchecked'.
    Otherwise set the checked state to 'Indeterminate'.
    """
    if value is True:
        check_state = "Checked"
    elif value is False:
        check_state = "Unchecked"
    else:
        check_state = "Indeterminate"
    ux_checkbox.SetCheck(check_state)


class GUIAttribute(object):

    """
    A base class for the GUI representation
    of all the prime brokerage funds' attributes.
    """

    def __init__(self, gui_id, attr_def, attribute):
        self.gui_id = gui_id
        self.attr_def = attr_def
        self.attribute = attribute
        self.edited = False


    # FIXME: Necessary?
    def __repr__(self):
        representation = ("{0}(gui_id={1}, "
                          "attr_def={2}, "
                          "attribute={3})").format(
                              type(self).__name__,
                              repr(self.gui_id),
                              repr(self.attr_def),
                              repr(self.attribute))
        return representation


    def validate_value(self, value):
        """
        Check if the provided value is valid
        for the underlying attribute.

        If it is not, raise an exception of type WrongValueError.
        """
        data_type = self.attr_def.data_type
        if data_type == AttributeDefinition.STRING_TYPE:
            return # strings are not validated
        elif data_type == AttributeDefinition.BOOL_TYPE:
            validate_bool_value(value)
        elif data_type == AttributeDefinition.INT_TYPE:
            validate_int_value(value)
        elif data_type == AttributeDefinition.FLOAT_TYPE:
            validate_float_value(value)
        elif data_type == AttributeDefinition.DATE_TYPE:
            validate_date_value(value)
        elif is_choice_list(data_type):
            validate_choice_list_value(data_type, value)
        elif is_enum(data_type):
            validate_enum_value(data_type, value)
        else:
            validate_acm_class_value(data_type, value)


    def create_layout(self, builder, name_suffix=None):
        """
        Add the attribute's layout to the provided FUxLayoutBuilder.
        """
        if name_suffix is None:
            name_suffix = ""
        builder.BeginHorzBox()
        if self.attr_def.data_type == AttributeDefinition.BOOL_TYPE:
            builder.AddCheckbox("{0}_input".format(self.gui_id),
                                str(self.attr_def.name + name_suffix))
            builder.AddFill()
        elif (is_choice_list(self.attr_def.data_type) or
              is_enum(self.attr_def.data_type)):
            builder.AddOption("{0}_input".format(self.gui_id),
                              str(self.attr_def.name + name_suffix))
        else:
            builder.AddInput("{0}_input".format(self.gui_id),
                             str(self.attr_def.name + name_suffix))
        builder.AddButton("{0}_button".format(self.gui_id),
                          "...Edit...",
                          True,
                          True)
        builder.EndBox()


    def load_attribute(self, edited_state=False):
        """
        Load the current value of the underlying attribute.
        """
        if self.attr_def.editable:
            self.make_edited(edited_state)
        current_value = self.attribute.getvalue()
        if self.attr_def.data_type == AttributeDefinition.BOOL_TYPE:
            bool_value = get_bool_value(str(current_value))
            set_checked_state(self.w_input, bool_value)
        elif (is_choice_list(self.attr_def.data_type) or
              is_enum(self.attr_def.data_type)):
            # FIXME: This code always gets an index
            # of the first option with the provided name.
            try:
                idx = self.options.index(str(current_value))
            except ValueError:
                idx = None
            self.w_input.SetData(idx)
        else:
            self.w_input.SetData(str(current_value))


    def init_layout(self, layout):
        """
        Initialize the GUI parts of the attribute's layout.
        """
        import acm
        self.layout = layout
        self.w_input = self.layout.GetControl(
            "{0}_input".format(self.gui_id))
        if is_choice_list(self.attr_def.data_type):
            bg_color = acm.UX().Colors().Create(214, 214, 206) # grey
            self.w_input.SetColor("BackgroundReadOnly", bg_color)
            choice_list = acm.FChoiceList[str(self.attr_def.data_type)]
            self.options = []
            for choice in choice_list.ChoicesSorted():
                name = choice.Name()
                self.options.append(name)
                self.w_input.AddItem(name)
        elif is_enum(self.attr_def.data_type):
            bg_color = acm.UX().Colors().Create(214, 214, 206) # grey
            self.w_input.SetColor("BackgroundReadOnly", bg_color)
            enumeration = acm.FEnumeration["enum({0})".format(
                self.attr_def.data_type)]
            self.options = []
            for enumerator in enumeration.Enumerators():
                self.options.append(enumerator)
                self.w_input.AddItem(enumerator)
        self.w_input.ToolTip(str(self.attr_def.description))
        self.w_input.Editable(False)
        self.w_button = self.layout.GetControl(
            "{0}_button".format(self.gui_id))
        self.w_button.Label("Edit")
        if not self.attr_def.editable:
            # FIXME: This tooltip does not seem to work
            self.w_button.ToolTip("This is a read-only attribute")
            self.w_button.Editable(False)


    def set_callbacks(self, parent_dialog):
        """
        Set a GUI callback for editing the underlying attribute.
        """
        # FIXME: Use the parent_dialog variable in a "cleaner" way.
        self.parent_dialog = parent_dialog
        self.w_button.AddCallback("Activate",
                                  self.button_callback,
                                  self.w_button)


    def make_edited(self, value=True):
        """
        Mark the current GUI attribute as edited or not edited.
        """
        raise NotImplementedError


    def button_callback(self, _ux_control, _unused):
        """
        Enable editing of the underlying attribute.
        """
        raise NotImplementedError


class GUIChronicleAttribute(GUIAttribute):

    """
    A GUI representation of the chronicle attribute.
    """

    def make_edited(self, value=True):
        import acm
        if value:
            reddish = acm.UX().Colors().Create(255, 150, 150)
            self.w_input.SetColor("BackgroundReadOnly", reddish)
            self.edited = True
        else:
            if self.attr_def.data_type == AttributeDefinition.BOOL_TYPE:
                bg_color = acm.UX().Colors().Create(255, 255, 255) # white
            else:
                bg_color = acm.UX().Colors().Create(214, 214, 206) # grey
            self.w_input.SetColor("BackgroundReadOnly", bg_color)
            self.edited = False


    def button_callback(self, _ux_control, _unused):
        """
        Launch the window for editing the chronicle attribute,
        wait for it to finish and collect its return value.
        Update the underlying chronicle attribute if necessary.
        """
        import acm
        # FIXME: Resolve this circular import in a better way.
        from pb_gui_dialog_attribute import ChronicleAttributeEditDialog
        shell = self.parent_dialog.layout_dialog.Shell()
        dialog = ChronicleAttributeEditDialog(
            self.attr_def,
            self.attribute,
            self.parent_dialog.pb_fund,
            self.parent_dialog.pb_fund_storage,
            validating_function=self.validate_value)
        builder = dialog.create_layout()
        # FIXME: It looks like the modal property of the dialog does not work...
        edited_chronicle_attribute = acm.UX().Dialogs().ShowCustomDialogModal(
            shell, builder, dialog)
        if edited_chronicle_attribute is not None:
            self.attribute.init(edited_chronicle_attribute)
            self.load_attribute(edited_state=True)
            # We can make the parent dialog edited without checking,
            # because one of its attributes has just been marked as edited.
            self.parent_dialog.make_edited(True)


class GUIQuirkAttribute(GUIAttribute):

    """
    A GUI representation of the quirk attribute.
    """

    def create_layout(self, builder, name_suffix=None):
        if name_suffix is None:
            name_suffix = "*"
        super(GUIQuirkAttribute, self).create_layout(builder, name_suffix)


    def make_edited(self, value=True):
        if value:
            self.w_input.Editable(True)
            self.w_button.Label("Revert")
            self.edited = True
        else:
            self.w_input.Editable(False)
            self.w_button.Label("Edit")
            self.edited = False


    def button_callback(self, _ux_control, _unused):
        """
        Make the quirk's value editable.
        """
        if self.edited:
            self.load_attribute()
        else:
            self.make_edited(True)
        self.parent_dialog.update_edited_state()


    def get_string_value(self, validate=True):
        """
        Get the value of this quirk from the GUI input field,
        validate it (if desired) and return it as string.
        """
        if self.attr_def.data_type == AttributeDefinition.BOOL_TYPE:
            checked_value = get_checked_state(self.w_input)
            string_value = str(checked_value)
        else:
            string_value = self.w_input.GetData()
        if string_value and validate:
            try:
                self.validate_value(string_value)
            except WrongValueError as exc:
                exception_message = ("Unable to save "
                                     "quirk attribute '{0}'. "
                                     "Reason: {1}").format(
                                         self.attr_def.name, exc)
                raise WrongValueError(exception_message)
        return string_value


    def save_from_input(self):
        """
        Save the value in the input field
        to the underlying quirk attribute.
        """
        if self.edited: # Only proceed if the GUI attribute has been edited.
            string_value = self.get_string_value()
            self.attribute.setvalue(string_value)
            information_message = ("Quirk attribute '{0}' has been saved "
                                   "using the value '{1}'.").format(
                                       self.attr_def.name, string_value)
            print(information_message)
            self.make_edited(False)


class GUIPortfolioSwapQuirkAttribute(GUIQuirkAttribute):

    """
    A GUI representation of the portfolio-swap-based quirk attribute.
    """

    def load_attribute(self, acm_portfolio_swap, edited_state=False):
        """
        Load the current value of the underlying portfolio-swap-based quirk
        from the currently selected portfolio swap.
        """
        if self.attr_def.editable:
            self.make_edited(edited_state)
        current_value = self.attribute.getvalue(acm_portfolio_swap)
        if self.attr_def.data_type == AttributeDefinition.BOOL_TYPE:
            bool_value = get_bool_value(str(current_value))
            set_checked_state(self.w_input, bool_value)
        elif (is_choice_list(self.attr_def.data_type) or
              is_enum(self.attr_def.data_type)):
            # FIXME: This code always gets an index
            # of the first option with the provided name.
            try:
                idx = self.options.index(str(current_value))
            except ValueError:
                idx = None
            self.w_input.SetData(idx)
        else:
            self.w_input.SetData(str(current_value))


    def button_callback(self, _ux_control, _unused):
        """
        Make the portfolio-swap-based quirk's value editable.
        """
        if self.edited:
            acm_portfolio_swap = self.parent_dialog.portfolio_swaps[
                self.parent_dialog.product_type_index]
            self.load_attribute(acm_portfolio_swap)
        else:
            self.make_edited(True)
        self.parent_dialog.update_edited_state()


    def save_from_input(self, acm_portfolio_swap):
        """
        Save the value in the input field
        using the underlying portfolio-swap-based quirk
        to the currently selected portfolio swap.
        """
        if self.edited: # Only proceed if the GUI attribute has been edited.
            string_value = self.get_string_value()
            self.attribute.setvalue(acm_portfolio_swap, string_value)
            information_message = ("Portfolio-swap-based quirk attribute "
                                   "'{0}' has been saved using "
                                   "the portfolio swap '{1}'"
                                   "and value '{2}'.").format(
                                       self.attr_def.name,
                                       acm_portfolio_swap.Name(),
                                       string_value)
            print(information_message)
            self.make_edited(False)


class GUIPortfolioSwapSuggestionQuirkAttribute(GUIQuirkAttribute):

    """
    A GUI representation of the portfolio-swap-based
    suggestion quirk attribute.
    """

    def __init__(self, gui_id, attr_def, attribute):
        super(GUIPortfolioSwapSuggestionQuirkAttribute, self).__init__(
            gui_id, attr_def, attribute)
        # The suggestion quirks should be editable
        self.attr_def.editable = True


    def load_attribute(self, sweeping_class, fully_funded):
        """
        Load the current value of the underlying portfolio-swap-based
        suggestion quirk using the provided sweeping class properties.
        """
        if self.attr_def.editable:
            self.make_edited(False)
        current_value = self.attribute.getvalue(sweeping_class, fully_funded)
        if self.attr_def.data_type == AttributeDefinition.BOOL_TYPE:
            bool_value = get_bool_value(str(current_value))
            set_checked_state(self.w_input, bool_value)
        elif (is_choice_list(self.attr_def.data_type) or
              is_enum(self.attr_def.data_type)):
            # FIXME: This code always gets an index
            # of the first option with the provided name.
            try:
                idx = self.options.index(str(current_value))
            except ValueError:
                idx = None
            self.w_input.SetData(idx)
        else:
            self.w_input.SetData(str(current_value))


    def button_callback(self, _ux_control, _unused):
        """
        Make the portfolio-swap-based quirk's value editable.
        """
        if self.edited:
            sweeping_class = self.parent_dialog.sweeping_class
            fully_funded = self.parent_dialog.fully_funded
            self.load_attribute(sweeping_class, fully_funded)
        else:
            self.make_edited(True)
        self.parent_dialog.update_edited_state()


def create_attribute(gui_id, attr_def, attribute):
    """
    Return an instance of the appropriate subclass
    of the GUIAttribute class representing the provided attribute.
    """

    if isinstance(attribute, ChronicleAttribute):
        gui_attr_inst = GUIChronicleAttribute(gui_id, attr_def, attribute)
    elif isinstance(attribute, QuirkAttribute):
        gui_attr_inst = GUIQuirkAttribute(gui_id, attr_def, attribute)
    elif isinstance(attribute, PortfolioSwapBasedQuirk):
        gui_attr_inst = GUIPortfolioSwapQuirkAttribute(
            gui_id, attr_def, attribute)
    elif isinstance(attribute, PortfolioSwapSuggestionQuirk):
        gui_attr_inst = GUIPortfolioSwapSuggestionQuirkAttribute(
            gui_id, attr_def, attribute)
    else:
        exception_message = ("The provided attribute {0} "
                             "is of unknown type {1}.").format(
                                 repr(attribute),
                                 type(attribute).__name__)
        raise RuntimeError(exception_message)

    return gui_attr_inst
