""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/settlement/etc/FSettlementSwiftXMLFieldsTemplate.py"
"""----------------------------------------------------------------------------
MODULE
    FSettlementSwiftXMLFieldsTemplate

DESCRIPTION    
    Before changing these fields, copy the content to a new module called
    FSettlementSwiftXMLFields. After adding or changing this module
    the Documentation ATS needs to be restarted for the changes to take affect.
----------------------------------------------------------------------------"""

# --------------
# FIELDS
# --------------
# Changes in the following fields trigger corresponding confirmation update

field_dict = {}

field_dict['SETTLEMENT'] = \
    ['ACQUIRER_ACCNAME', 'ACQUIRER_ACCOUNT', 'ACQUIRER_ACCOUNT_NETWORK_NAME',
    'ACQUIRER_PTYID', 'ACQUIRER_PTYNBR', 'AMOUNT', 'CFWNBR', 
    'COUNTERPARTY_PTYNBR', 'CURR', 'DELIVERY_TYPE', 'DIVIDEND_SEQNBR', 
    'DOCUMENT', 'FROM_PRFNBR', 'MESSAGE_TYPE', 'NETTING_RULE_SEQNBR', 
    'NOTIFICATION_DAY', 'ORG_SEC_NOM', 'PARTY_ACCOUNT',
    'PARTY_ACCOUNT_NETWORK_NAME', 'PARTY_PTYID', 'PAYNBR',
    'POST_SETTLE_ACTION', 'PRIMARY_ISSUANCE', 'RELATION_TYPE', 'REF_PAYNBR',
    'REF_SEQNBR', 'REF_TYPE', 'RESTRICT_NET', 'SEC_INSADDR', 
    'SETTLE_CATEGORY', 'SETTLE_SEQNBR', 'SETTLED_AMOUNT', 
    'SETTLEINSTRUCTION_SEQNBR', 'STATUS', 'STATUS_EXPLANATION', 
    'TEXT', 'TO_PRFNBR', 'TRDNBR', 'TYPE', 'VALUE_DAY']

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

