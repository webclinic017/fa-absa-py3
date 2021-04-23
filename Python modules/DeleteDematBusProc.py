import os

import acm
from demat_isin_mgmt_menex import current_authorised_amount, MMSS_ISIN_REQUEST_STATE_CHART_NAME

import FRunScriptGUI

ins_key = '0'

# Variable Name, Display Name, Type, Candidate Values,
# Default, Mandatory, Multiple, Description, Input Hook, Enabled
ael_variables = [[ins_key, 'Instrument Selection', 'FInstrument', None,
        None, 0, 1, 'Demat Instrument selection.', None, 1]]

def ael_main(parameters):
    instruments = parameters[ins_key]
    for ins in instruments:
        processes = acm.BusinessProcess.FindBySubjectAndStateChart(ins, MMSS_ISIN_REQUEST_STATE_CHART_NAME)
        for p in processes:
            p.Delete()
            print('Business process delete for instrument [%s]' % (ins.Name()))
