""" Settlement:1.2.2.hotfix26 """

"""----------------------------------------------------------------------------
MODULE
    FSettlementClientSTPTemplate - Module which includes STP rules defiend
    by the user/customer.
    
    (c) Copyright 2003 by Front Capital Systems AB. All rights reserved.

DESCRIPTION
    Client STP processing is done after ordinary STP.
    
RENAME this module to FSettlementClientSTP since this file is only template.

----------------------------------------------------------------------------"""

"""----------------------------------------------------------------------------
FUNCTION
    client1() - Client defined STP function. 

DESCRIPTION
    This function should be implemented to test client specific issues. Add 
    the tests that should be performed on the applied settlement record. 
    
ARGUMENTS
    settle   Cloned settlement object      
----------------------------------------------------------------------------"""
def client1(settle):
    ok=1
    #*************** STP Rules on Acquirer = Funding Desk ***************
    if settle.trdnbr:
        if settle.trdnbr.acquirer_ptynbr:
            if settle.trdnbr.acquirer_ptynbr.ptynbr == 2247:    #Funding Desk
                #********** Only Deposit Settlements are settled **********
                if settle.trdnbr.insaddr.instype not in ('Deposit', 'CD', 'FRN'):
                    settle.text = 'Not Valid Instrument'
                    settle.status = 'Hold'
                    settle.commit()
                    ok = 0
                    return ok
                #********** CP = Funding Desk are not settled **********
                if settle.trdnbr.counterparty_ptynbr.ptynbr == 2247:    #Funding Desk
                    settle.text = 'Not Valid Counterparty'
                    settle.status = 'Hold'
                    settle.commit()
                    ok = 0
                    return ok
    return ok

"""----------------------------------------------------------------------------
FUNCTION
    client2() - Client defined STP function. 

DESCRIPTION
    This function should be implemented to test client specific issues. Add 
    the tests that should be performed on the applied settlement record. 
    
ARGUMENTS
    settle   Cloned settlement object      
----------------------------------------------------------------------------"""    
def client2(settle):
    ok = 1
    #*************** STP Rules on Acquirer = EQ Derivatives Desk ***************
    if settle.trdnbr:
        if settle.trdnbr.acquirer_ptynbr:
            if settle.trdnbr.acquirer_ptynbr.ptynbr == 9710:    #EQ Derivatives Desk
                #********** No Call Accounts on EQ Derivatives Desk are settled **********
                if settle.trdnbr.insaddr.instype == 'Deposit':
                    if settle.trdnbr.insaddr.legs().members() != []:
                        for l in settle.trdnbr.insaddr.legs():
                            if l.type == 'Call Fixed Adjustable':
                                settle.text = 'Not Valid Instrument'
                                settle.status = 'Hold'
                                settle.commit()
                                ok = 0
                                return ok
                #********** CP = EQ Derivatives Desk, NLD DESK, Non Linear Deriv are not settled **********
                if settle.trdnbr.counterparty_ptynbr.ptynbr in (9710, 30311, 102):        #EQ Derivatives Desk, NLD DESK, Non Linear Deriv
                    settle.text = 'Not Valid Counterparty'
                    settle.status = 'Hold'
                    settle.commit()
                    ok = 0
                    return ok
    return ok

"""----------------------------------------------------------------------------
FUNCTION
    client3() - Client defined STP function. 

DESCRIPTION
    This function should be implemented to test client specific issues. Add 
    the tests that should be performed on the applied settlement record. 
    
ARGUMENTS
    settle   Cloned settlement object      
----------------------------------------------------------------------------"""
def client3(settle):
    ok=1
    #*************** Additional STP Rules on Acquirer = Funding Desk ***************
    if settle.trdnbr:
        if settle.trdnbr.acquirer_ptynbr.ptynbr == 2247:
            if settle.trdnbr.insaddr.legs()[0].type != 'Call Fixed Adjustable':
                if settle.cfwnbr:
                    if settle.cfwnbr.type == 'Fixed Amount':
                        if settle.trdnbr.add_info('MM_Account_Ceded') == 'Yes':
                            settle.text = 'Ceeded Account'
                            settle.status = 'Hold'
                            settle.commit()
                            ok = 0
                            return ok
    return ok
    
"""----------------------------------------------------------------------------
Main
----------------------------------------------------------------------------"""
import ael, FSettlementGeneral

"""aef-------------------------------------------------------------------------
hook.FSettlementClientSTP::clientSTP

The **clientSTP** function and the **FSettlementClientSTP** module are a part of Settlement script package - and support executing Client defined STP rules. These rules are always called after standard STP rules (that are fixed and can not be changed).

As a result of Client STP a settlement gets status 'Authorised' meaning that all checks are fulfilled, otherwise the status becomes 'Manual Match' meaning that additional
changes needs to be made (then the Settlement will be authorised).

In order to create custom Client STP rules the customer needs to:

1. Rename **FSettlementClientSTPTemplate** to **FSettlementClientSTP**. 

2. Add custom STP functions (client1 and client2 are in place by default).

3. Accommodate the client STP function to use additional functions such as client3.

Note that the ARENA Task Server real time process that executes **FSettlementAMB** needs to be restarted
every time this file is edited.

@category PRIME.Settlement
@param settle:Settlement A Settlement entity (already cloned) to apply client stp on.
@return None The function itself does not return anything, but the settlement 
gets saved afterwards.
@example
def client3(settle):
    # an example of client stp function (called by clientSTP(settle))
    # clientSTP function needs to be extended to use client3(settle)
    ok=1
    if settle.trdnbr == 4711:
        ok = 0
    return ok
----------------------------------------------------------------------------"""
def clientSTP(settle):
    if settle:
        if settle.record_type == 'Settlement':
            log_str = 'Running client STP on Settlement %d' % (settle.seqnbr)
            log(1, log_str)
            ok = 1            
            clone = settle.clone()
            
            if settle.trdnbr:
                if settle.trdnbr.acquirer_ptynbr:
                    if settle.trdnbr.acquirer_ptynbr.ptynbr == 2247:   #Funding Desk
                        if not client1(clone):
                            ok = 0
                        else:
                            if not client3(clone):
                                ok = 0
                    if settle.trdnbr.acquirer_ptynbr.ptynbr == 9710:   #EQ Derivatives Desk
                        if not client2(clone):
                            ok = 0
                            
            #when addiditonal client rules are added (i.e. clientx) adapt following code
            #if not clientx(clone):
            #    ok = 0
            
            FSettlementGeneral.clear_status_explanation(clone)            
            if ok:        
                clone.status = 'Authorised'
                clone.commit()      
                log(1, 'client STP: After authorised commit')            
            #else:
            #    clone.status = 'Manual Match'
            #    clone.commit()
            #    log(1,'client STP: After manual match commit')
    else:
        log(1, 'client STP: no settlement as input!')
    return

def log(level, s):
    return FSettlementGeneral.log(level, s)

