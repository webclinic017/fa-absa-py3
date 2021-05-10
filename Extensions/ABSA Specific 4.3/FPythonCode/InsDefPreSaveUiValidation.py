"""UI validation hooks. Call the logic that's in a regular python module."""


from GValidation import validate_gui


def ael_custom_dialog_show(shell, params):
    return validate_gui(shell, params)


def ael_custom_dialog_main(_parameters, dict_extra):
    return dict_extra
