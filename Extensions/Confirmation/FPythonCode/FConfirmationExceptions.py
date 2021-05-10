""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/confirmation/etc/FConfirmationExceptions.py"

import exceptions

#-------------------------------------------------------------------------
class ConfirmationClientValidationException(exceptions.Exception):
    def __init__(self, args = None):
        super(ConfirmationClientValidationException, self).__init__(args)