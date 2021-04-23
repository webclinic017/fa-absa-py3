import ael, Call_Rolling_Interest
from FBDPCommon import *
from SAGEN_IT_Functions import *
from SettlementConstants  import *

'''
Date                    : ?????, 2010-10-27
Purpose                 : Test if portfolio that is linked to the settlement (normal or netted) rolls up to the GRAVEYARD portfolio. If so, we do not settle.
                          Amended script to use continues instead of breaks which was causing the script to exit without completing.
Department and Desk     : Ops Money Market Settlements
Requester:              : Martie Waite
Developer               : Heinrich Cronje/Anwar Banoo/Bhavnisha Sarawan, Anwar Banoo
CR Number               : ?????, 476845

23/05/2018      Elaine Visagie  Bhavnisha Sarawan       Rollback, excluding counterparties, changed filter to only include BO and BO BO Confirmed trades, added print statements for pseudo dry run

'''

cpty_exclusion_list = []
    
def Payment(temp,*rest):
    #use ACM so that we can get the smallest set of settlements back to work with
    query = acm.CreateFASQLQuery("FSettlement", "AND")
    query.AddAttrNode("Status", "EQUAL", "Authorised")
    query.AddAttrNode("Type", "NOT_EQUAL", "Stand Alone Payment")
    query.AddAttrNode("Amount", "LESS", -1)
    query.AddAttrNode("ValueDay", "EQUAL", acm.Time().DateToday())
    query.AddAttrNode("Acquirer.Oid", "EQUAL", FUNDING_DESK)
    for cpty in cpty_exclusion_list:
        query.AddAttrNode("Counterparty.Name", "NOT_EQUAL", cpty)
    qor = query.AddOpNode('OR')
    qor.AddAttrNode("Trade.Status", "EQUAL", "BO Confirmed")
    qor.AddAttrNode("Trade.Status", "EQUAL", "BO-BO Confirmed")
    settlements = query.Select()    
    today = ael.date_today()
    ins_zar = ael.Instrument['ZAR']
    yesterday = today.add_banking_day(ins_zar, -1)
    valid_port = []    
    ael.log('Settlements to process:' + str(settlements))
    for s in settlements:
        settle = ael.Settlement[s.Oid()]
        ael.log("Settlement in scope, " + str(settle.seqnbr) + ',' + settle.trdnbr.status + ',' + str(settle.trdnbr.trdnbr) + ',' + settle.type + ',' + str(settle.value_day))
        print "Settlement in scope, ", settle.seqnbr, ',', settle.trdnbr.status, ',', settle.trdnbr.trdnbr, ',', settle.type, ',', settle.value_day
        matchPort = 0
        if settle.trdnbr:
            trade = settle.trdnbr
            fun_instype = trade.add_info('Funding Instype')
            
            #Funding instypes that do not need the settle
            '''if fun_instype in ('NCC','NCD','CD','CL','PRN','FRN','RDL'):
                clone = settle.clone()
                clone.status = 'Hold'
                clone.commit()
                continue
            '''
            trd_port = trade.prfnbr.prfid
            if trd_port not in valid_port:
                if not get_Port_Struct_from_Port(trade.prfnbr, 'GRAVEYARD'):
                    valid_port.append(trd_port)
                    matchPort = 1
            else:
                matchPort = 1                
                
            if trade.insaddr.legs().members():
                if matchPort:
                    leg0 = trade.insaddr.legs()[0]
                    #Payment of fixed amounts on annuities or Payment of interest
                    if fun_instype=='FDI'\
                       and settle.value_day<leg0.end_day\
                       and settle.value_day>leg0.start_day\
                       and settle.type in ('Fixed Amount', 'Fixed Rate')\
                       and leg0.amort_type=='Annuity':
                        ael.log("Releasing Annuity| " + str(settle.seqnbr) + '|' + settle.trdnbr.status + '|' + settle.party_ptyid)
                        print "Releasing Annuity, ", settle.seqnbr, ',', settle.trdnbr.status, ',', settle.party_ptyid
                        clone = settle.clone()
                        clone.status = 'Released'
                        clone.commit()
                        continue
                    if leg0.type == 'Call Fixed Adjustable':
                        ael.log('Call_Rolling_Interest: ' + str(Call_Rolling_Interest.Call_Rolling_Interest2(settle.cfwnbr, today, today)=='in'))
                        print 'Call_Rolling_Interest: ', Call_Rolling_Interest.Call_Rolling_Interest2(settle.cfwnbr, today, today)=='in'
                    #Call Automated Payments
                    if leg0.type == 'Call Fixed Adjustable'\
                       and leg0.reinvest == 0\
                       and (fun_instype[0:4] == 'Call' or fun_instype[0:19] == 'Access Deposit Note')\
                       and (settle.type in ('Call Fixed Rate Adjustable', 'Fixed Rate Adjustable'))\
                       and leg0.rolling_base_day <= today\
                       and Call_Rolling_Interest.Call_Rolling_Interest2(settle.cfwnbr, today, today)=='in'\
                       and ((settle.type=='Call Fixed Rate Adjustable' and yesterday>=settle.cfwnbr.start_day and yesterday<settle.cfwnbr.end_day) or 
                            (settle.type=='Call Fixed Rate Adjustable' and settle.cfwnbr.end_day.adjust_to_banking_day(ins_zar, 'Following')!=settle.cfwnbr.pay_day and settle.cfwnbr.pay_day==today) or 
                             settle.type=='Fixed Rate Adjustable'):
                        
                        #switch back to the acm object mode so that we get the account directly instead of iterating through the list of accounts
                        account = acm.FAccount.Select01("name = '%s' and party = '%s'" %(settle.party_accname, settle.counterparty_ptynbr.ptyid), '')
                        if account.Bic():
                            if account.Bic().Type().Name() == 'SWIFT':
                                set_AdditionalInfoValue(settle, settle.seqnbr, 'Call_Confirmation', 'Auto Int Payment')                            
                                ael.poll()
                                if settle.add_info('Call_Confirmation') != '':
                                    ael.log("Releasing Call Account Interest| " + str(settle.seqnbr) + '|' + settle.type + '|' + settle.party_ptyid + '|' + str(settle.cfwnbr.start_day) + '|' + str(settle.cfwnbr.end_day))
                                    print "Releasing Call Account Interest, ", settle.seqnbr, ',', settle.type, ',', settle.party_ptyid, ',', settle.cfwnbr.start_day, ',', settle.cfwnbr.end_day
                                    clone = settle.clone()
                                    clone.status = 'Released'
                                    clone.commit()
                                else:
                                    ael.log('Add info not added to : ' + str(settle.seqnbr) + ' - settlement will not be released')
                                    
                                continue
                                        
                    #Netted Settlements with trdnbr
                    '''if settle.relation_type == 'Net':
                        Netted_Settlement(settle, valid_port)
        else:
            #Payment of Netted Settlements without trdnbr
            Netted_Settlement(settle, valid_port)
            '''
    return 'Done'

'''def Netted_Settlement(settle, valid_port, *rest):
    low_set = get_lowest_settlement(settle,[])
    netSumm = len(low_set)
    netCounter = 0

    for s in low_set:
        settlev = ael.Settlement[s]        
        leg0 = settlev.trdnbr.insaddr.legs()[0]
        if settlev.trdnbr.add_info('Funding Instype')=='FDI'\
            and settlev.value_day<leg0.end_day\
            and settlev.value_day>leg0.start_day\
            and (settlev.type in ('Fixed Amount','Fixed Rate'))\
            and leg0.amort_type=='Annuity':
            if not get_Port_Struct_from_Port(settlev.trdnbr.prfnbr,'GRAVEYARD'):
                netCounter += 1
                
    if netCounter == netSumm:
        clone = settle.clone()
        clone.status = 'Released'
        clone.commit()
'''

#Payment(1)
