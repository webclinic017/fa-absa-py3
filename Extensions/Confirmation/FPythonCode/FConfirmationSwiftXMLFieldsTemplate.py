""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/confirmation/etc/FConfirmationSwiftXMLFieldsTemplate.py"
"""----------------------------------------------------------------------------
MODULE
    FConfirmationSwiftXMLFieldsTemplate -

DESCRIPTION
    Changes to any of these settings require a restart of both the
    confirmation ATS and the documentation ATS for the changes to
    take affect.
----------------------------------------------------------------------------"""

# --------------
# FIELDS
# --------------
# Changes in the following fields trigger corresponding confirmation update

field_dict = {}

# confirmation
field_dict['CONFIRMATION'] = \
    ['CHASER_CUTOFF', 'CHASING_SEQNBR', 'CONFIRMATION_SEQNBR', 
     'CONF_TEMPLATE_CHLNBR', 'DOCUMENT', 'MANUAL_MATCH', 'RESET_RESNBR',
     'STATUS', 'STATUS_EXPLANATION', 'TRANSPORT', 'TRDNBR', 'UPDAT_USRNBR']

# party
field_dict['PARTY'] = \
    ['ADDRESS', 'ADDRESS2', 'ATTENTION', 'CALCAGENT', 'CITY', 'CONTACT1',
     'CONTACT2', 'CORRESPONDENT_BANK', 'COUNTRY', 'DOCUMENT_DATE',
     'DOCUMENT_TYPE_CHLNBR', 'EMAIL', 'EXTERNAL_CUTOFF', 'FAX', 'FREE1',
     'FREE2', 'FREE3', 'FREE4', 'FREE5', 'FREE1_CHLNBR', 'FREE2_CHLNBR',
     'FREE3_CHLNBR', 'FREE4_CHLNBR', 'FULLNAME', 'FULLNAME2',
     'GUARANTOR_PTYNBR', 'INTERNAL_CUTOFF', 'ISDA_MEMBER', 'ISSUER',
     'LEGAL_FORM_CHLNBR', 'NOTIFY_RECEIPT', 'PARENT_PTYNBR', 'PTYID', 'PTYID2',
     'SWIFT', 'TELEPHONE', 'TELEX', 'TIME_ZONE', 'TYPE', 'ZIPCODE']
                                                
# party alias
field_dict['PARTYALIAS'] = \
    ['ALIAS', 'PTYNBR', 'TYPE']

# agreement
field_dict['AGREEMENT'] = \
    ['COUNTERPARTY_PTYNBR', 'DATED', 'DOCUMENT_TYPE_CHLNBR', 'INSTYPE',
     'INTERNDEPT_PTYNBR', 'UND_INSTYPE']

# account
field_dict['ACCOUNT'] = \
    ['ACCOUNT', 'ACCOUNT2', 'ACCOUNT3', 'ACCOUNT4', 'ACCOUNT5', 'CURR', 'NAME',
     'SWIFT', 'SWIFT2', 'SWIFT3', 'SWIFT4', 'DETAILS_OF_CHARGES', 'BIC_SEQNBR',
     'BIC2_SEQNBR', 'BIC3_SEQNBR', 'BIC4_SEQNBR', 'BIC5_SEQNBR',
     'NETWORK_ALIAS_TYPE', 'NETWORK_ALIAS_SEQNBR', 'CORRESPONDENT_BANK_PTYNBR',
     'CORRESPONDENT_BANK2_PTYNBR', 'CORRESPONDENT_BANK3_PTYNBR',
     'CORRESPONDENT_BANK4_PTYNBR', 'CORRESPONDENT_BANK5_PTYNBR',
     'INTERNAL_CUTOFF', 'EXTERNAL_CUTOFF', 'ACCOUNT_TYPE']
    
#trade
field_dict['TRADE'] = ['TRDNBR']

# trade account link
field_dict['TRADEACCOUNTLINK'] = []