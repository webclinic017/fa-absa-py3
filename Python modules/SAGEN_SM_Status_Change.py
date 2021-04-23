import ael, SAGEN_Set_Additional_Info, time

'''Description
Date            Who             CR Nbr          What
2009-02-09      Heinrich Cronje                 Created

All Settlements with type Security Nominal that is in status Authorised
should change status to Closed.
Thus, the settlements needs to move through the status sycle:

Authorised -> Released -> Acknowledged -> Pending Closure -> Closed.

To be released the Settlements needs to be "Confirmed". Thus, updating the
additional info field Call_Confirmation befor releasing the settlement.
'''

def SAGEN_SM_SecNom(temp,*rest):
    #Selecting all settlements with type Security Nominal
    status = ael.enum_from_string('SettlementStatus', 'Authorised')
    type = ael.enum_from_string('SettlementCashFlowType', 'Security Nominal')
    settlements = '''select
                        settlement.seqnbr
                    from
                        settlement
                    where
                        settlement.type = %d
                    and settlement.status = %d''' % (type, status)
                    
    for sm in ael.dbsql(settlements)[0]:
        for se in sm:
            settle = ael.Settlement[se]
            SAGEN_Set_Additional_Info.main(settle, (str)(settle.seqnbr), 'Call_Confirmation', 'Auto Closed')
            ael.poll()
            time.sleep(2)
            
            s = settle.clone()
            s.status = 'Released'
            try:
                s.commit()
            except:
                print 'Error saving Released: seqnbr = ', s.seqnbr
                break
            ael.poll()
            time.sleep(2)
            
            s = settle.clone()
            s.status = 'Acknowledged'
            try:
                s.commit()
            except:
                print 'Error saving Acknowledged: seqnbr = ', s.seqnbr
                break
            ael.poll()
            time.sleep(2)
            
            s = settle.clone()
            s.status = 'Pending Closure'
            try:
                s.commit()
            except:
                print 'Error saving Pending Closure: seqnbr = ', s.seqnbr
                break
            ael.poll()
            time.sleep(2)
            
            s = settle.clone()
            s.status = 'Closed'
            try:
                s.commit()
            except:
                print 'Error saving Closed: seqnbr = ', s.seqnbr
                
    return 'Done'

