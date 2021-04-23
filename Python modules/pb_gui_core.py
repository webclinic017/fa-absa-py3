"""
A module which contains classes and functions
for creating simple GUI dialogs.
"""

from datetime import datetime

from FUxCore import LayoutDialog

from at_chronicle import TimeValue
from pb_gui_attribute import WrongValueError


OK_BUTTON_ID = "ok"
CANCEL_BUTTON_ID = "cancel"


def timestamp_to_str(timestamp):
    """
    Return a string representation of a naive datetime object
    corresponding to the provided unix timestamp.
    """
    return str(datetime.fromtimestamp(timestamp))


def sanitize_ux_control_label(name):
    """
    Return a sanitized version of a name
    which can be used for labels of FUxControl objects.
    """
    return str(name).replace("'", " ")


# FIXME: Is this function ever used?
def show_error_window(shell, message):
    import acm
    acm.UX().Dialogs().MessageBox(shell,
                                  "Error",
                                  message,
                                  "OK",
                                  None,
                                  None,
                                  "Button1",
                                  "Button1")


def show_information_window(shell, message):
    import acm
    acm.UX().Dialogs().MessageBoxInformation(shell, message)


def show_question_window(shell, message):
    import acm
    answer = acm.UX().Dialogs().MessageBoxYesNo(shell, "Question", message)
    return answer


class OpenDialog(LayoutDialog):

    """
    A class which represents open dialog
    for opening items of a certain type.
    """

    def __init__(self, rows, column_names, selected_name=None):
        """
        Initialize the instance.
        """
        self.rows = rows
        self.column_names = column_names
        self.selected_name = selected_name


    def create_layout(self):
        """
        Return a new instance of FUxLayoutBuilder
        with a layout that will be used for this dialog.
        """
        import acm
        builder = acm.FUxLayoutBuilder()
        builder.BeginVertBox()
        builder.AddList("names_list", 20, -1, 120, -1)
        builder.BeginHorzBox()
        builder.AddInput("name", "Name")
        builder.AddButton(OK_BUTTON_ID, "Open", False, True)
        builder.AddButton(CANCEL_BUTTON_ID, "Close", False, True)
        builder.EndBox()
        builder.EndBox()
        return builder


    def init_layout(self, layout):
        """
        Initialize the GUI parts of the dialog's layout.
        """
        w_ok = layout.GetControl(OK_BUTTON_ID)
        w_ok.SetStandardFont("Bold")
        self.w_names_list = layout.GetControl("names_list")
        self.w_names_list.ToolTip("The list of items to select from")
        self.w_names_list.ShowColumnHeaders(True)
        self.w_names_list.ShowGridLines(True)
        for column_name in self.column_names:
            self.w_names_list.AddColumn(column_name, -1)
        root_item = self.w_names_list.GetRootItem()
        for line in self.rows:
            child_item = root_item.AddChild(True)
            for i, field in enumerate(line):
                child_item.Label(field, i)
            name = line[0]
            child_item.SetData(name)
            if name == self.selected_name:
                self.w_names_list.SetSelectedItems([child_item])
                child_item.EnsureVisible()
        for i in range(len(self.rows[0])):
            self.w_names_list.AdjustColumnWidthToFitItems(i)
        self.w_names_list.AddCallback(
            "SelectionChanged",
            self.select_callback,
            self.w_names_list)
        self.w_name = layout.GetControl("name")
        self.w_name.SetData(self.selected_name)
        self.w_name.ToolTip("The currently selected item")
        self.w_name.Editable(False)


    def select_callback(self, ux_control, _unused):
        """
        Set the name of the currently selected item to the input box.
        """
        selected_item = self.w_names_list.GetSelectedItem()
        if selected_item is not None:
            self.selected_name = selected_item.GetData()
            self.w_name.SetData(self.selected_name)


    def HandleCreate(self, layout_dialog, main_layout):
        """
        Handle the dialog's create event.
        """
        layout_dialog.Caption("Open ...")
        self.init_layout(main_layout)


    def HandleApply(self):
        """
        Return the selected item's data.

        This function handles an event of pressing a button
        with name == "ok".
        """
        return self.w_name.GetData()


class TimeValueEditDialog(LayoutDialog):

    """
    A class representing a dialog for editing a time value.
    """

    def __init__(self,
                 time_value,
                 ok_button_label=None,
                 validating_function=None):
        """
        Initialize the instance.
        """
        self.time_value = time_value
        if ok_button_label is None:
            ok_button_label = "Edit"
        self.ok_button_label = ok_button_label
        self.validating_function = validating_function


    def load_time_value(self, time_value=None):
        """
        Load the provided time value.
        """
        if time_value is not None:
            self.time_value = time_value
        self.w_value.SetData(str(self.time_value.value))
        self.w_utc_datetime.SetData(str(self.time_value.utc_datetime))


    def create_layout(self):
        """
        Return a new instance of FUxLayoutBuilder
        with a layout that will be used for this dialog.
        """
        import acm
        builder = acm.FUxLayoutBuilder()
        builder.BeginVertBox()
        builder.AddInput("utc_datetime", "UTC date and time")
        builder.AddInput("value", "Value")
        builder.BeginHorzBox()
        builder.AddButton(OK_BUTTON_ID, self.ok_button_label, False, True)
        builder.AddFill()
        builder.AddButton(CANCEL_BUTTON_ID, "Close", False, True)
        builder.EndBox()
        builder.EndBox()
        return builder


    def init_layout(self, layout):
        """
        Initialize the GUI parts of the dialog's layout.
        """
        w_ok = layout.GetControl(OK_BUTTON_ID)
        w_ok.SetStandardFont("Bold")
        self.w_utc_datetime = layout.GetControl("utc_datetime")
        self.w_utc_datetime.ToolTip(("UTC date and time at which "
                                     "the indicated value is valid"))
        self.w_value = layout.GetControl("value")
        self.w_value.ToolTip(("The value which is valid "
                              "at the indicated UTC date and time"))
        self.w_value.SetFocus()
        self.load_time_value()


    def HandleCreate(self, layout_dialog, main_layout):
        """
        Handle the dialog's create event.
        """
        self.layout_dialog = layout_dialog
        self.layout_dialog.Caption("{0} time value".format(
            self.ok_button_label))
        self.init_layout(main_layout)


    def HandleApply(self):
        """
        Save the edited time value and return it.

        This function handles an event of pressing a button
        with name == "ok".
        """
        utc_datetime_string = self.w_utc_datetime.GetData()
        # FIXME: Use some function to check the validity
        # of the provided datetime string.
        try:
            utc_datetime = datetime.strptime(utc_datetime_string,
                                             "%Y-%m-%d %H:%M:%S.%f")
        except ValueError as exc:
            shell = self.layout_dialog.Shell()
            message = ("The provided date and time '{0}' is not valid. "
                       "Reason: {1}").format(utc_datetime_string, exc)
            show_information_window(shell, message)
            return
        string_value = self.w_value.GetData()
        if string_value and self.validating_function:
            try:
                self.validating_function(string_value)
            except WrongValueError as exc:
                shell = self.layout_dialog.Shell()
                message = ("The provided value '{0}' is not valid. "
                           "Reason: {1}").format(string_value, exc)
                show_information_window(shell, message)
                return
        #FIXME: Not necessary?
        self.time_value = TimeValue(string_value, utc_datetime=utc_datetime)
        return self.time_value


def demo_launch():
    """
    Launch the open dialog as a standalone application within Front Arena.
    The parent of this dialog will be the session manager.
    """
    import acm
    shell = acm.UX().SessionManager().Shell()
    extension_contexts = acm.FExtensionContext.Select("")
    rows = [(context.Name(),
             context.UpdateUser(),
             timestamp_to_str(context.UpdateTime()),
             context.CreateUser(),
             timestamp_to_str(context.CreateTime()))
            for context in extension_contexts]
    column_names = ["Name",
                    "Update user",
                    "Update time",
                    "Create user",
                    "Create time"]
    selected_name = acm.GetDefaultContext().Name()
    dialog = OpenDialog(rows, column_names, selected_name)
    builder = dialog.create_layout()
    return_value = acm.UX().Dialogs().ShowCustomDialogModal(shell,
                                                            builder,
                                                            dialog)
    print("Return value == '{0}'".format(return_value))


#demo_launch()
