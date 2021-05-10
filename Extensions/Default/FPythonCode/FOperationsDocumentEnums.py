""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/operations_document/etc/FOperationsDocumentEnums.py"
"""
Module for defining enums as python classes. Do not import anything into this module.
If new values are added to existing enums or new enums are added make sure to update or
add new tests to test this in test_FOperationsDocumentEnums.py
"""

class DocumentFormat:
    INVALID = 0
    RTF     = 1
    PDF     = 2
    ASCII   = 3

class DataType:
    INVALID = 0
    BINARY  = 1
    TEXT    = 2

class OperationsDocumentStatus:
    NEW                             = 'New'
    EXCEPTION                       = 'Exception'
    PENDING_GENERATION              = 'Pending generation'
    GENERATED                       = 'Generated'
    SENDING                         = 'Sending'
    SENT_SUCCESSFULLY               = 'Sent successfully'
    SEND_FAILED                     = 'Send failed'

class OperationsDocumentType:
    SWIFT                           = 'SWIFT'
    LONGFORM                        = 'Longform'