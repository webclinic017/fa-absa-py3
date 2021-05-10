""" Compiled: 2020-09-18 10:38:46 """

#__src_file__ = "extensions/accounting/etc/FAccountingExceptions.py"

import exceptions

#-------------------------------------------------------------------------
class DynamicAccountException(exceptions.Exception):
    def init(self, args = None):
        super(DynamicAccountException, self).__init__(args)

#-------------------------------------------------------------------------
class IncorrectLedgerKeyException(exceptions.Exception):
    def init(self, args = None):
        super(IncorrectLedgerKeyException, self).__init__(args)
        