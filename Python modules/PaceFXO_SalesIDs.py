"""Writes PACE FXO traders to a file."""
# Desk   Requester        Developer              CR Number
# What
# =============================================================================

# OPS    PACE-FXO         Lukas Paluzga          CHNG0001203303
# Writes PACE FXO traders to a file. The file is then uploaded to Tumbleweed.
# See http://confluence.barcapint.com/display/AbCapFxIT/Environments for details.

import os
import acm 
import at

FXO_GROUP_NAME = 'FO PACE FXO Trader'

ael_variables = at.ael_variables.AelVariableHandler()
ael_variables.add('output_folder', label = 'Output folder', mandatory = 1)
ael_variables.add('file_name', label = 'File name', mandatory = 1, default = 'PaceFXO_SalesIDs.txt')

def ael_main(params):
    # Get all users belonging to FXO_GROUP_NAME friendgroup.
    friendgroups = acm.FFriendGroup.Select('userGroup="{0}"'.format(FXO_GROUP_NAME)) 
    
    filename = os.path.join(params['output_folder'], params['file_name'])
    with open(filename, 'wb') as f:
        for fg in friendgroups:
            f.write(fg.User().Name())
            # Forcing Windows-style line ends as the other side cannot process UNIX-style
            f.write("\r\n") 
    
    print("Output written to", filename)
    print("Completed successfully")
