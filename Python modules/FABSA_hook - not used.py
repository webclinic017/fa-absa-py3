'''
Willie van der bank
This module is part of the previous settlement solution and is not used anymore
'''

""" Based on Settlement:1.2.2.hotfix23 """
#-----------------------------------------------------------------------------------------------------------------
#  Developer           : Anwar, Heinrich Cronje, Willie van der Bank
#  Purpose             : Catered for payments using intermediaries, SND implementation, Bringing online of new desks
#  Department and Desk : Operations
#  Requester           : Miguel
#  CR Number           : 617525, 662927, 852496 08/12/2011
#-----------------------------------------------------------------------------------------------------------------

'''
HISTORY
=============================================================================================================
Date            Change no       Developer                       Description
-------------------------------------------------------------------------------------------------------------
2012-08-08      396485          Heinrich Cronje                 PRIME SERVICES DESK Implementation
2013-05-09      1007691         Pavel Saparov                   Removing /REC/ for MT103 in Field 70
2015-03-06      CHNG0002688904  Lawrence Mucheka                Added combination instrument type

-------------------------------------------------------------------------------------------------------------
'''
"""----------------------------------------------------------------------------
MODULE
    FABSA_hook - Module that is executed as AEL hook in AMBA

    (c) Copyright 2001 by Front Capital Systems AB. All rights reserved.

DESCRIPTION
    This module is used as an AEL Hook that extends/modifies outgoing as
    well as incoming Settlement AMBA messages. Check the flag
    ael_module_name in the AMBA ini-file for more information.

DATA-PREP
    Note that this file includes variables that need to be configured.

----------------------------------------------------------------------------"""
import ael, amb, string, time, acm, re
import FSettlementParameters
import SettlementConstants
import SettlementGLAccounts
from SAGEN_IT_Functions import get_lowest_settlement, get_Port_Struct_from_Port

"""----------------------------------------------------------------------------
MODULE
# Variables from the old FSettlementVariables reside in this section below
----------------------------------------------------------------------------"""

#days_back see FSettlementParameters.maximumDaysBack

# The number of days from today that settlements should be generated for.
# Days are specified per currency. New currencies can be added here.
days_curr = {'ZAR':7}

# Default Instrument types that are supported
# In order to exclude some Instrument types you are allowed to 
# reduce a number of items in this list (do not add anything)
valid_instrument_types = ['Deposit', 'Future/Forward', 'Option', 'Combination',
                          'VarianceSwap', 'Zero', 'CD', 'FRN',
                          'TotalReturnSwap', 'FRA', 'Swap', 'Cap',
                          'IndexLinkedSwap', 'Floor', 'CurrSwap',
                          'CreditDefaultSwap', 'Curr', 'Repo/Reverse', 'FxSwap', 'Commodity']

# List containing the names and values of additional infos on a cash flow record. Used for preventing
# creation of settlemetn records. The names and values, both of type string, have to be entered as tuple pairs.
# Example:  cash_flow_additional_infos = [('MyAdditionalInfo1', 'Exclude'), ('MyAdditionalInfo2', 'Prevent')]
cash_flow_additional_infos = []


"""----------------------------------------------------------------------------

# Variables from the old FSettlementVariables reside in this section above.
----------------------------------------------------------------------------"""

# Customerspecific variables, to be edited

# RESOURCES, this must represented in the the AMBA ini file
# the flag is called -receiver_sources {KMS,INTERPAY}
# where KMS is used for SWIFT/KMaster and INTERPAY for Internal payments
RESOURCES = ['KMS', 'INTERPAY', 'SWIFT']

# Variables for e-mail notifications, to be edited before use
# default = 0, means no e-mail notifications
SENDMAIL = 0

# E-mail address to be sent to (define e-mail groups on e-mail
#  server for multiple receivers)
EMAIL_RECEIVER = 'info@bank.com'

# Subject
SUBJECT = 'SWIFT-interface answer: Settlement'

# Message added to current message info (see function sendm_mail)
MESSAGE = 'Check the result in the Settlement Manager.'

# Settlement fields to be validated
validate_non_swift_chars = ['ACQUIRER_ACCNAME', 'ACQUIRER_ACCOUNT', \
'ACQUIRER_PTYID', 'PARTY_ACCNAME', 'PARTY_ACCOUNT', 'PARTY_PTYID', 'TEXT']

# max length of the line is 50 according to the SWIFT requirement
# default NARRATIVE_LENGTH = 50
NARRATIVE_LENGTH = 50

# Identifies type of operation
# Default value of MT103, MT205MT103, MT202MT103 field 23B
BANK_OPERATION_CODE = 'CRED'

#"our" bank's party short name. Will be used for SWIFT code of currency acc.
OUR_BANK = 'ABSA BANK LTD'

#SWIFT code of the ordering institution field 52A
ORDERING_INSTITUTION = 'ABSAZAJJ'

#Separator
SEPARATOR = '|'

#Valid portfolio's acquirer ptynbr
#6292 = CREDIT DERIVATIVES DESK
ACQUIRER_FOR_VALID_PORTF = [6292]

#CREDIT DERIVATIVES DESK valid Compound Portfolios prfnbr
#1512 = 1574,   1518 = 1571,    1631 = 1573,    1644 = 2792,    1742 = 2793,    1746 = 2794,    1827 = 1572,    1884 = 3306,    1098 = 0057
VALID_PORTF_FOR_ACQUIRER = [1512, 1518, 1631, 1644, 1742, 1746, 1827, 1884, 1098]

# ANSI char table including decimal keys (0-255) and their transition.
# By default non swift characters are replaced by space.
# You have right to change space to some other approved sign but
# note that emtpy string should not be used (use at least space)!
# More ASCII info http://www.neurophys.wisc.edu/www/comp/docs/ascii.html
# When you have adopted dict_trans please run 
# check_transitions()

dict_trans = {0: ' ', 1: ' ', 2: ' ', 3: ' ', 4: ' ', 
5: ' ', 6: ' ', 7: ' ', 8: ' ', 9: ' ', 10: '\n', 
11: ' ', 12: ' ', 13: '\n', 14: ' ', 15: ' ', 16: ' ', 
17: ' ', 18: ' ', 19: ' ', 20: ' ', 21: ' ', 22: ' ',
23: ' ', 24: ' ', 25: ' ', 26: ' ', 27: ' ', 28: ' ',
29: ' ', 30: ' ', 31: ' ', 32: ' ', 33: ' ', 34: ' ', 35: ' ',
36: ' ', 37: ' ', 38: ' ',39: "'", 40: '(', 41: ')', 42: ' ', 43: '+', 
44: ',', 45: '-', 46: '.', 47: '/', 48: '0', 49: '1', 50: '2', 51: '3',
52: '4', 53: '5', 54: '6',55: '7', 56: '8', 57: '9', 58: ':', 59: ' ',
60: ' ', 61: ' ', 62: ' ', 63: '?', 64: ' ', 65: 'A', 66: 'B', 67: 'C',
68: 'D', 69: 'E', 70: 'F', 71: 'G', 72: 'H', 73: 'I', 74: 'J', 75: 'K',
76: 'L', 77: 'M', 78: 'N', 79: 'O', 80: 'P', 81: 'Q', 82: 'R', 83: 'S', 
84: 'T', 85: 'U', 86: 'V', 87: 'W', 88: 'X', 89: 'Y', 90: 'Z', 91: ' ',
92: '/', 93: ' ', 94: ' ', 95: ' ', 96: ' ', 97: 'a', 98: 'b', 99: 'c',
100: 'd', 101: 'e', 102: 'f', 103: 'g', 104: 'h', 105: 'i', 106: 'j',
107: 'k', 108: 'l', 109: 'm', 110: 'n', 111: 'o', 112: 'p', 113: 'q', 
114: 'r', 115: 's', 116: 't', 117: 'u', 118: 'v', 119: 'w', 120: 'x', 
121: 'y', 122: 'z', 123: ' ', 124: ' ', 125: ' ', 126: ' ', 
127: ' ', 128: ' ', 129: ' ', 130: ' ', 131: ' ', 132: ' ',
133: ' ', 134: ' ', 135: ' ', 136: ' ', 137: ' ', 138: ' ', 
139: ' ', 140: ' ', 141: ' ', 142: ' ', 143: ' ', 144: ' ', 
145: ' ', 146: ' ', 147: ' ', 148: ' ', 149: ' ', 150: ' ', 
151: ' ', 152: ' ', 153: ' ', 154: ' ', 155: ' ', 156: ' ', 
157: ' ', 158: ' ', 159: ' ', 160: ' ', 161: ' ', 162: ' ', 
163: ' ', 164: ' ', 165: ' ', 166: ' ', 167: ' ', 168: ' ', 
169: ' ', 170: ' ', 171: ' ', 172: ' ', 173: ' ', 174: ' ', 
175: ' ', 176: ' ', 177: ' ', 178: ' ', 179: ' ', 180: ' ', 
181: ' ', 182: ' ', 183: ' ', 184: ' ', 185: ' ', 186: ' ', 
187: ' ', 188: ' ', 189: ' ', 190: ' ', 191: ' ', 192: ' ', 
193: ' ', 194: ' ', 195: ' ', 196: ' ', 197: ' ', 198: ' ', 
199: ' ', 200: ' ', 201: ' ', 202: ' ', 203: ' ', 204: ' ', 
205: ' ', 206: ' ', 207: ' ', 208: ' ', 209: ' ', 210: 'O', 
211: 'O', 212: 'O', 213: 'O', 214: 'O', 215: ' ', 216: ' ', 
217: 'U', 218: 'U', 219: 'U', 220: 'U', 221: 'Y', 222: ' ', 
223: ' ', 224: 'a', 225: 'a', 226: 'a', 227: 'a', 228: 'a', 
229: 'a', 230: ' ', 231: 'c', 232: 'e', 233: 'e', 234: 'e', 
235: 'e', 236: 'i', 237: 'i', 238: 'i', 239: 'i', 240: ' ', 
241: 'n', 242: 'o', 243: 'o', 244: 'o', 245: 'o', 246: 'o', 
247: ' ', 248: ' ', 249: 'u', 250: 'u', 251: 'u', 252: 'u', 
253: 'y', 254: ' ', 255: 'y'}

"""aef-------------------------------------------------------------------------
hook::add_swift_tag

Hook function **add_swift_tag** is a part of this module and is used for
populating outgoing AMBA settlement messages. In order to be called as a
sender AMBA hook, the name of this function needs to be stated in the AMBA
ini file as an 'ael_sender_add'.

@category AMBA
@param e:ael_entity An entity - function only handles Settlement
@param op:string Database event such as 'Update', 'Insert' or 'Delete'
@return tuple List that includes added fields. Note that if the List is not
returned, no AMBA message will be sent.
----------------------------------------------------------------------------"""
def add_swift_tag(e, op):
    'The name of this function responds the one stated as \
    -ael_sender_add in the AMBA ini-file.\
    Note that if you are using MessageAdaptation hook then\
    you need to configure it to run this function. For more\
    information see FCA 2105'

    lst = []
    update_status_add = ['Released']
    if e:
        if e.record_type == 'Settlement':
            if op == "Update" and e.status in update_status_add and not e.post_settle_action:# post settle action not to be sent out
            
                #Anwar Refactor - took out the function calls from the building of the list so that we can manipulate the individual tag values
                #without having to jump through hoops to amend them in the list
                
                MESSAGE_TYPE = get_Message_Type(e)
                DESTINATION_ADDRESS = validateSWIFTCode(get_Destination_Address(e, MESSAGE_TYPE))
                DESTINATION_ADDRESS2 = ''                
                if MESSAGE_TYPE == 'MT205C103':
                    DESTINATION_ADDRESS2 = validateSWIFTCode(get_Destination_Address(e, 'MT205C205'))
                elif MESSAGE_TYPE == 'MT202C103':
                    DESTINATION_ADDRESS2 = validateSWIFTCode(get_Destination_Address(e, 'MT202C202'))
                RELATED_REFERENCE = get_related_reference(e)
                ACQUIRER_ACC_NBR = get_acq_account(e)
                
                CORR_BANK_CURR_CORR_BANK_SWIFT = validateSWIFTCode(get_corr_bank_curr_corr_bank_SWIFT(e))
                CORR_BANK_CURR_CORR_BANK_BRANCH = get_corr_bank_curr_corr_bank_BRANCH(e)
                CORR_BANK_CURR_CORR_BANK_ACCOUNT = get_corr_bank_curr_corr_bank_ACCOUNT(e)
                
                CORR_BANK_SWIFT = validateSWIFTCode(get_corr_bank_SWIFT(e))
                CPTY_SWIFT = validateSWIFTCode(get_counterparty_SWIFT(e))
                CORR_BANK_BRANCH = get_corr_branch(e, MESSAGE_TYPE == 'MT103')
                CORR_ACC_NBR = get_corr_acc(e)
                CPTY_FULLNAME = get_party_fullname(e)
                REMITTANCE_INFO = get_adhoc_info(e)
                DETAILS_OF_CHARGES = get_detail_of_charges(e)
                
                SENDER_RECEIVER_INFO = get_sender_reciever_info(e, MESSAGE_TYPE)
                SENDER_RECEIVER_INFO_2 = ''                
                if MESSAGE_TYPE == 'MT205C103':
                    SENDER_RECEIVER_INFO_2 = get_sender_reciever_info(e, 'MT205C205')
                
                INTER_SWIFT = validateSWIFTCode(get_Inter_SWIFT_code(e, MESSAGE_TYPE))
                CASH_BOOK = get_cashbook_info(e)
                CAPITAL_EVENTREF = get_capital_eventRef(e)
                
                if MESSAGE_TYPE == 'MT202C103':
                    SENDER_CORR = validateSWIFTCode(get_our_curr_NOSTRO_SWIFT(e))
                else:
                    SENDER_CORR = validateSWIFTCode(get_sender_corr(e))                
                
                if ((MESSAGE_TYPE == 'MT202C103') and (DESTINATION_ADDRESS2 == CORR_BANK_CURR_CORR_BANK_SWIFT)):
                    MESSAGE_TYPE = 'MT103'
                    DESTINATION_ADDRESS = DESTINATION_ADDRESS2
                    DESTINATION_ADDRESS2 = ''
                    SENDER_CORR = ''
                if ((MESSAGE_TYPE == 'MT205C103') and (SettlementConstants.isVostro(e))):
                    MESSAGE_TYPE = 'VOSTRO'
                
                #Message Type                
                lst.append(['MSG_TYPE', MESSAGE_TYPE])
                #Destination Address
                lst.append(['DESTINATION_ADDRESS', DESTINATION_ADDRESS])                
                lst.append(['DESTINATION_ADDRESS_2', DESTINATION_ADDRESS2])                    
                #Related Reference
                lst.append(['RELATED_REFERENCE', RELATED_REFERENCE])
                #Bank Operation Code
                lst.append(['BANK_OPERATION_CODE', BANK_OPERATION_CODE])
                #Acquirer Account Number
                lst.append(['ACQUIRER_ACC_NBR', ACQUIRER_ACC_NBR])
                #Ordering Institution
                lst.append(['ORDERING_INSTITUTION', validateSWIFTCode(ORDERING_INSTITUTION)])
                #Sender's correspondent SWIFT code
                lst.append(['SENDER_CORR', SENDER_CORR])                
                #Correspondent Bank's currency Correspondent Bank's SWIFT code
                lst.append(['CORR_BANK_CURR_CORR_BANK_SWIFT', CORR_BANK_CURR_CORR_BANK_SWIFT])                
                #Correspondent Bank's SWIFT code
                lst.append(['CORR_BANK_SWIFT', CORR_BANK_SWIFT])
                #Correspondent Bank's branch code
                lst.append(['CORR_BANK_BRANCH', CORR_BANK_BRANCH])
                #Correspondent Bank's account number
                lst.append(['CORR_ACC_NBR', CORR_ACC_NBR])
                #Counterparty Fullname
                lst.append(['CPTY_FULLNAME', CPTY_FULLNAME])
                #Remittance information
                lst.append(['REMITTANCE_INFO', REMITTANCE_INFO])
                #Details of charges
                lst.append(['DETAILS_OF_CHARGES', DETAILS_OF_CHARGES])
                #Sender to reciever information
                lst.append(['SENDER_RECIEVER_INFO', SENDER_RECEIVER_INFO])
                #Intermediary SWIFT code - Only first populated one
                lst.append(['INTER_SWIFT', INTER_SWIFT])
                #Details of cashbook name to append to seqnbr on field 20
                lst.append(['CASH_BOOK', CASH_BOOK])
                #Field 21 is a mirror of 20 except for mm demat in which case 21 is the capital event ref
                lst.append(['CAPITAL_EVENTREF', CAPITAL_EVENTREF])
                #Used in field 58 when a cpty swift code exists
                lst.append(['CPTY_SWIFT', CPTY_SWIFT])
                #Correspondent Bank's currency Correspondent Bank's branch code
                lst.append(['CORR_BANK_CURR_CORR_BANK_BRANCH', CORR_BANK_CURR_CORR_BANK_BRANCH])
                #Correspondent Bank's currency Correspondent Bank's account code
                lst.append(['CORR_BANK_CURR_CORR_BANK_ACCOUNT', CORR_BANK_CURR_CORR_BANK_ACCOUNT])                
                #Sender to reciever information 2 for combos
                lst.append(['SENDER_RECIEVER_INFO_2', SENDER_RECEIVER_INFO_2])
            elif op == "Update" and e.status in update_status_add and \
                e.post_settle_action:
                ael.log('FABSA_hook caught settlement update but')
                ael.log('no additional SWIFT tags are appended when it is'\
                        'post settle action')

    return lst
  
def validateSWIFTCode(swiftCode):
    if TESTMESSAGES:
        if swiftCode:
            swiftCode = swiftCode[0:len(swiftCode)-1] + '0'
    return swiftCode

"""aef-------------------------------------------------------------------------
add_swift_tag functions

Functions to retrieve all the information for the outgoing SWFIT message
----------------------------------------------------------------------------"""
#Get the SWIFT alias of a Party
def get_SWIFT(party):
    SWIFT = ''
    if party:
        if party.aliases().members() != []:
            for alias in party.aliases():
                if alias.type.alias_type_name == 'SWIFT':
                    SWIFT = alias.alias

    return validate(SWIFT)

#Get the correspondent's bank SWIFT code. Destination Address
def get_corr_bank_SWIFT(settl):
    corr_bank_SWIFT = ''
    if settl.their_corr_bank != '':
        corr_bank = ael.Party[settl.their_corr_bank]
        corr_bank_SWIFT = get_SWIFT(corr_bank)
                
    return validate(corr_bank_SWIFT)


#Get the correspondent's bank SWIFT code. Field 57a, 58a
def get_counterparty_SWIFT(settl):
    counterparty_SWIFT = ''
    if settl.counterparty_ptynbr != '':
        counterparty_SWIFT = get_SWIFT(settl.counterparty_ptynbr)
                
    return validate(counterparty_SWIFT)


#Get the OUR_BANK's SWIFT code based on the currency of the settlement.
def get_our_curr_NOSTRO_SWIFT(settl):
    our_curr_NOSTRO_SWIFT = ''
    party = ael.Party[OUR_BANK]
    for acc in party.accounts():
        if acc.curr.insid == settl.curr.insid:
            our_curr_NOSTRO_SWIFT = get_SWIFT(acc.correspondent_bank_ptynbr)
            
    return validate(our_curr_NOSTRO_SWIFT)

#Get the correspondent bank's currency corresponding bank's SWIFT code. Destination Address, Field 54a, 57a
def get_corr_bank_curr_corr_bank_SWIFT(settl):
    corr_bank_curr_corr_bank_SWIFT = ''
    if settl.their_corr_bank != '':        
        corr_bank = ael.Party[settl.their_corr_bank]
        for acc in corr_bank.accounts():
            if acc.curr.insid == settl.curr.insid:
                corr_bank_curr_corr_bank_SWIFT = get_SWIFT(acc.correspondent_bank_ptynbr)
                break
    
    return validate(corr_bank_curr_corr_bank_SWIFT)

#Get the correspondent bank's currency corresponding bank's SWIFT code. Destination Address, Field 54a, 57a
def get_corr_bank_curr_corr_bank_BRANCH(settl):
    corr_bank_curr_corr_bank_BRANCH = ''
    if settl.their_corr_bank != '':        
        corr_bank = ael.Party[settl.their_corr_bank]        
        for acc in corr_bank.accounts():
            if acc.curr.insid == settl.curr.insid:
                if acc.account != '':
                    findSpace = acc.account.find(' ')
                    if findSpace != -1:
                        if acc.curr.insid == 'ZAR':
                            corr_bank_curr_corr_bank_BRANCH = '//ZA' + acc.account[:findSpace]
                        else:
                            corr_bank_curr_corr_bank_BRANCH = '//' +  acc.account[:findSpace]
                break
    
    return validate(corr_bank_curr_corr_bank_BRANCH)

def get_corr_bank_curr_corr_bank_ACCOUNT(settl):
    corr_bank_curr_corr_bank_ACCOUNT = ''
    if settl.their_corr_bank != '':        
        corr_bank = ael.Party[settl.their_corr_bank]        
        for acc in corr_bank.accounts():
            if acc.curr.insid == settl.curr.insid:
                if acc.account != '':
                    if acc.account.__contains__('DIRECT'):
                        corr_bank_curr_corr_bank_ACCOUNT = ''
                    else:
                        findSpace = acc.account.find(' ')
                        if findSpace == -1:
                            corr_bank_curr_corr_bank_ACCOUNT = '/' + acc.account
                        else:
                            corr_bank_curr_corr_bank_ACCOUNT = '/' +  acc.account[findSpace+1:]
                break
    
    return validate(corr_bank_curr_corr_bank_ACCOUNT)


#Correspondent Account Number. --> Field 58a, 59a
def get_corr_acc(settl):
    corr_acc = ''
    if settl:
        if settl.party_account != '':
            if settl.party_account.__contains__('DIRECT'):
                corr_acc = ''
            else:
                findSpace = settl.party_account.find(' ')
                if findSpace == -1:
                    corr_acc = '/' + (str)(settl.party_account)
                else:
                    corr_acc = '/' + (str)(settl.party_account[findSpace+1:])
                
    return validate(corr_acc)




#Cashbook Reference --> Field 108
def get_related_reference(settl):
    related_Reference = ''
    if settl:
        if settl.acquirer_ptynbr:
            if settl.acquirer_ptynbr.ptyid in ('Funding Desk'):
                related_Reference = 'MMA'
            elif settl.acquirer_ptynbr.ptyid in ('Money Market Desk'):
                if settl.trdnbr.insaddr.instype in ('Cap', 'CurrSwap', 'Floor', 'FRA', 'IndexLinkedSwap', 'Swap'):
                    related_Reference = 'DER'
                else:
                    related_Reference = 'MMA'
            else:
                related_Reference = 'DER'
                
    return validate(related_Reference)
    
#Related reference --> Field 20 --> should mirror field 20 except in the case of mm demat trades

def __get_capital_eventRef(settl):
    eventRef = ''
    if settl.trdnbr:
        if settl.trdnbr.add_info('MM_DEMAT_TRADE') == 'Yes':
            if settl.add_info('Capital_Event_Ref'):
                eventRef = settl.add_info('Capital_Event_Ref')
    return eventRef


def get_capital_eventRef(settl):
    eventRef = ''
    if settl:
        if settl.trdnbr:
            eventRef = __get_capital_eventRef(settl)
        else:
            #in the case of netted settlements we will use details from the earliest trade in the sequence
            mess = "get_capital_eventRef: Netted settlement without a trade number - get lowest settlement for " + str(settl.seqnbr)
            ael.log(mess)
            
            settlm = ael.Settlement[get_lowest_settlement(settl, [])[0]]
            if settlm:
                mess = "get_capital_eventRef: Get MM_DEMAT_TRADE on trade linked to " + str(settlm.seqnbr)
                ael.log(mess)
                
                eventRef = __get_capital_eventRef(settlm)
            else:
                ael.log("Error in retrieving lowest settlement")
                
    return validate(eventRef)

#Account number of the Acquirer. First 6 digits is the branch code. --> Field 50k
def get_acq_account(settl):
    acq_account = ''
    if settl:
        if settl.acquirer_account:
            findSpace = settl.acquirer_account.find(' ')
            if findSpace == -1:
                acq_account = '/' + (str)(settl.acquirer_account)
            else:
                acq_account = '/' + (str)(settl.acquirer_account[findSpace+1:])
    
    return validate(acq_account)

#Sender's Correspondent --> Field 53a
def get_sender_corr(settl):
    sender_corr = ''

    if settl:
        if settl.trdnbr:
            if settl.trdnbr.add_info('MM_DEMAT_TRADE') == 'Yes':
                sender_corr = 'SARBZAJ2'
        else:
            #in the case of netted settlements we will use details from the earliest trade in the sequence
            mess = "get_sender_corr: Netted settlement without a trade number - get lowest settlement for " + str(settl.seqnbr)
            ael.log(mess)
            
            settlm = ael.Settlement[get_lowest_settlement(settl, [])[0]]
            if settlm:
                mess = "get_sender_corr: Get MM_DEMAT_TRADE on trade linked to " + str(settlm.seqnbr)
                ael.log(mess)
                
                if settlm.trdnbr:
                    if settlm.trdnbr.add_info('MM_DEMAT_TRADE') == 'Yes':
                        sender_corr = 'SARBZAJ2'
            else:
                ael.log("Error in retrieving lowest settlement")
    
        if sender_corr == '':    
            if int(time.strftime('%H')) >= 15 and int(time.strftime('%M')) >= 30:
                sender_corr = 'SARBZAJ2'
            else:
                sender_corr = 'BKSVZAJJ'
        
        if TESTMESSAGES:
            sender_corr = 'ZYABZAJ0'

    return validate(sender_corr)

#Correspondent Bank's Branch Code. --> Field 57a
def get_corr_branch(settl, localZAR):
    corr_branch = ''
    if settl:
        if settl.party_account != '':
            findSpace = settl.party_account.find(' ')
            if findSpace != -1:
                if localZAR:
                    corr_branch = '//ZA' + settl.party_account[:findSpace]
                else:
                    corr_branch = '//' +  settl.party_account[:findSpace]
    
    return validate(corr_branch)

#Correspondent Account Number. --> Field 58a, 59a
def get_corr_acc(settl):
    corr_acc = ''
    if settl:
        if settl.party_account != '':
            if settl.party_account.__contains__('DIRECT'):
                corr_acc = ''
            else:
                findSpace = settl.party_account.find(' ')
                if findSpace == -1:
                    corr_acc = '/' + (str)(settl.party_account)
                else:
                    corr_acc = '/' + (str)(settl.party_account[findSpace+1:])
                
    return validate(corr_acc)

#Counterparty Full Name. --> Field 58a, 58d, 59a
def get_party_fullname(settl):
    party_fullname = ''
    if settl:
        party_fullname = settl.counterparty_ptynbr.fullname
    
    return validate(party_fullname)

#Additional Information --> Field 70, 72
def __get_adhoc_info(settl):
    adhoc_info = ''
    if settl.trdnbr:
        if settl.acquirer_ptynbr.ptyid in ('Funding Desk', 'Money Market Desk'):
            if settl.trdnbr.insaddr.instype == 'FRN':
                adhoc_info = 'FRN'
            elif settl.trdnbr.insaddr.instype == 'Deposit':
                if settl.trdnbr.insaddr.legs().members() != []:
                    if settl.trdnbr.insaddr.legs()[0].type == 'Call Fixed Adjustable':
                        if settl.trdnbr.quantity == -1:
                            adhoc_info = 'Call Loan'
                        else:
                            adhoc_info = 'Call Deposit'
                    else:
                        adhoc_info = settl.trdnbr.add_info('Funding Instype')
                        if adhoc_info in ('Call Bond Deposit', 'Call Bond Loan', 'Call Deposit Coll DTI', 'Call Deposit Coll NonDTI', 'Call Deposit DTI', 'Call Deposit NonDTI', 'Call I/Div', 'Call I/Div DTI', 'Call I/Div SARB', 'Call Interdesk'):
                            adhoc_info = 'Call Withdrawal'
                        elif adhoc_info in ('Call Loan Coll DTI', 'Call Loan Coll NonDTI', 'Call Loan DTI', 'Call Loan NonDTI'):
                            adhoc_info = 'Loan Advance'
                        elif adhoc_info in ('FDC', 'FDE', 'FDI'):
                            adhoc_info = 'Fixed Deposit Maturity'
                        elif adhoc_info in ('FLI', 'FTL'):
                            adhoc_info = 'Fixed Loan'
                        elif adhoc_info in ('FRN', 'NCC', 'NCD', 'PRN'):
                            adhoc_info = 'Coupon/Capital Payment'
            else:
                adhoc_info = settl.trdnbr.add_info('Funding Instype')
        elif settl.acquirer_ptynbr.ptyid == 'Gold Desk':
            adhoc_info = 'GLD_9923CC_' + str(settl.trdnbr.trdnbr)
        elif settl.acquirer_ptynbr.ptyid == 'Metals Desk':
            adhoc_info = 'MET_0319CC_' + str(settl.trdnbr.trdnbr)
        elif settl.acquirer_ptynbr.ptyid == 'PRIME SERVICES DESK':
            adhoc_info = 'PAYMENT_' + str(settl.trdnbr.trdnbr)
        else:
            if settl.trdnbr.insaddr.instype != 'Option':                            
                adhoc_info = settl.trdnbr.insaddr.instype.upper() + '_' + str(settl.trdnbr.trdnbr)
            else:
                adhoc_info = 'Premium'    
    
    return adhoc_info

def get_adhoc_info(settl):
    adhoc_info = ''
    if settl:
        if settl.acquirer_ptynbr:
            if settl.trdnbr:
                adhoc_info = __get_adhoc_info(settl)
            else:
                #in the case of netted settlements we will use details from the earliest trade in the sequence
                mess = "get_adhoc_info: Netted settlement without a trade number - get lowest settlement for " + str(settl.seqnbr)
                ael.log(mess)
                
                settlm = ael.Settlement[get_lowest_settlement(settl, [])[0]]
                if settlm:
                    mess = "get_adhoc_info: Get adhoc info for trade linked to " + str(settlm.seqnbr)
                    ael.log(mess)
                    
                    adhoc_info = __get_adhoc_info(settlm)
                else:
                    ael.log("Error in retrieving lowest settlement")

    if get_Message_Type(settl) != 'MT103':
        # If the message type is not MT103, add /REC/ according 
        # to Field 72, in case of MT103 leave it out in Field 70
        adhoc_info = '/REC/' + adhoc_info
    
    return validate(adhoc_info)

#Details of Charges from Account --> Field 71
def get_detail_of_charges(settl):
    detail_of_charges = 'OUR'
    '''
    2010-08-18 meeting with business --> charges as a rule of thumb are paid by the initiating bank so hard code
    if settl:
        party = settl.counterparty_ptynbr
        for a in party.accounts():
            if a.name == settl.party_accname:
                detail_of_charges = a.details_of_charges
    '''            
    return validate(detail_of_charges)

def acc_type(accnbr):
    accType = ''
    accType = 'CHQ'
    if re.match('^[0-9]{6}[A-Z,a-z]{3}[0-9]{6}$', accnbr):
        if accnbr[6:9] == 'ZAR':
            accType = 'VOS'
        else:
            accType = 'CFC'
    return accType
    
#Sender to Recieved information --> Field 72

def __get_sender_reciever_info(settl, messageType):
    if settl.trdnbr.add_info('MM_DEMAT_TRADE') == 'Yes':
        sender_reciever_info = '/REC/MPDEM'
    else:
        sender_reciever_info = '/REC/DTBNK'
    return sender_reciever_info
                            
def get_sender_reciever_info(settl, messageType):
    sender_reciever_info = ''
    
    if settl:
        if messageType in ('MT103', 'MT205C103', 'MT202C103'):
            sender_reciever_info = '/REC/DTCUS'
        else:
            if settl.acquirer_ptynbr:
                if (settl.acquirer_ptynbr.ptyid in ('Funding Desk')) or (settl.acquirer_ptynbr.ptyid in ('Money Market Desk') and settl.trdnbr.insaddr.instype not in ('Cap', 'CurrSwap', 'Floor', 'FRA', 'IndexLinkedSwap', 'Swap')):
                    if settl.trdnbr:
                        sender_reciever_info = __get_sender_reciever_info(settl, messageType)
                    else:
                        #in the case of netted settlements we will use details from the earliest trade in the sequence
                        mess = "get_sender_reciever_info: Netted settlement without a trade number - get lowest settlement for " + str(settl.seqnbr)
                        ael.log(mess)
                        
                        settlm = ael.Settlement[get_lowest_settlement(settl, [])[0]]
                        if settlm:
                            mess = "get_sender_reciever_info: Get remittance for trade linked to " + str(settlm.seqnbr)
                            ael.log(mess)
                            
                            sender_reciever_info = __get_sender_reciever_info(settlm, messageType)
                        else:
                            ael.log("Error in retrieving lowest settlement")                 
                            
                else:
                    sender_reciever_info = '/REC/OPDER'

    if SettlementConstants.get_is_internal(settl):
        cptyAcc = settl.party_account
        cptyType = acc_type(cptyAcc)
        if cptyType == 'CFC':
            acqrAcc = SettlementGLAccounts.GL_Acc(settl.curr.insid)
            acqrType = 'NOS'
        else:
            acqrAcc = settl.acquirer_account
            acqrType = acc_type(acqrAcc)
        
        accInfo = '--/ACCOUNTING-INFO'
        if settl.amount <= 0:
             accInfo = accInfo + '--//DR-' + acqrType + '--//CR-' + cptyType
        else:
            accInfo = accInfo + '--//DR-' + cptyType + '--//CR-' + acqrType
        sender_reciever_info = sender_reciever_info + accInfo
        if acc_type(settl.party_account) == 'CFC':
            if settl.amount <= 0:
                sender_reciever_info = sender_reciever_info + '--//DRACC-' + acqrAcc
            else:
                sender_reciever_info = sender_reciever_info + '--//CRACC-' + acqrAcc
            
    return validate(sender_reciever_info)

#Cashbook indicator to prefix the settlement sequence number --> Field 20
def get_cashbook_info(settl):
    cashbook_info = ''
    if settl:
        if settl.acquirer_ptynbr:
            if settl.acquirer_ptynbr.ptyid in ('Funding Desk'):
                cashbook_info = '3301m'
            elif settl.acquirer_ptynbr.ptyid in ('Money Market Desk'):
                if settl.trdnbr.insaddr.instype in ('Cap', 'CurrSwap', 'Floor', 'FRA', 'IndexLinkedSwap', 'Swap'):
                    cashbook_info = 'IRD_'
                else:
                    cashbook_info = '3301m'
            elif settl.acquirer_ptynbr.ptyid in ('EQ Derivatives Desk'):
                cashbook_info = 'EQD_'
            elif settl.acquirer_ptynbr.ptyid in ('IRD DESK', 'LIQUID ASSET DESK', 'REPO DESK', 'FORWARDS DESK', 'Non Linear Deriv', 'Swaps Desk', 'ZZZ DO NOT USE IRP_FX Desk', 'NLD DESK', 'BOND DESK', 'FOREX DESK'): 
                cashbook_info = 'IRD_'
            elif settl.acquirer_ptynbr.ptyid in ('STRUCT NOTES DESK', 'CREDIT DERIVATIVES DESK'): 
                cashbook_info = 'SND_'
            elif settl.acquirer_ptynbr.ptyid in ('Metal Desk'): 
                cashbook_info = 'MET_'
            elif settl.acquirer_ptynbr.ptyid in ('Gold Desk'): 
                cashbook_info = 'GLD_'
            elif settl.acquirer_ptynbr.ptyid in ('PRIME SERVICES DESK'): 
                cashbook_info = 'PRS_'
    
    return validate(cashbook_info)

#Destination address based on the message type.
def get_Destination_Address(settl, message_type):
    destination_address = ''
    if message_type in ('MT103', 'MT205', 'MT205C103', 'MT202C103'):
        destination_address = get_corr_bank_SWIFT(settl)
    elif message_type in ('MT202', 'MT202C202'):
        destination_address = get_our_curr_NOSTRO_SWIFT(settl)
    elif message_type == 'MT205C205':        
        destination_address = get_corr_bank_curr_corr_bank_SWIFT(settl)
    
    return validate(destination_address)

#Determines the message type.
def get_Message_Type(settl):
    return SettlementConstants.get_Message_Type(settl)

#Get the first intermediary SWIFT code
def get_Inter_SWIFT_code(settl, message_type):
    inter_SWIFT_code = ''
    partyObj = settl.counterparty_ptynbr
    for i in range(2, 6):
        field = 'correspondent_bank' + str(i) + '_ptynbr'
        for a in partyObj.accounts():
            if a.name == settl.party_accname:
                inter_Obj = getattr(a, field)
                inter_SWIFT_code = get_SWIFT(inter_Obj)
                if inter_SWIFT_code != '':
                    account = getattr(a, ('account%i' %i))
                    acctNum = ''
                    if account.__contains__('DIRECT'):
                        acctNum = ''
                    else:
                        if account != '':
                            findSpace = account.find(' ')
                            if findSpace == -1:
                                acctNum = '/' + account
                            else:
                                acctNum = '/' +  account[findSpace+1:]                                

                    inter_SWIFT_code = '%s|%s' %(acctNum, inter_SWIFT_code)
                        
                    return inter_SWIFT_code
            
    return inter_SWIFT_code

"""aef-------------------------------------------------------------------------
hook::modify_sender

Hook function **modify_sender** is a part of this module and is used for
changing certain fields in the outgoing AMBA messages.
In order to be called as a modify sender AMBA hook, the name of this
function needs to be stated in the AMBA ini file as an 'ael_sender_modify'.

@category AMBA
@param m:AMB_MESSAGE A message in the AMB format.
@param s:string Subject of the message
@return tuple List that includes the message and the subject.
----------------------------------------------------------------------------"""
def modify_sender(m, s):
 
    result = (m, s)
    type_obj = m.mbf_find_object('TYPE', 'MBFE_BEGINNING')
    type_value = type_obj.mbf_get_value() 
    
    
    if type_value == 'UPDATE_SETTLEMENT':
        result = modify_swift_sender(m, s)
    elif type_value in ['INSERT_INSTRUMENT', 'UPDATE_INSTRUMENT']:
        result = modify_instrument_message(m, s)
    elif type_value in ['INSERT_TRADE', 'UPDATE_TRADE']:
        if trade_message_can_be_skippped(m):    
            return None
    return result


"""aef-------------------------------------------------------------------------
hook::modify_swift_sender

Hook function **modify_swift_sender** is a part of this module and is used for
changing certain fields in the outgoing AMBA settlement messages.
In order to be called as a modify sender AMBA hook, the name of this
function needs to be stated in the AMBA ini file as an 'ael_sender_modify'.

Note that this function should be used if you want to replace non swift characters
with the supported ones (see SPR 270241).

@category AMBA
@param m:AMB_MESSAGE A message in the AMB format.
@param s:string Subject of the message (not used for SWIFT purposes)
@return tuple List that includes the message and the subject.
----------------------------------------------------------------------------"""
def modify_swift_sender(m, s):
    '''The name of this function responds the one stated as
    -ael_sender_modify in the AMBA ini-file.
    Note that if you are using MessageAdaptation hook then
    you need to configure it to run this function. For more
    information see FCA 2105.
    '''

    o1 = m.mbf_find_object('TYPE', 'MBFE_BEGINNING')
    if o1.mbf_get_value() in ['UPDATE_SETTLEMENT']:
        o2 = m.mbf_find_object('!SETTLEMENT', 'MBFE_BEGINNING')
        if not o2:
            o2 = m.mbf_find_object('SETTLEMENT', 'MBFE_BEGINNING')
        if o2:
            o3 = o2.mbf_find_object('STATUS', 'MBFE_BEGINNING')
            o4 = o2.mbf_find_object('!STATUS', 'MBFE_BEGINNING')
            if o3 and o4:
                new_status = o3.mbf_get_value()
                old_status = o4.mbf_get_value()
                if old_status == 'Authorised' and new_status == 'Released':
                    # status changed from authorised to released
                    for field in validate_non_swift_chars:
                        ff = o2.mbf_find_object(field, 'MBFE_BEGINNING')
                        if ff:
                            ret = validate(ff.mbf_get_value())
                            o2.mbf_replace_string(field, ret)

            if o3 and not o4:
                # Make sure to change show_changes in amba ini to 1, if it for SWIFT.
                # released settlement still released, settl is however changed
                # send empty network
                if o3.mbf_get_value() == 'Released':
                    o5 = o2.mbf_find_object('NETWORK', 'MBFE_BEGINNING')
                    if o5:
                        # check on SWIFT migth be done if more then one network
                        o2.mbf_replace_string('NETWORK', '')
                        ael.log("NETWORK emptied, SWIFT message sending prevented")
    return (m, s)

"""----------------------------------------------------------------------------
modify_instrument_message

This function is called by the modify_sender hook.
It modifies instrument AMBA messages by removing cash flows whose pay day are
not within the time window specified in FSettlementVariables.
It also removes cash flows that have additional infos matching the ones
specified in the cash_flow_additional_infos variable (see above).

Also, only messages for instruments listed in valid_instrument_types in 
FSettlementVariables are sent to the AMB.
----------------------------------------------------------------------------"""
def modify_instrument_message(m, s):
    instrument_obj = object_by_name(m, ['', '+', '!'], 'INSTRUMENT')
    if message_can_be_skipped(instrument_obj):
        return        
    for leg_obj in objects_by_name(instrument_obj, ['', '+', '!'], 'LEG'):
        currency_obj = leg_obj.mbf_find_object('CURR.INSID')
        if currency_obj:
            currency = currency_obj.mbf_get_value()
            for cash_flow_obj in objects_by_name(leg_obj, ['', '+'], 'CASHFLOW'):
                if cash_flow_can_be_removed_from_message(cash_flow_obj, currency):
                    leg_obj.mbf_remove_object()
    return (m, s)

"""aef-------------------------------------------------------------------------
hook::modify_swift_receiver

Hook function **modify_swift_receiver** is a part of this module and is used for
filtering of incoming AMBA settlement messages. In order to be called
as a modify receiver AMBA hook the name of this function needs to be stated
in the AMBA ini file as an 'ael_receiver_modify'.

Note that this function will not execute messages sent by other sources
then those that are defined within the variable 'RESOURCES'.

@category AMBA
@param m:AMB_MESSAGE A message in the AMB format.
@return tuple List that includes the message.
----------------------------------------------------------------------------"""
def modify_swift_receiver(m):
    'This function responds the one that is stated as \
    -ael_receiver_modify in the AMBA ini-file. Note that\
    this function will not execute messages sent on some\
    other source then RESOURCES (see defined variables above).\
    Note that if you are using MessageAdaptation hook then\
    you need to configure it to run this function. For more\
    information see FCA 2105.'

    source = ''
    sourceOK = 0

    o1 = m.mbf_find_object('TYPE', 'MBFE_BEGINNING')
    if o1.mbf_get_value() not in ['UPDATE_SETTLEMENT']:
        return (m)
    else:
        s = m.mbf_find_object('SOURCE')
        if s:
            source = s.mbf_get_value()
            if source in RESOURCES:
                sourceOK = 1
        # SWIFT interface is sending updates to AMBA
        # if not proper source then do not proceede
        if sourceOK == 0:
            return


        # Note that AMBA might send no event prefix
        o2 = m.mbf_find_object('!SETTLEMENT', 'MBFE_BEGINNING')
        if not o2:
            o2 = m.mbf_find_object('SETTLEMENT', 'MBFE_BEGINNING')

        if o2:
            o3 = o2.mbf_find_object('SEQNBR', 'MBFE_BEGINNING')
            if o3:
                seqnbr = o3.mbf_get_value()
                if seqnbr:
                    pr = 'Dealing with incoming Settlement %s' % (seqnbr)
                    ael.log(pr)

                    o4 = o2.mbf_find_object('STATUS', 'MBFE_BEGINNING')
                    if o4:
                        status = o4.mbf_get_value()
                        if status:
                            if status in ['Acknowledged', 'Not Acknowledged']:
                                pr = 'SWIFT-interface answered with a  new '\
                                'settlement status %s:\n Commit will be done.' \
                                      % (status)
                                ael.log(pr)
                                send_email(seqnbr, pr)
                                setl = ael.Settlement[int(seqnbr)]
                                ok = 1
                                if not setl:
                                    ok = 0
                                elif setl.status != 'Released':
                                    pr = 'Settlement %d status not Released'\
                                         '(%s)'  % (int(seqnbr), setl.status)
                                    ael.log(pr)
                                    ok = 0

                                if ok:
                                    clone = setl.clone()
                                    clone.status = status
                                    (clone, o2)
                                    clone.commit()
                            else:
                                pr = 'SWIFT-interface answered with wrong '\
                                'status %s. Nothing will be committed to the' \
                                'database.' % (status)
                                ael.log(pr)
                                send_email(seqnbr, pr)
                        else:
                            pr = 'No settlement status in the respond from the'\
                            'SWIFT-interface. Nothing will be committed to the'\
                            'database.' % (status)
                            ael.log(pr)
                            send_email(seqnbr, pr)

    return

def send_email(seqnbr, info):
    'This function send e-mail to predefined receiver.\
    SENDMAIL flag is to be switched on in the beggining of the module.\
    info could be additional information from some line in the code.'

    if SENDMAIL:
        body = 'Settlement '+seqnbr+'\n'+MESSAGE+'\n'+info
        subject = SUBJECT+' '+seqnbr
        ael.sendmail(EMAIL_RECEIVER, subject, body)

def add_diary(clone, amb_msg):
    '''KMaster message includes some fields that are to be placed in the diary.
    New lines need to be taken care of...
    '''
    diary = ''
    o5 = amb_msg.mbf_find_object('SWIFT_EXPLANATION', 'MBFE_BEGINNING')
    if o5:
        d = o5.mbf_get_value()
        diary = r"SWIFT EXPLANATION: %s " % d

    o6 = amb_msg.mbf_find_object('SWIFT_MESSAGE', 'MBFE_BEGINNING')
    if o6:
        d = o6.mbf_get_value()
        d = d.replace('\\r\\n', ' ')
        d = d.replace('\\n', ' ')
        d = d.replace('rn', ' ')
        diary = r"%sSWIFT MESSAGE: %s" % (diary, d)

    if len(diary):
        clone.add_diary_note(diary)


def objects_by_name(parent_obj, name_prefixes, name):
    obj = parent_obj.mbf_first_object()
    names = list()
    for name_prefix in name_prefixes:
        names.append(name_prefix + name)
    while obj:
        if obj.mbf_get_name() in names:
            yield obj
        obj = parent_obj.mbf_next_object()
        
def object_by_name(parent_obj, name_prefixes, name):
    for obj in objects_by_name(parent_obj, name_prefixes, name):
        return obj
    return None

def get_days_forward(currency):
    '''This function is based on days_curr dictionary from above.
    FSettlementParameters.maxiumumDaysForward is used only if cf/settlement
    currency or used account currency is not presented in days_curr! '''
    days_forward = FSettlementParameters.maximumDaysForward
    if days_curr.has_key(currency):
        days_forward = days_curr[currency]
    else:
        used_account_currency = ael.used_acc_curr()
        if days_curr.has_key(used_account_currency):
            days_forward = days_curr[used_account_currency]            
    return days_forward
        
def within_time_window(pay_day, currency):
    days_back = FSettlementParameters.maximumDaysBack
    days_forward = get_days_forward(currency)
    end_day = ael.date_today().add_banking_day(ael.Instrument[currency], days_forward)
    start_day = ael.date_today().add_banking_day(ael.Instrument[currency], (0-days_back))
    return (start_day <= pay_day <= end_day)

def is_remove_cash_flow_add_info(add_info_obj):
    remove = False
    name_obj = add_info_obj.mbf_find_object('ADDINF_SPECNBR.FIELD_NAME', 'MBFE_BEGINNING')
    if name_obj:
        value_obj = add_info_obj.mbf_find_object('VALUE', 'MBFE_BEGINNING')
        if value_obj:
            if (name_obj.mbf_get_value(), value_obj.mbf_get_value()) in cash_flow_additional_infos:
                remove = True
    return remove

def message_can_be_skipped(instrument_obj):
    skip = False
    instrument_type_obj = instrument_obj.mbf_find_object('INSTYPE')
    instrument_type = instrument_type_obj.mbf_get_value()
    if instrument_type not in valid_instrument_types:
        skip = True
    return skip

def isValidPortfolio(amb_message):
    for trade_obj in objects_by_name(amb_message, ['', '+', '!'], 'TRADE'):
        portf_obj = trade_obj.mbf_find_object('PRFNBR')
        
        #If portfolio is not a valid portfolio dskip the message
        if portf_obj:
            portf = portf_obj.mbf_get_value()
            if portf:
                portf_entity = ael.Portfolio[int(portf)]
                for p in VALID_PORTF_FOR_ACQUIRER:
                    if get_Port_Struct_from_Port(portf_entity, str(ael.Portfolio[p].prfid)):
                        return True
        return False

def trade_message_can_be_skippped(amb_message):
    skip = False
    messageType_obj = amb_message.mbf_find_object('TYPE', 'MBFE_BEGINNING')
    if messageType_obj.mbf_get_value() == 'INSERT_TRADE':
        for trade_obj in objects_by_name(amb_message, ['+'], 'TRADE'):
            #Check if CREDIT DERIVATIVES DESK is in a list of Compound Portfolios
            acq_obj = trade_obj.mbf_find_object('ACQUIRER_PTYNBR')
            if acq_obj:
                acqnbr = acq_obj.mbf_get_value()
                if acqnbr and (int(acqnbr) in ACQUIRER_FOR_VALID_PORTF):
                    if not isValidPortfolio(amb_message):
                        skip = True
                        
    for trade_obj in objects_by_name(amb_message, ['', '+', '!'], 'TRADE'):
        #Check for valid instruments
        insaddr_obj = trade_obj.mbf_find_object('INSADDR')
        if insaddr_obj:
           insaddr = insaddr_obj.mbf_get_value()
           if insaddr:           
               instrument = ael.Instrument[int(insaddr)]
               if instrument:           
                   instrument_type = instrument.instype
                   if instrument_type not in valid_instrument_types:
                       skip = True  
    return skip  

def cash_flow_can_be_removed_from_message(cash_flow_obj, currency):
    pay_day_obj = cash_flow_obj.mbf_find_object('PAY_DAY')
    if pay_day_obj:
        pay_day = pay_day_obj.mbf_get_value()
        try:
            cf_date = ael.date(pay_day)
        except Exception, e:
            cf_date = ael.date('1900-01-01')
            cfwnbr_obj = cash_flow_obj.mbf_find_object('CFWNBR')
            cfwnbr = ' No cfwnbr '
            if cfwnbr_obj:
                cfwnbr = cfwnbr_obj.mbf_get_value()
            msg = 'Cashflow paydate is invalid for cashflow : %s with error: %s' %(str(cfwnbr), e.message)
            ael.log(msg)
            
        if within_time_window(cf_date, currency):
            for add_info_obj in objects_by_name(cash_flow_obj, ['', '+'], 'ADDITIONALINFO'):
                if is_remove_cash_flow_add_info(add_info_obj):
                    return True
        else:
            return True
    return False

def check_length(narrative, separator=SEPARATOR,*rest):
    'Swift requires 35*50x characters format. This function\
    adds speratator after every NARRATIVE_LENGTH.'
    r = ''
    if narrative:
        for i in range(0, 60, NARRATIVE_LENGTH):    
            pos = i+NARRATIVE_LENGTH            
            if len(narrative) >= pos:                
                r = r + narrative[i:pos] + separator
            else:                
                r = r + narrative[i:]
    return validate(r)

def get_customer_specific(dict_trans=dict_trans):
    '''Returns customers translation table of non swift characters '''
    customer_specific = ""
    for v in dict_trans.values():        
        customer_specific  = "%s%s" % (customer_specific, v)
    #no validate needed here        
    return customer_specific 


def check_transitions():   
    '''This function checks validity of the customer specific mapping in dict_trans '''
    spec = get_customer_specific()
    for i in spec:
        if i not in SWIFT_OK :
            for k in dict_trans.keys():
                if dict_trans[k] == i and k not in [10, 13]:
                    #10 is "\n" used by Python, 13 is "Carriage Return" might come from other source
                    pr = "%s, = ANSI %d is not supported by the SWIFT. Please adopt dict_trans!" % (i, k)
                    ael.log(pr)
                    break
    l = len(spec)
    if l == 256:
        ael.log('Transition dict includes 256 characters ==> OK')
    else:
        ael.log('Transition dict includes', l, 'characters ==> NOT OK, please adopt dict_trans!')


def validate(str):
    '''Checks the input string and returns string swift validated characters. '''    
    return string.translate(str, swift_trans) 

all_char_256 = string.maketrans('', '')
replace = get_customer_specific()
SWIFT_OK = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789/-?:().,'+ " 
swift_trans = string.maketrans(all_char_256, replace)

# TEST FUNCTIONS
# Please uncomment the row if you want to run it
#print 'These 256 characters will be used:',get_customer_specific()
#check_transitions()                        
#print validate('De"utchland vs Deutchland, \nhow does the 3rd sign look like? ')

"""----------------------------------------------------------------------------
Section from above includes code that used to reside in FSettlement72
----------------------------------------------------------------------------"""


#AR 628331 - AMBA for Settlement Manager fall far behind
def AMBA_PreCache():
    """----------------------------------------------------------------------------
    MODULE
    # AMBA Pre Cache Start
    ----------------------------------------------------------------------------"""

    import ael, time, acm

    ####### get the performance time of the AMBA Bridge ##########
    GlobalCounter = 1

    perfTime = time.clock() 
    def performanceTick():
        global perfTime
        perfTime = time.clock()

    def performanceTock():
        delta = time.clock() - perfTime
        print "AMBA Pre Cache Processed in ", delta, " sec"

    print "Start AMBA Pre-caching..."
    performanceTick()
    LegCntr = 0
    CFWCntr = 0
    ResetCntr = 0

    iDep = acm.FInstrument.Select('insType="Deposit"')
    print 'Deposit Instruments cached:', len(iDep)
    iFRN = acm.FInstrument.Select('insType="FRN"')
    print 'FRN Instruments cached:', len(iFRN)
    #Rectype 13 = cashflow
    
    iInst = []
    for i in iDep:
        iInst.append(i)
    for i in iFRN:
        iInst.append(i)
    print 'All Instruments cached:', len(iInst)
    
    iak = acm.FAdditionalInfoSpec.Select('recType=13')
    print 'FAdditionalInfoSpec for Cashflows cached', len(iak)
    for each in iInst:
        #performanceTick()
        iDepLegs = each.Legs()
        LegCntr = LegCntr + len(iDepLegs)
        for LegCF in iDepLegs:
            if LegCF.LegType() in ['Call Fixed Adjustable', 'Call Fixed', 'Call Float', 'Float', 'Capped Float', 'Floored Float', 'Collared Float', 'Reverse Float', 'Target Redemption', 'Range Accrual', 'Snowball']:
                iLegsCF = LegCF.CashFlows()
                CFWCntr = CFWCntr + len(iLegsCF)
                for CFW in iLegsCF:
                    iAddInfos = CFW.AdditionalInfo()
                    iResets=CFW.Resets()
                    ResetCntr = ResetCntr + len(iResets)
        #performanceTock()
          
    print 'Legs cached:', LegCntr
    print 'Cashflow and AddInfos cached:', CFWCntr
    print 'Resets cached:', ResetCntr
    print 'AMBA Pre-cache done'
    performanceTock()



    """----------------------------------------------------------------------------
    MODULE
    # AMBA Pre Cache End
    ----------------------------------------------------------------------------"""
#AMBA_PreCache()
print "FABSAHook loaded..."
TESTMESSAGES = True
for item in ael.ServerData.select():
    if item.customer_name == 'Production':
        TESTMESSAGES = False
print 'Run using test message BICS =', TESTMESSAGES


#def debug(e):
#    print get_sender_reciever_info(e, 'MT205')
#
#e = ael.Settlement[1480075]
#print get_adhoc_info(e)
