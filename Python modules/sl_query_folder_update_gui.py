"""-----------------------------------------------------------------------------
PROJECT                 :  Security Borrowing and Lending
PURPOSE                 :  Updates a list of Query Folders. The Query Folders 
                           should select trades from portfolios based on the 
                           values of additional info fields on the portfolios.
                           The Query Folders are much faster if the portfolios 
                           are specified explicitly as opposed to filterring
                           on the additional info field values. This script 
                           sets the portfolios on the Query Folders.
DEPATMENT AND DESK      :  Prime Services, Securities Lending
REQUESTER               :  Linda Breytenbach
DEVELOPER               :  Francois Truter
CR NUMBER               :  332137

HISTORY
=============================================================================
Date       Change no Developer          Description
-----------------------------------------------------------------------------
2010-06-08 332137    Francois Truter    Initial Implementation

-----------------------------------------------------------------------------"""

import acm
from sl_query_folder_update import queryFoldersKey, updateQueryFolders

#Variable Name, Display Name, Type, Candidate Values, Default, Mandatory, Multiple, Description, Input Hook, Enabled
ael_variables = [
    [queryFoldersKey, 'Query Folders', 'FStoredASQLQuery', None, None, 0, 1, 'The Query Folders that need to be recreated', None, 1]
]

def ael_main(parameters):
    try:
        updateQueryFolders(parameters)
    except Exception as ex:
        acm.Log('Error in sl_query_folder_update_gui: %s' % str(ex))
        

