""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/business_data_upload/etc/FBusinessDataUploadUtils.py"
"""--------------------------------------------------------------------------
MODULE
    FBusinessDataUploadUtils

    (c) Copyright 2014 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-----------------------------------------------------------------------------"""

import FStateChartUtils as Utils


def CreateStateChart(name='Data Upload'):
    # Create the default state chart for Business Data Upload
    limit = 'Single'
    layout = 'Unidentified,445,328;Successful,835,-71;Invalid data,443,96;Pending upload,676,99;Comparison,578,-254;Ready,164,42;Discrepancy,579,-86;'
    definition = {
        'Ready':                {'Identified': 'Comparison',
                                 'Not identified': 'Unidentified'},
        'Unidentified':         {'Create business object': 'Pending upload',
                                 'Validation failed': 'Invalid data'},
        'Invalid data':         {'Redo' : 'Ready'},
        'Discrepancy':          {'Update business object': 'Pending upload',
                                 'Redo' : 'Ready'},
        'Comparison':           {'Mismatch found': 'Discrepancy',
                                 'Matched': 'Successful'},
        'Pending upload':       {'Validation failed': 'Invalid data',
                                 'Uploaded successfully': 'Successful'}
    }

    return Utils.CreateStateChart(name, definition, layout, limit)