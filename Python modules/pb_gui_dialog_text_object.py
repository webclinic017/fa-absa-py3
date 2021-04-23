"""
A module which contains class for creating a GUI
for editing the text objects.
"""

from FUxCore import LayoutDialog

from pb_gui_core import (CANCEL_BUTTON_ID,
                         OK_BUTTON_ID,
                         OpenDialog,
                         show_question_window,
                         timestamp_to_str)
from pb_storage_core import get_text_object


class TextObjectEditDialog(LayoutDialog):

    """
    A class which represents a dialog
    for editing the text objects.
    """

    def __init__(self, text_object_id, editable=False):
        """
        Initialize the instance.
        """
        self.text_object_id = text_object_id
        self.editable = editable
        self.edited = False


    def load_text_object(self, text_object_id=None):
        """
        Load a text object with the provided name.
        """
        if text_object_id is not None:
            self.text_object_id = text_object_id
        text_object = get_text_object(self.text_object_id)
        self.w_text_object_id.SetData(text_object.Name())
        self.w_text_object_subtype.SetData(text_object.SubType())
        self.w_text_object_text.SetData(text_object.Text())


    def create_layout(self):
        """
        Return a new instance of FUxLayoutBuilder
        with a layout that will be used for this dialog.
        """
        import acm
        builder = acm.FUxLayoutBuilder()
        builder.BeginVertBox()
        builder.BeginHorzBox()
        builder.AddButton("open", " Open ", False, True)
        builder.AddInput("text_object_id", "Text object ID")
        builder.AddInput("text_object_subtype", "Text object subtype")
        builder.EndBox()
        builder.AddText("text_object_text", 600, 800)
        builder.BeginHorzBox()
        builder.AddButton(OK_BUTTON_ID, " Edit ", False, True)
        builder.AddFill()
        builder.AddLabel("notice", "..... loading  .....", False, True)
        builder.AddFill()
        builder.AddButton(CANCEL_BUTTON_ID, " Close ", False, True)
        builder.EndBox()
        builder.EndBox()
        return builder


    def init_layout(self, layout):
        """
        Initialize the GUI parts of the dialog's layout.
        """
        w_open = layout.GetControl("open")
        w_open.ToolTip("Open a custom text object")
        w_open.AddCallback("Activate", self.open_text_object_callback, w_open)
        self.w_ok = layout.GetControl(OK_BUTTON_ID)
        self.w_ok.SetStandardFont("Bold")
        if not self.editable:
            self.w_ok.Enabled(False)
        self.w_notice = layout.GetControl("notice")
        self.w_notice.SetStandardFont("Bold")
        self.w_notice.SetAlignment("Center")
        self.w_notice.SetData("")
        self.w_text_object_id = layout.GetControl("text_object_id")
        self.w_text_object_id.ToolTip("The ID of the text object")
        self.w_text_object_id.Editable(False)
        self.w_text_object_subtype = layout.GetControl("text_object_subtype")
        self.w_text_object_subtype.ToolTip("The subtype of the text object")
        self.w_text_object_subtype.Editable(False)
        self.w_text_object_text = layout.GetControl("text_object_text")
        self.w_text_object_text.ToolTip(
            "The actual text stored in the text object")
        self.w_text_object_text.SetStandardFont("Monospace")
        self.w_text_object_text.Editable(False)
        self.load_text_object()


    def open_text_object_callback(self, _ux_control, _unused):
        """
        Launch a window for opening a new text object.
        """
        import acm
        shell = self.layout_dialog.Shell()
        subtype = self.w_text_object_subtype.GetData()
        if subtype:
            selection_string = "subType='{0}'".format(subtype)
        else:
            selection_string = ""
        text_objects = acm.FCustomTextObject.Select(selection_string)
        text_objects_data = [(text_object.Name(),
                              timestamp_to_str(text_object.UpdateTime()),
                              text_object.SubType(),
                              text_object.Owner(),
                              timestamp_to_str(text_object.CreateTime()))
                             for text_object in text_objects]
        column_labels = ["Name",
                         "Update time",
                         "Subtype information",
                         "Owner",
                         "Create time"]
        dialog = OpenDialog(text_objects_data,
                            column_labels,
                            self.text_object_id)
        builder = dialog.create_layout()
        text_object_id = acm.UX().Dialogs().ShowCustomDialogModal(
            shell, builder, dialog)
        self.load_text_object(text_object_id)
        self.make_edited(False)


    def make_edited(self, value):
        """
        Mark the current dialog as edited or not edited.
        """
        if value:
            import acm
            reddish = acm.UX().Colors().Create(195, 31, 0)
            self.w_notice.SetColor("Text", reddish)
            self.w_notice.SetData("edited")
            self.w_ok.Label("Save")
            self.w_text_object_subtype.Editable(True)
            self.w_text_object_text.Editable(True)
            self.edited = True
        else:
            self.w_notice.SetData("")
            self.w_ok.Label("Edit")
            self.w_text_object_subtype.Editable(False)
            self.w_text_object_text.Editable(False)
            self.edited = False


    def HandleCreate(self, layout_dialog, main_layout):
        """
        Handle the dialog's create event.
        """
        self.layout_dialog = layout_dialog
        self.layout_dialog.Caption(
            "Text Object '{0}'".format(self.text_object_id))
        self.init_layout(main_layout)


    def HandleApply(self):
        """
        Toggle the "ok" button's label between "Edit" and "Save",
        based on whether the currently opened text object
        has been already edited or not.

        This function handles an event of pressing a button
        with name == "ok".
        """
        if self.edited:
            shell = self.layout_dialog.Shell()
            message = ("Are you sure you want to save "
                       "the entered text into "
                       "a text object with "
                       "ID {0}?").format(repr(self.text_object_id))
            answer = show_question_window(shell, message)
            if answer == "Button1": # The first button (Yes) has been pressed.
                data = self.w_text_object_text.GetData()
                text_object = get_text_object(self.text_object_id)
                text_object.Text(data)
                text_object.Commit()
                information_message = ("The text object {0} "
                                       "have been saved.").format(
                                           repr(self.text_object_id))
                print(information_message)
                self.make_edited(False)
            else:
                information_message = "Nothing has been saved."
                print(information_message)
        else:
            self.make_edited(True)


def demo_launch():
    """
    Launch the text object edit dialog
    as a standalone application within Front Arena.
    The parent of this dialog will be the session manager.
    """
    import acm
    shell = acm.UX().SessionManager().Shell()
    dialog = TextObjectEditDialog("pb_funds", editable=True)
    builder = dialog.create_layout()
    acm.UX().Dialogs().ShowCustomDialogModal(shell, builder, dialog)


#demo_launch()
