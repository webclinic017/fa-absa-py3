""" Settlement:1.2.2.hotfix23 """

"""----------------------------------------------------------------------------
MODULE
    FSwiftPreview - Module for previewing and validation of Swift messages
    
    (c) Copyright 2004 by Front Capital Systems AB. All rights reserved.

DESCRIPTION
    By running this module AEL variables will be used. In order to use
    a certain settlement either enter seqnbr or choose from the list. 

REFERENCES
    Swift Connectivity Mapping - SCM version 7
NOTE
    This module is NOT SUPPORTED by the Front Capital Systems it is only a
    test tool.
    
USAGE FROM INFORMATION MANAGER

    select  s.seqnbr, 
            s.trdnbr, 
            ael_s(s, 'FSwiftPreview.preview', s.seqnbr) 
    from    settlement s 
    where   s.seqnbr = @SettleID{;settlement.seqnbr} 

----------------------------------------------------------------------------"""

import ael
import FSettlement72, FSettlementAMBAHook

RELEASED_SETL = """
You have picked settlement that is already released,
no AMB message fields will be shown bellow!

This behaviour is due to SPR 263497: 
Update of the released settlement should not result in further Swift message!!!
"""

def preview(x,*rest):
    'Function for previewing of AMBA fields for SWIFT messages'
    
    try:
        if x.record_type and x.record_type == 'Settlement':
            setl = x
        else:
            setl = ael.Settlement[x]
    except:
        setl = ael.Settlement[x]

    if setl:
        print 'Settlement', setl.seqnbr
        c = setl.clone()
        c.status = 'Released'
        fields = FSettlementAMBAHook.add_swift_tag(c, 'Update')

        SENDER_BIC = ''
        RECEIVER_BIC = ''
        PARTY_BIC = ''
        ACCOUNT_WITH_INSTITUTION = ''
        ACCOUNT_WITH_INSTITUTION_BIC = ''
        AMOUNT_ROUNDED = ''
        NETWORK = '' 
        PARTY_TYPE = ''
        VALUE_DAY_SWIFT = ''
        BANK_OPERATION_CODE = ''
        SWIFT_SERVICE_CODE = ''
        SWIFT_MESSAGE_TYPE = None
        if len(fields)==0 or (setl and setl.status == "Released"):
            print RELEASED_SETL
            return RELEASED_SETL
        for i in fields:
            print i
            if i[0]=='SENDER_BIC':
                SENDER_BIC = i[1]
            elif i[0]=='RECEIVER_BIC':
                RECEIVER_BIC = i[1]
            elif i[0]=='PARTY_BIC':
                PARTY_BIC = i[1]
            elif i[0]=='NETWORK':
                NETWORK = i[1]
            elif i[0]=='ACCOUNT_WITH_INSTITUTION':
                ACCOUNT_WITH_INSTITUTION = i[1]
            elif i[0]== 'ACCOUNT_WITH_INSTITUTION_BIC':
                ACCOUNT_WITH_INSTITUTION_BIC = i[1]
            elif i[0]== 'AMOUNT_ROUNDED':
                AMOUNT_ROUNDED = i[1]   
            elif i[0]== 'PARTY_TYPE':
                PARTY_TYPE = i[1]
            elif i[0]== 'SWIFT_LOOPBACK':
                SWIFT_LOOPBACK = i[1]
            elif i[0]== 'VALUE_DAY_SWIFT':
                VALUE_DAY_SWIFT = i[1]
            elif i[0]== 'BANK_OPERATION_CODE':
                BANK_OPERATION_CODE = i[1]
            elif i[0] =='SWIFT_SERVICE_CODE':
                SWIFT_SERVICE_CODE = i[1]
            elif i[0] =='SWIFT_MESSAGE_TYPE':
                SWIFT_MESSAGE_TYPE = i[1]
            #SENDER
    
        CURR = setl.curr.insid      
        print 'Amount', setl.amount, CURR, 'rounded to', AMOUNT_ROUNDED, CURR
        print 'Delivery type:', setl.delivery_type
        print 'Setl cat:', setl.settle_category
        print
        print '\nMessage Generation Simulation\n============================='            
        if SWIFT_SERVICE_CODE.strip() != '':
            print '\nSWIFT Target-II implemented and SWIFT_SERVICE_CODE is', \
                  SWIFT_SERVICE_CODE, '\n'
        NO_SWIFT = 'no SWIFT message will be sent'

        MT202_ok = 1
        MT299_ok = 0
        MT103_ok = 1
        MT199_ok = 0
        self_trading = 0
        validation103_ok = 1
        validation202_ok = 1

        if not (c.type != 'Security Nominal'):
            print 'Settlement type:', c.type, NO_SWIFT
            MT202_ok = 0
            MT103_ok = 0

        if not (c.delivery_type != 'Delivery versus Payment'):
            print 'Delivery type:', c.delivery_type, NO_SWIFT
            MT202_ok = 0
            MT103_ok = 0

        if not((SENDER_BIC != ACCOUNT_WITH_INSTITUTION_BIC) and (c.acquirer_account != ACCOUNT_WITH_INSTITUTION)):

            if not(SENDER_BIC != ACCOUNT_WITH_INSTITUTION_BIC):
                if SENDER_BIC == '':
                    print 'SENDER_BIC and ACCOUNT_WITH_INSTITUTION_BIC are both empty strings'
                else:                
                    print 'SENDER_BIC and ACCOUNT_WITH_INSTITUTION_BIC are equal,', SENDER_BIC, '=', ACCOUNT_WITH_INSTITUTION_BIC
                self_trading = 1

            if not(c.acquirer_account != ACCOUNT_WITH_INSTITUTION):
                print 'setl.acquirer_account and ACCOUNT_WITH_INSTITUTION are equal,', c.acquirer_account, '=', ACCOUNT_WITH_INSTITUTION
                MT202_ok = 0
                MT103_ok = 0
                if self_trading and SWIFT_LOOPBACK == '1':
                    MT202_ok = 1
                    MT103_ok = 1
                    print 'Testing SWIFT_LOOPBACK with selftrading'
                elif self_trading:
                    print 'Selftrading, SWIFT interface (KMaster) will auto acknowledge'

        if (c.settle_category == 'Good Value'):
            MT299_ok = 1        
            MT199_ok = 1

        if not(NETWORK == 'SWIFT'):
            print 'Network is not SWIFT,', NO_SWIFT
            MT202_ok = 0
            MT103_ok = 0

        if NETWORK == '' :
            validation103_ok = 0
            validation202_ok = 0

        if SENDER_BIC == '':
            print 'Empty SENDER_BIC,', NO_SWIFT 
            validation103_ok = 0
            validation202_ok = 0

        if RECEIVER_BIC == '':
            print 'Empty RECEIVER_BIC,', NO_SWIFT 
            validation103_ok = 0
            validation202_ok = 0


        if AMOUNT_ROUNDED == '':
            print 'Empty AMOUNT_ROUNDED,', NO_SWIFT 
            validation103_ok = 0
            validation202_ok = 0

        if PARTY_TYPE == '':
            print 'Empty PARTY_TYPE, this may prohibit logic of KMaster'
            validation103_ok = 0
            validation202_ok = 0

        if VALUE_DAY_SWIFT == '':
            print 'Empty VALUE_DAY_SWIFT,', NO_SWIFT 
            validation103_ok = 0
            validation202_ok = 0

        if SWIFT_MESSAGE_TYPE != '210':

            if not(PARTY_TYPE == 'Counterparty' or (PARTY_TYPE == 'Broker' and PARTY_BIC!='')):
                MT202_ok = 0
                print 'PARTY_TYPE is not Counterparty nor broker with Nonempty PARTY_BIC, no MT 202 will be generated'

            if not(PARTY_TYPE == 'Client' or (PARTY_TYPE == 'Broker' and PARTY_BIC=='')):
                MT103_ok = 0
                print 'PARTY_TYPE is not Client nor broker with empty PARTY_BIC, no MT 103 will be generated'

            if ACCOUNT_WITH_INSTITUTION == '':
                print 'Empty ACCOUNT_WITH_INSTITUTION (only warning)'

            if ACCOUNT_WITH_INSTITUTION_BIC == '':
                print 'Empty ACCOUNT_WITH_INSTITUTION_BIC (only warning)'

            if BANK_OPERATION_CODE == '':
                print 'Empty BANK_OPERATION_CODE,', NO_SWIFT
                validation103_ok = 0

            if PARTY_BIC == '':
                print 'Empty PARTY_BIC, no MT 202 will be generated'
                validation202_ok = 0

            if not(c.amount < 0):
                print 'Positive amount, no MT 103 or MT 202 will be generated'
                MT202_ok = 0
                MT103_ok = 0
        if MT103_ok and validation103_ok:   
            print '\nIf settlement is released, MT 103 will be generated'
            if MT199_ok:    
                print 'If settlement is released, MT 199 will be generated (Pay', setl.settle_category, ')'            
        elif not MT103_ok:
            print '\nValidation errors (business logic) prohibit MT 103' 
        else:
            print '\nValidation errors (missing data) prohibit MT 103'

        if MT202_ok and validation202_ok:
            # 4208 was wrong client
            print '\nIf settlement is released, MT 202 will be generated'
            if MT299_ok:    
                print 'If settlement is released, MT 299 will be generated (Pay', setl.settle_category, ')'            
        elif not MT202_ok:
            print 'Validation errors (business logic) prohibit MT 202'
        else:
            print 'Validation errors (missing data) prohibit MT 202'

        if SWIFT_MESSAGE_TYPE:
            if SWIFT_MESSAGE_TYPE == '210':
                print '\nIf settlement is released, MT 210 will be generated'
        elif SWIFT_MESSAGE_TYPE != '210':
           print 'Validation errors (business logic) prohibit MT 210'

    else:
        print 'choose some other settlement'
        ael.log('choose some other settlement')

    return 'Message preview done'


def settlements():
    'Returns Authorised settlements. Used for population of the\
    ael_variables menu'
    
    setls = []
    for setl in ael.Settlement.select():
        if setl.status in ['Authorised']:
            setls.append(str(setl.seqnbr))

    if len(setls):
        setls.sort()

    return setls

  
try:
    if __name__ == "__main__":
        import sys, getopt

    ael_variables = [('settlement', 'Settlement to Preview', 'int', settlements(), '', 1, 0)]

    def ael_main(dictionary):
        print '\nFSwiftPreview:\n=============='
        s = dictionary.get('settlement')
        preview(s)

except Exception, e:
    if globals().has_key('ael_variables'):
        del globals()['ael_variables']
    if globals().has_key('ael_main'):
        del globals()['ael_main']
    print 'Could not run FSwiftPreview due to '
    print e


