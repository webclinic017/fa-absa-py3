""" Settlement:1.2.2.hotfix23 """

"""----------------------------------------------------------------------------
MODULE
    FSettlement72 - Module used for population of certain SWIFT fields
    
    (c) Copyright 2004 by Front Capital Systems AB. All rights reserved.

DESCRIPTION    
    Function descr that is available in this module could be called from
    other sources or interfaces.

DATA-PREP
    Note that this file includes variables that are not available
    in FSettlementVariablesTemplate so you need to save these before upgrading
    to future versions of this file.

    Before starting AMBA verify that all variables are correct because
    FSettlementAMBAHook is using this module and vice versa. Note that if
    any further changes are done in this module running AMBA needs to be
    restarted in order to reload the hook.

REFERENCES
    Swift Connectivity Mapping - SCM version 7
----------------------------------------------------------------------------"""
import ael, string
import FSettlementAMBAHook

# Rounding per currency for SWIFT outgoing messages
# see field AMOUNT_ROUNDED in FSettlementAMBAHook
# see also function round_amount(setl)
# note that JPY is truncated i.e. 3.22 JPY becomes 3 JPY (no rounding)
round_per_curr={'EUR':2,'USD':2,'JPY':0,'KRW':0,'TRL':0,'KWD':3,\
                'AED':2,'ARS':2,'AUD':2,'BAM':2,'BRL':2,'BGL':2,\
                'CAD':2,'CNY':2,'CYP':2,'CZK':2,'DKK':2,'GBP':2,\
                'EKK':2,'HKD':2,'HRK':2,'HUF':2,'ISK':2,'INR':2,\
                'IDR':2,'LVL':2,'MYR':2,'MXN':2,'MXV':2,'NZD':2,\
                'NOK':2,'PHP':2,'SAR':2,'SGD':2,'SKK':2,'SIT':2,\
                'ZAR':2,'SEK':2,'CHF':2,'TWD':2,'THB':2,'YUM':2}

# Default text phrases for narrative fields of MT messages
NARRATIVE_199 = 'Paying Good Value for settlement '
NARRATIVE_299 = 'Text that is part of MT299'
OLD_AMOUNT = 'Old amount:'
OLDVALUDAY = 'Old value day:'


# max length of the line is 50 according to the SWIFT requirement
# default NARRATIVE_LENGTH = 50
NARRATIVE_LENGTH = 50

# Identifies type of operation
# Default value of MT103 field 23B
BANK_OPERATION_CODE = 'CRED'

# Default value of MT103 field 71A
# Note that this value overrides info available in account.details_of_charges
DETAILS_OF_CHARGES = 'SHA'

# Default value of MT103 field 23E
INSTRUCTION_CODE = 'PHOB'

# Used in cp_fullname function
# If true (FULLNAME = 1) fullname is used otherwise ptyid
FULLNAME = 1

# Following naming conventions are used in function type_to_nice_name
FIXED_AMOUNT = 'Fixed Amount'
PREMIUM = 'Premium'
FIXED_RATE = 'Fixed Rate'
INSERT = 'Insert'

# Sign used as delimitor before sending to swift
# Note that this sign should not be at the end
# remove_last_separator takes care of last char (see LAST_CHAR_CHECK)
SEPARATOR = FSettlementAMBAHook.FIELD72_SEPARATOR

# If toggled (LAST_CHAR_CHECK = 1) check will be done
# on fields before sending to swift
# the result is that separator on the end will be removed
LAST_CHAR_CHECK = 1

# Shows if Field 53a should use option A (or B)
# see function get_senders_correspondent where it is used 
FIELD53_OPTION = 'A'

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

# See also TEST FUNCTIONS bellow
    
def descr(e,newline=SEPARATOR,*rest):
    'This function populates Swift field 72 Sender to Receiver information.\
    It is up to those who call this function to check that every line is \
    maximum characters long. Separator can be deployed (newline). Check of\
    netted settlement is done. In the case of netted settlement the settlement\
    connected to the least trade number is used as so called child settlement.'
    
    ret = ''
    YOUR_REF = 'Our Reference: '
    OUR_REF = 'Your Reference: '    
    
    if e.record_type == 'Settlement':
        network = FSettlementAMBAHook.get_networktype(e)
        client_type = cp_type(e)        
        child_setl = e
        
        # settlement might be netted
        if FSettlementAMBAHook.is_net(e):
            # setlement that is part of netting, has least trdnbr
            child_setl = FSettlementAMBAHook.least_net_trdnbr(e, 2)
            # just to be sure not to have None value
            if child_setl == None:
                child_setl = e
                ael.log('FSettlement72.descr: least trdnbr not found info based on %d' % (e.seqnbr))

        if network == 'CUSTODIAN' or \
        (network == 'SWIFT' and client_type == 'Client'):

            fullname = cp_fullname(e, FULLNAME)
            if fullname != '':                
                ret = fullname + newline

            type = type_to_nice_name(e)
            proddescr = get_productdescr(child_setl)
            if type != '' and proddescr != '':            
                ret = ret + type + ' ' + proddescr +newline
            elif type == '':
                ret = ret + proddescr + newline
            elif proddescr == '':                
                ret = ret + type + newline

            ret = ret + YOUR_REF + ':' + get_trdnbr(child_setl)+ newline

            yf = get_your_ref(child_setl)        
            if yf != '':
                ret = ret + OUR_REF + yf + newline 
                
        elif network in FSettlementAMBAHook.RESOURCES and client_type != 'Client':
            accounting = ''
            # counterparty account
            acc = FSettlementAMBAHook.get_account(child_setl, 1)

            if acc:                
                accounting = acc.accounting
                if accounting != '':
                    ret = accounting + newline

    # 6*35x
    ret = remove_last_separator(ret, LAST_CHAR_CHECK)    
    return validate(ret)


def add_info(e,spec,*rest):
    'Takes a settlement or trade as input and returns additional info.'
    ret = ''
    tr = None
    
    if e:    
        if e.record_type == 'Settlement':
            tr = e.trdnbr            
        elif e.record_type == 'Trade':
            tr = e            
    if tr:
        try:            
            ret = str(tr.add_info(spec))
        except:
            pr = ''
            if spec:            
                pr = '%s, no such additional info' % (spec) 
            ael.log(pr)
            
    return validate(ret)

def cp_address(setl,*rest):
    'Counterparty address, suitable for parties without BIC'
    ret = ''
    if setl:
        cp = ael.Party[setl.party_ptyid]
        if cp:  
            ret = cp.address+' '
            if cp.address2 != '' and cp.address != cp.address2:
                ret = ret + cp.address2
            ret = ret + cp.city + ' ' + cp.country
    
    return validate(ret)

def cp_fullname(setl, mode=1,*rest):
    'Full name of the counterparty if mode is 1,\
    otherwise ptyid will be returned'
    ret = ''
    if setl:
        #MT 103 Field 59 PARTY_NAME
        cp = ael.Party[setl.party_ptyid]
        if cp:
            if mode:
                ret = cp.fullname
            else:
                ret = cp.ptyid
    
    return validate(ret)
def acq_address(setl,*rest):
    'Acquirer address, suitable for parties without BIC'
    ret = ''
    if setl:
        acq = ael.Party[setl.acquirer_ptyid]
        if acq:  
            ret = acq.address+' '
            if acq.address2 != '' and acq.address != acq.address2:
                ret = ret + acq.address2
            ret = ret + acq.city + ' ' + acq.country
    
    return validate(ret)

def acq_fullname(setl, mode=1,*rest):
    'Full name of the aquirer if mode is 1,\
    otherwise ptyid will be returned'
    ret = ''
    if setl:
        acq = ael.Party[setl.acquirer_ptyid]
        if acq:
            if mode:
                ret = acq.fullname
            else:
                ret = acq.ptyid
    
    return validate(ret)
        

def cp_type(setl,*rest):
    'Type of the counterparty'
    ret = ''
    if setl:
        cp = ael.Party[setl.party_ptyid]
        if cp:  
            ret = cp.type
    
    return validate(ret)
            
def get_productdescr(setl,*rest):   
    'Product description via choice list'
    descr = ''
    tr = None
    if setl:
        if setl.record_type == 'Settlement':
            if setl.trdnbr:
                tr = setl.trdnbr

        if tr == None and setl.record_type == 'Trade':
            tr = setl
            if tr.optkey2_chlnbr:
                descr = str(tr.optkey2_chlnbr.seqnbr)

    if tr == None:
        ael.log('get_productdescr: the input is empty')
                                      
    return validate(descr)


def get_trdnbr(setl,*rest):
    'Returns the tradenumber of the settlement as a string'
    ret = ''
    tr = None
    if setl:
        tr = setl.trdnbr
        if tr:
            ret = str(tr.trdnbr)

    return validate(ret)


def get_your_ref(e, *rest):
    'Returns the value of the your_ref field on trade level.'
    your_ref = 'NONREF'
    tr = None
    
    if e:    
        if e.record_type == 'Settlement':                    
            if e.trdnbr:
                tr = e.trdnbr
            elif FSettlementAMBAHook.is_net(e):
                #settlement is not connected to the trade
                #can be netted or for some other reason ...    
                tr = FSettlementAMBAHook.least_net_trdnbr(e, 1)   
        elif e.record_type == 'Trade':
            tr = e

    if tr:
        if tr.your_ref != '':
            your_ref = tr.your_ref            
            if len(your_ref) > 16:
                ael.log('your_ref length is longer then 16 char')
                pr = 'See trade %d and adapt your_ref (CP ref)' % (tr.trdnbr)
                ael.log(pr)
                your_ref = your_ref[:16]
                ael.log('your_ref sent to SWIFT is 16 char long')
    
    return validate(your_ref)


def type_to_nice_name(setl,*rest):
    'Naming conventions, customer specific'
    ret = INSERT
    if setl:
        if setl.type == 'Premium':
            ret = PREMIUM
        elif setl.type == 'Fixed Amount':
            ret = FIXED_AMOUNT
        elif setl.type == 'Fixed Rate':
            ret = FIXED_RATE

    return validate(ret)

def get_bank_operation_code(setl,*rest):
    'BANK_OPERATION_CODE MT103 field 23B'
    boc = BANK_OPERATION_CODE    
    return validate(boc)
    
def get_remittance_info(setl, separator=SEPARATOR, *rest):
    'REMITTANCE_INFO includes details of the individual transaction'
    YOUR_REF = 'Your reference:'
    OUR_REF = 'Our reference:'
    ret = ''    
    if setl:
        if setl.trdnbr:
            # line 1
            ret = 'Instrument:'+setl.trdnbr.insaddr.insid + separator
            ret = ret + YOUR_REF + get_trdnbr(setl) + separator
            ret = ret + OUR_REF + get_your_ref(setl) + separator

    ret = remove_last_separator(ret)            
    return validate(ret)

def descr72_202(setl,newline=SEPARATOR,*rest):
    'Just calls the function descr.'
    #ret = remove_last_separator(ret)    
    return validate(descr(setl, SEPARATOR))

def descr72_103(setl,newline=SEPARATOR,*rest):
    'Here the customer can create own rules for\
    field 72 on message 103.'

    # untill new rules are implemented old descr funtion
    # is called
    # to restrict this field use DROP_FIELDS functionality
    #ret = remove_last_separator(ret)    
    return descr(setl, SEPARATOR)

def descr70_103(setl,newline=SEPARATOR,*rest):
    'Calls a function that populates field 70 of MT103'
    return validate(get_remittance_info(setl, SEPARATOR))

def get_details_of_charges(setl,*rest):
    ''' '''
    ret = DETAILS_OF_CHARGES
    if setl:
        acc = FSettlementAMBAHook.get_account(setl, 1)
        if acc:            
            ret = acc.details_of_charges
    return validate(ret)

def get_instruction_code(setl,*rest):
    '''INSTRUCTION_CODE'''
    ret = INSTRUCTION_CODE
    return validate(ret)

def get_narrative199(setl,mode=0,separator=SEPARATOR,*rest):
    'Takes a settlement. Mode 1 means that info about the\
    settlement shell be appended. Separator can be used for newline.\
    See header of this module where variables such \
    as OLD_AMOUNT are configurable.'

    ret = NARRATIVE_199
    vd = ''
    old_amount = ''

    if mode:
        #79    
        if setl.settle_seqnbr and setl.settle_category == 'Good Value':
            ret = ret + ' ' + str(setl.seqnbr) + '. '
            if setl.settle_seqnbr.value_day:
                vd = setl.settle_seqnbr.value_day.to_string('%Y-%m-%d')
                if vd != '':
                    ret = ret + OLDVALUDAY + vd + ' '
            if setl.settle_seqnbr.amount:
                #old_amount = str(setl.settle_seqnbr.amount)
                old_amount = round_amount(setl.settle_seqnbr)                
                if old_amount != '':
                    ret = ret + OLD_AMOUNT + old_amount + ' '+ setl.settle_seqnbr.curr.insid                    

    ret = check_length(ret, separator=SEPARATOR)
    #ret = remove_last_separator(ret)    
    return validate(ret)

def get_narrative299(setl,mode=0,separator=SEPARATOR,*rest):
    'Takes a settlement. Mode 1 means that some info about\
    settlement shell be appended. Separator can be used for newline.'
    ret = NARRATIVE_299
    if mode:
        ret = ret + ' ' + str(setl.seqnbr)
        #ROUND AMOUNT
    ret = check_length(ret, separator=SEPARATOR)    
    #ret = ret + separator
    #ret = remove_last_separator(ret)
    return validate(ret)

def remove_last_separator(str,mode=LAST_CHAR_CHECK,*rest):
    ''
    ret = str
    if mode:
        if len(str)>1:
            if str[len(str)-1] in [SEPARATOR, '|']:
                #all but last character to be presented
                ret = str[:-1]
    #no validate needed here
    return ret

def round_amount(setl,*rest):
    'Round decimal amount according to currency stated\
    in round_per_cur. Note that JPY is truncated.'
    ret = '0'
    if setl:
        ret = str(setl.amount)
        curr = setl.curr.insid
        if round_per_curr.has_key(curr):
            if curr != 'JPY':
                ret = str(round(setl.amount, round_per_curr[curr]))          
            elif curr == 'JPY':                
                # truncate jpy before decimal sign
                jen = str(setl.amount)
                pos = jen.find('.')    
                ret = str(setl.amount)
                if pos > -1:
                    ret = jen[:pos]
                else:
                    ael.log('decimal sign not found')
        else:
            pr = 'round_per_curr does not include rounding value for %s' % (setl.curr.insid)
            ael.log(pr)
            pr = 'please review the round_per_curr list in FSettlement72'
            ael.log(pr)
    
    return validate(ret)

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

def get_senders_correspondent(setl, option=FIELD53_OPTION, *rest):
    'Field 53a of MT 103 and MT 202 is Senders correspondent.\
    Option A conciders BIC while Option B conciders Location.\
    Customer can modify this function to support wanted Option.'

    ret = ''
    if setl:
        if option == 'A':
            acc = FSettlementAMBAHook.get_account(setl, 0)            
            if acc and acc.bic_seqnbr:                        
                ret = acc.bic_seqnbr.alias                            
        elif option == 'B':
            ret = get_location(setl, 0)
                    
    return validate(ret)

    
def get_location(setl,mode=0,*rest):
    'Returns location of acquirer (if mode=0) otherwise \
    counterparty location (city).'
    
    location = ''
    pty = None    

    if mode == 0:        
        pty = ael.Party[setl.acquirer_ptyid]
    else:                
        pty = ael.Party[setl.party_ptyid]
    
    if pty:
        location = pty.city

    return validate(location)

def drop_override(setl, inList):
    '''Function where the customer can add rules for dropping fields.
    Returns a list that includes message fields to be dropped.
    This function is called from FSettlementAMBAHook.'''

    dropList = []

    for n in inList:        
        dropList.append(n)
        
    #if setl.curr.insid != 'EUR' and '53' not in dropList:
    #    dropList.append('53')        
        
    #no validate needed here, list returned
    return dropList


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
    '''Checks the input string and returns string swift validated characters.
    Call this function from FSettlementAMBAHook and FSettlement72.'''    
    return string.translate(str, swift_trans) 

all_char_256 = string.maketrans('', '')
replace = get_customer_specific()
SWIFT_OK = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789/-?:().,'+ " 
swift_trans = string.maketrans(all_char_256, replace)

# TEST FUNCTIONS
# Please uncomment the row if you want to run it
#print 'These 256 characters will be used:',get_customer_specific()
#check_transitions()                        
#print validate('De tchland vs Deutchland, \nhow does the 3rd sign look like? ')



