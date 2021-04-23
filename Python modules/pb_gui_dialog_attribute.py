"""
A module which contains classes for creating a GUI
for editing a chronicle attribute.
"""

from copy import deepcopy

from FUxCore import LayoutDialog

from at_chronicle import TimeValue
from pb_gui_attribute import WrongValueError
from pb_gui_core import (CANCEL_BUTTON_ID,
                         OK_BUTTON_ID,
                         sanitize_ux_control_label,
                         show_information_window,
                         show_question_window,
                         TimeValueEditDialog)
from pb_storage_attr_def import AttributeDefinitionStorage
from pb_storage_fund import PrimeBrokerageFundStorage


class ChronicleAttributeEditDialog(LayoutDialog):

    """
    A class which represents a dialog
    for editing the prime brokerage chronicle attribute.
    """

    def __init__(self,
                 attr_def,
                 chronicle_attribute,
                 pb_fund,
                 pb_fund_storage,
                 validating_function=None):
        """
        Initialize the instance.
        """
        self.attr_def = attr_def
        # A (deep)copy is used so that the original chronicle attribute
        # is left unchanged if the dialog is closed without saving.
        self.chronicle_attribute_copy = deepcopy(chronicle_attribute)
        self.pb_fund = pb_fund
        self.pb_fund_storage = pb_fund_storage
        self.validating_function = validating_function
        self.edited = False
        self.initial_value_edited = False


    def make_edited(self, new_edited_state):
        """
        Mark the current dialog as edited or not edited.
        """
        if new_edited_state and not self.edited:
            self.w_ok.Enabled(True)
            self.w_notice.SetData("edited")
            self.edited = True
        elif not new_edited_state and self.edited:
            self.w_ok.Enabled(False)
            self.w_notice.SetData("")
            self.edited = False


    def load_attribute(self, chronicle_attribute=None):
        """
        Load the provided prime brokerage chronicle attribute.
        """
        if chronicle_attribute is not None:
            self.chronicle_attribute_copy = deepcopy(chronicle_attribute)
        initial_value = str(self.chronicle_attribute_copy.chronicle.initial_value)
        self.w_initial_value.SetData(initial_value)
        self.w_time_values.Clear()
        root_item = self.w_time_values.GetRootItem()
        sorted_tvs = self.chronicle_attribute_copy.chronicle.sorted_tvs.wrapped_list
        for i, time_value in enumerate(sorted_tvs, start=1):
            child_item = root_item.AddChild(True)
            child_item.Label(str(time_value.utc_datetime), 0)
            child_item.Label(str(time_value.value), 1)
            child_item.SetData(time_value)
            if i == len(sorted_tvs):
                self.w_time_values.SetSelectedItems([child_item])
                child_item.EnsureVisible()
        self.w_time_values.AdjustColumnWidthToFitItems(0)
        self.w_time_values.AdjustColumnWidthToFitItems(1)


    def launch_time_value_edit_dialog(self,
                                      time_value=None,
                                      ok_button_label=None):
        """
        Launch a dialog for editing the provided time value.
        """
        import acm
        if time_value is None:
            time_value = TimeValue(None)
        shell = self.layout_dialog.Shell()
        dialog = TimeValueEditDialog(
            time_value,
            ok_button_label=ok_button_label,
            validating_function=self.validating_function)
        builder = dialog.create_layout()
        return acm.UX().Dialogs().ShowCustomDialogModal(shell, builder, dialog)


    def create_layout(self):
        """
        Return a new instance of FUxLayoutBuilder
        with a layout that will be used at the bottom of the main dialog.
        """
        import acm
        builder = acm.FUxLayoutBuilder()
        builder.BeginVertBox()
        attr_name = sanitize_ux_control_label(str(self.attr_def.name))
        builder.AddLabel("attr_name", attr_name)
        attr_description = sanitize_ux_control_label(
            str(self.attr_def.description))
        builder.AddLabel("attr_description", attr_description)
        builder.BeginHorzBox()
        builder.AddInput("initial_value", "Initial value")
        builder.AddButton("edit_initial_value", " Edit ", False, True)
        builder.EndBox()
        builder.BeginHorzBox()
        builder.AddFill()
        builder.AddLabel("notice", "..... loading  .....", False, True)
        builder.AddFill()
        builder.EndBox()
        builder.AddList("list_of_values", 7, -1, 50, -1)
        builder.BeginHorzBox()
        builder.AddButton(OK_BUTTON_ID, " Save ", False, True)
        builder.AddFill()
        builder.AddButton("add_time_value", " Add ", False, True)
        builder.AddButton("edit_time_value", " Edit ", False, True)
        builder.AddButton("delete_time_value", " Delete ", False, True)
        builder.AddFill()
        builder.AddButton(CANCEL_BUTTON_ID, " Close ", False, True)
        builder.EndBox()
        builder.EndBox()
        return builder


    def init_layout(self, layout):
        """
        Initialize the GUI parts of the dialog's layout.
        """
        import acm
        w_name = layout.GetControl("attr_name")
        w_name.ToolTip("The name of the attribute")
        w_name.SetStandardFont("Bold")
        w_name.SetData(str(self.attr_def.name))
        w_attr_description = layout.GetControl("attr_description")
        w_attr_description.ToolTip("Attribute's description")
        w_attr_description.SetData(str(self.attr_def.description))
        self.w_ok = layout.GetControl(OK_BUTTON_ID)
        self.w_ok.SetStandardFont("Bold")
        self.w_ok.Enabled(False)
        self.w_initial_value = layout.GetControl("initial_value")
        initial_value = str(self.chronicle_attribute_copy.chronicle.initial_value)
        self.w_initial_value.SetData(initial_value)
        self.w_initial_value.Editable(False)
        self.w_time_values = layout.GetControl("list_of_values")
        self.w_time_values.ShowGridLines(True)
        self.w_time_values.AddCallback("DefaultAction", # a double click event
                                       self.edit_time_value_callback,
                                       self.w_time_values)
        self.w_time_values.AddColumn(
            "UTC datetime",
            -1,
            "UTC date and time since when the particular value is valid")
        self.w_time_values.AddColumn(
            "Value",
            -1,
            "A value valid since the particular UTC date and time")
        self.w_time_values.ShowColumnHeaders(True)
        self.w_notice = layout.GetControl("notice")
        self.w_notice.SetStandardFont("Bold")
        self.w_notice.SetAlignment("Center")
        reddish = acm.UX().Colors().Create(195, 31, 0)
        self.w_notice.SetColor("Text", reddish)
        self.w_notice.SetData("")
        self.w_edit_initial_value = layout.GetControl("edit_initial_value")
        self.w_edit_initial_value.AddCallback(
            "Activate",
            self.edit_initial_value_callback,
            self.w_initial_value)
        self.w_add_time_value = layout.GetControl("add_time_value")
        self.w_add_time_value.AddCallback(
            "Activate",
            self.add_time_value_callback,
            self.w_time_values)
        self.w_edit_time_value = layout.GetControl("edit_time_value")
        self.w_edit_time_value.AddCallback(
            "Activate",
            self.edit_time_value_callback,
            self.w_time_values)
        self.w_edit_time_value.SetFocus()
        self.w_delete_time_value = layout.GetControl("delete_time_value")
        self.w_delete_time_value.AddCallback(
            "Activate",
            self.delete_time_value_callback,
            self.w_time_values)
        self.load_attribute()


    def edit_initial_value_callback(self, _ux_control, _unused):
        """
        Enable editing of the initial value.
        """
        if not self.initial_value_edited:
            self.w_edit_initial_value.Enabled(False)
            self.w_initial_value.Editable(True)
            self.initial_value_edited = True
            self.make_edited(True)


    def add_time_value_callback(self, _ux_control, _unused):
        """
        Add an empty time value to the list of time values.
        and launch a dialog for editing it.
        """
        time_value = self.launch_time_value_edit_dialog(ok_button_label="Add")
        if time_value is not None:
            self.chronicle_attribute_copy.chronicle.insert_time_value(time_value)
            self.make_edited(True)
            self.load_attribute()


    def edit_time_value_callback(self, _ux_control, _unused):
        """
        Launch a window for editing the selected value.
        """
        selected_item = self.w_time_values.GetSelectedItem()
        if selected_item is None:
            information_message = ("No time value is selected, "
                                   "not editing anything.")
            print(information_message)
            return

        time_value = selected_item.GetData()
        edited_time_value = self.launch_time_value_edit_dialog(time_value=time_value)
        if edited_time_value is not None:
            self.chronicle_attribute_copy.chronicle.insert_time_value(
                edited_time_value)
            self.make_edited(True)
            self.load_attribute()


    def delete_time_value_callback(self, _ux_control, _unused):
        """
        Remove the currently selected time value from the list of time values.
        """
        selected_item = self.w_time_values.GetSelectedItem()
        if selected_item is None:
            information_message = ("No time value is selected, "
                                   "not deleting anything.")
            print(information_message)
        else:
            time_value = selected_item.GetData()
            self.chronicle_attribute_copy.chronicle.remove_time_value(
                time_value.utc_datetime)
            self.make_edited(True)
            self.load_attribute()


    def HandleCreate(self, layout_dialog, main_layout):
        """
        Handle the dialog's create event.
        """
        self.layout_dialog = layout_dialog
        self.layout_dialog.Caption(("Fund '{0}' | "
                                    "Attribute '{1}'").format(
                                        self.pb_fund.fund_id,
                                        self.attr_def.name))
        self.init_layout(main_layout)


    def HandleApply(self):
        """
        Obtain the changed fund's attributes from the GUI
        and set them using the underlying Attributes.

        This function handles an event of pressing a button
        with name == "ok".
        """
        if self.edited:
            shell = self.layout_dialog.Shell()
            message = ("Are you sure you want to save "
                       "the chronicle attribute '{0}' "
                       "of the prime brokerage "
                       "fund '{1}'?").format(
                           self.attr_def.name, self.pb_fund.fund_id)
            answer = show_question_window(shell, message)
            if answer == "Button1": # The first button (Yes) has been pressed.
                if self.initial_value_edited:
                    # FIXME: Maybe it would be better to have a function
                    # which would take care of that?
                    string_value = self.w_initial_value.GetData()
                    if string_value and self.validating_function:
                        try:
                            self.validating_function(string_value)
                        except WrongValueError as exc:
                            shell = self.layout_dialog.Shell()
                            message = ("The provided initial value '{0}' "
                                       "is not valid. Reason: {1}").format(
                                           string_value, exc)
                            show_information_window(shell, message)
                            return # Keep the dialog open
                    # FIXME: Necessary?
                    self.w_edit_initial_value.Enabled(True)
                    self.w_initial_value.Editable(False)
                    self.initial_value_edited = False
                    self.chronicle_attribute_copy.chronicle.initial_value = \
                        string_value
                information_message = ("Chronicle attribute '{0}' "
                                       "of the prime brokerage fund '{1}' "
                                       "has been saved.").format(
                                           self.attr_def.name,
                                           self.pb_fund.fund_id)
                print(information_message)
                return self.chronicle_attribute_copy
            else:
                information_message = ("Abandoned the changes made to "
                                       "the chronicle attribute '{0}' "
                                       "of the prime brokerage "
                                       "fund '{1}'.").format(
                                           self.attr_def.name,
                                           self.pb_fund.fund_id)
                print(information_message)


    def HandleCancel(self):
        """
        If the current dialog has been edited,
        ask the user if they really want to close it.

        This function handles an event of pressing a button
        with name == "cancel".
        """
        if self.edited:
            shell = self.layout_dialog.Shell()
            message = ("Are you sure you want to close "
                       "this dialog without saving changes "
                       "to the currently edited "
                       "chronicle attribute '{0}'?").format(self.attr_def.name)
            answer = show_question_window(shell, message)
            if answer == "Button1": # The first button (Yes) has been pressed.
                information_message = ("The changes you have made "
                                       "to the prime brokerage fund's '{0}' "
                                       "chronicle attribute '{1}' "
                                       "have been lost.").format(
                                           self.pb_fund.fund_id,
                                           self.attr_def.name)
                print(information_message)
                return True # The dialog will be closed
        else:
            return True # The dialog will be closed


def demo_launch():
    """
    Launch the attribute edit dialog
    as a standalone application within Front Arena.
    The parent of this dialog will be the session manager.
    """
    import acm
    shell = acm.UX().SessionManager().Shell()
    pb_fund_storage = PrimeBrokerageFundStorage()
    pb_fund_storage.load()
    fund_id = pb_fund_storage.stored_funds.iterkeys().next()
    pb_fund = pb_fund_storage.load_fund(fund_id)
    attr_def_storage = AttributeDefinitionStorage()
    attr_def_storage.load()
    name, chronicle_attribute = pb_fund.attributes.iteritems().next()
    attr_def = attr_def_storage.attr_defs[name]
    dialog = ChronicleAttributeEditDialog(attr_def,
                                          chronicle_attribute,
                                          pb_fund,
                                          pb_fund_storage,
                                          validating_function=None)
    builder = dialog.create_layout()
    chronicle_attribute = acm.UX().Dialogs().ShowCustomDialogModal(
        shell, builder, dialog)
    print("Edited chronicle attribute:\n{0}".format(chronicle_attribute))


#demo_launch()
