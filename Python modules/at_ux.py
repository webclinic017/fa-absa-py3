"""Arena Toolkit (at) -- User Experience (UX) utility functions.

History
=======

2016-12-29 Vojtech Sidorin  Initial implementation.
"""

import acm


# NOTE: The following constants are only valid for the use with the modeless
# AEL message box, i.e. the msg_box function. If possible, use rather the newer
# ACM alternative, i.e. the msg_dialog function.

# Button layout codes. Determine the buttons that will be shown in the
# modeless message box.
OK_LAYOUT = 0
OK_CANCEL_LAYOUT = 1
ABORT_RETRY_IGNORE_LAYOUT = 2
YES_NO_CANCEL_LAYOUT = 3
YES_NO_LAYOUT = 4
RETRY_CANCEL_LAYOUT = 5
# Button codes returned by the modeless message box after the user clicks one.
OK_CLICKED = 1
CANCEL_CLICKED = 2
ABORT_CLICKED = 3
RETRY_CLICKED = 4
IGNORE_CLICKED = 5
YES_CLICKED = 6
NO_CLICKED = 7

def msg_box(msg, title="Information", buttons=OK_LAYOUT):
    """Show a modeless message box and return the code of the clicked button.

    This function wraps the older AEL function msgBox. Module-level constants
    can be used to set the buttons layout and read the code of the clicked
    button.

    Positional arguments:
    msg (str) -- message to be shown

    Keyword arguments:
    title (str) -- title of the message box
    buttons (int) -- buttons to show

    Example use:

        msg = "Do you wish to continue?"
        clicked_button = msg_box(msg, title="Question", buttons=YES_NO_LAYOUT)
        if clicked_button == YES_CLICKED:
            # Do some stuff.
            pass
        else:
            # Do some other stuff.
            pass
    """
    assert str(acm.Class()) == "FTmServer", "FA GUI is not running."
    msg_box_ = acm.GetFunction("msgBox", 3)
    return msg_box_(title, msg, buttons)


def msg_dialog(msg, type_="Information", shell=None, button1="OK", button2=None,
               button3=None, default_button="Button1", cancel_button="Button3"):
    """Show a modal dialog box and return the clicked button.

    This function wraps the newer ACM function MessageBox.

    Positional arguments:
    msg (str) -- message to be shown

    Keyword arguments:
    type_ (enum(FUxMessageBoxType)) -- type of the message box
    shell (FUxShell) -- shell of the parent frame; if set to None, the
        Session Manager (the main Prime window) will be used as the parent
    button1 (str) -- label of button 1
    button2 (str|None) -- label of button 2, None will hide the button
    button3 (str|None) -- label of button 3, None will hide the button
    default_button (enum(FUxMessageBoxButton)) -- default button (Enter)
    cancel_button (enum(FUxMessageBoxButton)) -- cancel button (Esc)

    Returns enum(FUxMessageBoxButton) corresponding to the button that was
    clicked, e.g. "Button1" or "Button2".

    Example use:

        question = "Do you wish to continue?"
        clicked_button = msg_dialog(question, type_="Question",
                                    shell=parent_shell, button3="Cancel")
        if clicked_button == "Button1":
            # Do some stuff.
            pass
        else:
            # Do some other stuff.
            pass
    """
    assert str(acm.Class()) == "FTmServer", "FA GUI is not running."
    if shell is None:
        shell = acm.UX().SessionManager().Shell()
    return acm.UX().Dialogs().MessageBox(shell, type_, msg, button1, button2,
                                         button3, default_button, cancel_button)
