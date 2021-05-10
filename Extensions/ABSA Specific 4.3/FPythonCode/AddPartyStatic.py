'''
DESCRIPTION
    Updated party static from the PartyStaticSetup extension

HISTORY

2017-06-20      CHNG0004671894  Willie van der Bank     Initial implementation
'''

import acm
from SAGEN_Set_Additional_Info import set_AdditionalInfoValue_ACM

def addMain(party,
            StriataAcceptReject,
            StriataPassword
            ):
    if StriataAcceptReject:
        set_AdditionalInfoValue_ACM(party, 'StriataAcceptReject', StriataAcceptReject)
    if StriataPassword:
        set_AdditionalInfoValue_ACM(party, 'StriataPassword', StriataPassword)
