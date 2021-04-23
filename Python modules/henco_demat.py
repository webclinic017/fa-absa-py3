import acm, sys, csv, at_addInfo

MMSS_ISIN_REQUEST_STATE_CHART_NAME = 'MM ISIN Management'
   
def amend_add_info_spec(name, type, description, data_type_type, data_type_group):
    acm.BeginTransaction()
    try:
        spec = acm.FAdditionalInfoSpec[name]
        if spec:
            spec.Name(name)
            spec.Description(description)
            spec.RecType(type)
            spec.DataTypeType(data_type_type)
            spec.DataTypeGroup(data_type_group)
            spec.Commit()
        else:
            print 'AddInfo %s on %s does not exist. Aborting.' % (name, type)
            return
        acm.CommitTransaction()
        print 'Successfully amended AddInfoSpec %s for %s' % (name, type)
    except Exception, e:
        acm.AbortTransaction()
        print 'Error: ', e

def create_choicelist(name , list, desc):

    acm.BeginTransaction()
    try:

        if not acm.FChoiceList[name]:
            chl_request = acm.FChoiceList()
            chl_request.Name(name)
            chl_request.List(list)
            chl_request.Description(desc)
            chl_request.Commit()

            print 'Choice List [%s] created !!' % (name)
        else:
            print 'Choice List [%s] already exists!!' % (name)
            
        acm.CommitTransaction()            
            
    except Exception, e:
        print 'Exception', e
        acm.AbortTransaction()
   
def setup_parties():
    print 'Updating ABSA BANK LTD account and alias'
    acm.PollAllDbEvents()

    absa = acm.FParty['ABSA BANK LTD']

    absa_issuer_bpid = acm.FPartyAlias()
    absa_issuer_bpid.Name('ABP/ZA700090')
    absa_issuer_bpid.Party(absa)
    absa_issuer_bpid.Type(acm.FPartyAliasType['MM_DEMAT_Issuer_BPID'])

    absa_trader_bpid = acm.FPartyAlias()
    absa_trader_bpid.Name('ZA600195')
    absa_trader_bpid.Party(absa)
    absa_trader_bpid.Type(acm.FPartyAliasType['MM_DEMAT_Trader_BPID'])

    absa_trader_bpid2 = acm.FPartyAlias()
    absa_trader_bpid2.Name('ZA601840')
    absa_trader_bpid2.Party(absa)
    absa_trader_bpid2.Type(acm.FPartyAliasType['MM_DEMAT_Trader_BPID'])
    try:
        absa_issuer_bpid.Commit()
    except Exception, e:
        print 'Exception', e
    try:
        absa_trader_bpid.Commit()
    except Exception, e:
        print 'Exception', e
    try:
        absa_trader_bpid2.Commit()
    except Exception, e:
        print 'Exception', e

    sor_account = acm.FAccount()
    sor_account.Name('FIRN/4912/ZARN')
    sor_account.Account('05500206484')
    sor_account.CorrespondentBank( acm.FParty['STANDARD CHARTERED BANK'])
    bic1alias = [a for a in acm.FParty['STANDARD CHARTERED BANK'].Aliases() if a.Name() == 'SCBLZAJJ']
    sor_account.Bic(bic1alias[0])
    sor_account.NetworkAliasType('SWIFT')
    sor_account.Depository('SCB/ZA100019/10003176')
    sor_account.Currency(acm.FInstrument['ZAR'])
    sor_account.Party(absa)
    sor_account.AccountType(acm.FEnumeration['enum(AccountType)'].Enumeration('Cash and Security') )
    try:
        sor_account.Commit()
    except Exception, e:
        print 'Exception', e

    print 'Updating Funding Desk account and alias'
    funding_desk =  acm.FParty['Funding Desk']

    funding_desk_trader_bpid = acm.FPartyAlias()
    funding_desk_trader_bpid.Name('ZA601840')
    funding_desk_trader_bpid.Party(funding_desk)
    funding_desk_trader_bpid.Type(acm.FPartyAliasType['MM_DEMAT_Trader_BPID'])

    try:
        funding_desk_trader_bpid.Commit()
    except Exception, e:
        print 'Exception',e

    accno = '05500206484'
    fd_sor_account = acm.FAccount.Select01(" party = %i and account = '%s'" % (funding_desk.Oid(), accno ) , "")

    if fd_sor_account is None:
        fd_sor_account = acm.FAccount()
        fd_sor_account.Name('SOR/CASH_ACCOUNT')
        fd_sor_account.Account(accno)
        fd_sor_account.Party(funding_desk)

    fd_sor_account.CorrespondentBank( acm.FParty['STANDARD CHARTERED BANK'])
    bic1alias = [a for a in acm.FParty['STANDARD CHARTERED BANK'].Aliases() if a.Name() == 'SCBLZAJJ']
    fd_sor_account.Bic(bic1alias[0])
    fd_sor_account.NetworkAliasType('SWIFT')
    fd_sor_account.Depository('SCB/ZA100019/10003176')
    fd_sor_account.Currency(acm.FInstrument['ZAR'])
    fd_sor_account.AccountType(acm.FEnumeration['enum(AccountType)'].Enumeration('Cash and Security') )
    
    try:
        fd_sor_account.Commit()
    except Exception, e:
        print 'Exception', e

    try:
        fd_sor_account.Commit()
    except Exception, e:
        print 'Exception', e

    print 'Updating Money Market Desk account and alias'
    moneymarket_desk =  acm.FParty['Money Market Desk']

    moneymarket_desk_trader_bpid = acm.FPartyAlias()
    moneymarket_desk_trader_bpid.Name('ZA601840')
    moneymarket_desk_trader_bpid.Party(moneymarket_desk)
    moneymarket_desk_trader_bpid.Type(acm.FPartyAliasType['MM_DEMAT_Trader_BPID'])

    try:
        moneymarket_desk_trader_bpid.Commit()
    except Exception, e:
        print 'Exception',e
		
    accno = '05500206484'
    mm_sor_account = acm.FAccount.Select01(" party = %i and account = '%s'" % (moneymarket_desk.Oid(), accno ) , "")

    mm_alias = acm.FPartyAlias.Select01("party = %i and type = '%s' and name = '%s' " % (moneymarket_desk.Oid(), 'SWIFT', 'ZAGTZAJ0'),"")

    if mm_sor_account is None:
        mm_sor_account = acm.FAccount()
        mm_sor_account.Name('SOR/CASH_ACCOUNT')
        mm_sor_account.Account(accno)
        mm_sor_account.Party(moneymarket_desk)

    mm_sor_account.CorrespondentBank( acm.FParty['STANDARD CHARTERED BANK'])
    bic1alias = [a for a in acm.FParty['STANDARD CHARTERED BANK'].Aliases() if a.Name() == 'SCBLZAJJ']
    mm_sor_account.Bic(bic1alias[0])
    mm_sor_account.NetworkAliasType('SWIFT')
    mm_sor_account.Depository('SCB/ZA100019/10003176')
    mm_sor_account.Currency(acm.FInstrument['ZAR'])
    mm_sor_account.AccountType(acm.FEnumeration['enum(AccountType)'].Enumeration('Cash and Security') )
    
    try:
        mm_sor_account.Commit()
    except Exception, e:
        print 'Exception', e   

    try:
        mm_sor_account.Commit()
    except Exception, e:
        print 'Exception', e   

    print 'Updating IMPUMELELO Add Infos'
    acm.PollAllDbEvents()

    print 'Updating IMPUMELELO account and alias'
    imp = acm.FParty['IMPUMELELO']

    imp_issuer_bpid = acm.FPartyAlias()
    imp_issuer_bpid.Name('ABP/ZA606151')
    imp_issuer_bpid.Party(imp)
    imp_issuer_bpid.Type(acm.FPartyAliasType['MM_DEMAT_Issuer_BPID'])

    imp_trader_bpid = acm.FPartyAlias()
    imp_trader_bpid.Name('ZA606151')
    imp_trader_bpid.Party(imp)
    imp_trader_bpid.Type(acm.FPartyAliasType['MM_DEMAT_Trader_BPID'])
  
    try:
        imp_issuer_bpid.Commit()
    except Exception, e:
        print 'Exception', e
    try:
        imp_trader_bpid.Commit()
    except Exception, e:
        print 'Exception', e
 
    imp_sor_account = acm.FAccount()

    imp_alias = acm.FPartyAlias.Select01("party = %i and type = '%s' and name = '%s' " % (imp.Oid(), 'SWIFT', 'ZAGTZAJ0'),"") 

    imp_sor_account.Name('SOR/CASH ACCOUNT')
    imp_sor_account.Account('05500206484')
    imp_sor_account.CorrespondentBank( acm.FParty['STANDARD CHARTERED BANK'])
    bic1alias = [a for a in acm.FParty['STANDARD CHARTERED BANK'].Aliases() if a.Name() == 'SCBLZAJJ']
    imp_sor_account.Bic(bic1alias[0])
    imp_sor_account.NetworkAliasType('SWIFT')
    imp_sor_account.Depository('SCB/ZA100019/10084924')
    imp_sor_account.Currency(acm.FInstrument['ZAR'])
    imp_sor_account.Party(imp)
    imp_sor_account.AccountType(acm.FEnumeration['enum(AccountType)'].Enumeration('Cash and Security') )

    try:
        imp_sor_account.Commit()
    except Exception, e:
        print 'Exception', e

    try:
        imp_sor_account.Commit()
    except Exception, e:
        print 'Exception', e

    print 'Updating ACQ STRUCT DERIV DESK account and alias'
    acm.PollAllDbEvents()

    acqsd = acm.FParty['ACQ STRUCT DERIV DESK']

    acqsd_trader_bpid = acm.FPartyAlias()
    acqsd_trader_bpid.Name('ZA606151')
    acqsd_trader_bpid.Party(acqsd)
    acqsd_trader_bpid.Type(acm.FPartyAliasType['MM_DEMAT_Trader_BPID'])

    try:
       acqsd_trader_bpid.Commit()
    except Exception, e:
        print 'Exception', e

    acqsd_sor_account = acm.FAccount()
    acqsd_sor_account.Name('SOR/CASH ACCOUNT')
    acqsd_sor_account.Account('05500206484')
    acqsd_sor_account.CorrespondentBank( acm.FParty['STANDARD CHARTERED BANK'])
    bic1alias = [a for a in acm.FParty['STANDARD CHARTERED BANK'].Aliases() if a.Name() == 'SCBLZAJJ']
    acqsd_sor_account.Bic(bic1alias[0])
    acqsd_sor_account.NetworkAliasType('SWIFT')
    acqsd_sor_account.Depository('SCB/ZA100019/10003176')
    acqsd_sor_account.Currency(acm.FInstrument['ZAR'])
    acqsd_sor_account.Party(acqsd)
    acqsd_sor_account.AccountType(acm.FEnumeration['enum(AccountType)'].Enumeration('Cash and Security') )
    try:
        acqsd_sor_account.Commit()
    except Exception, e:
        print 'Exception', e
		
def add_choice_list():

    #create_choicelist('ABSA_FRN_Main', 'Conf Template', 'FRN Template')
    #create_choicelist('ABSA_CD_Main', 'Conf Template', 'CD Template')
    create_choicelist('ABSA_FI_Generic_Main', 'Conf Template', 'FI Generic Template')
    create_choicelist('Demat', 'Settle Category', 'MM Demat')
    create_choicelist('LNCD', 'MoneyMarket Instype', 'Linked Negotiable Certificate of Dep')

    create_choicelist('Demat Match Request', 'Event', 'Demat Match Request')
    create_choicelist('Demat PreSettle Conf', 'Event', 'Demat PreSettle Conf')
    create_choicelist('Demat Settle Conf', 'Event', 'Demat Settle Conf')

def add_task_schedule():
    task = acm.FAelTask['mq_cust_swift_out_SERVER']

    task_group = acm.FAelTaskGroup()
    task_group.Name('MQ_CUSTOM_SWIFT_OUT')
    try:
        task_group.Commit()
    except Exception, e:
        print 'Exception', e
        
    if task:
        task.Group(task_group)
        try:
            task.Commit()
        except Exception, e:
            print 'Exception', e

        task_sched = acm.FAelTaskSchedule()
        task_sched.Task(task)
        task_sched.Schedule('1:D:1:E,5,0600,1800:20160223')
        task_sched.Period('Day')
        task_sched.PeriodInterval(1)
        task_sched.StartDate(acm.Time().DateToday())
        task_sched.DailyRepeat(True)
        task_sched.DailyRepeatInterval(5)
        #task_sched.DailyRepeatUntil('2016/02/23 08:00:00 PM')
        #task_sched.DailyRunTime('2016/02/23 10:00:00 AM')
        task_sched.DailyRepeatUntil('2016-06-01 08:00:00 PM')
        task_sched.DailyRunTime('2016-06-01 10:00:00 AM')
        task_sched.Enabled(True)
        task_sched.Commit()
    else:
        print 'Task not found!!!'

def create_mmss_isin_request_statechart(replace_existing = True):
    try:
        if replace_existing:
            
            state_chart = acm.FStateChart[MMSS_ISIN_REQUEST_STATE_CHART_NAME]
            if state_chart:
                processes = acm.BusinessProcess.FindBySubjectAndStateChart(None, state_chart)
                for p in processes:
                    p.Delete()
                state_chart.Delete()
                state_chart.Delete()
                print "REMOVED"
            else:
                print 'State Chart not removed, could not be found with name:', MMSS_ISIN_REQUEST_STATE_CHART_NAME
        
        state_chart = acm.FStateChart(name = MMSS_ISIN_REQUEST_STATE_CHART_NAME)
        state_chart.BusinessProcessesPerSubject('Single Active') # Can be Single or Unlimited
        state_chart.Commit()
        
        state_chart.CreateState('New ISIN Request to be sent')
        state_chart.CreateState('New ISIN Request MQ ACKNACK')
        state_chart.CreateState('New ISIN Request Pending')
        state_chart.CreateState('TopUp Reduce Request to be sent')
        state_chart.CreateState('TopUp Reduce Request MQ ACKNACK')
        state_chart.CreateState('TopUp Reduce Request Pending')
        state_chart.CreateState('DeIssue Request to be sent')
        state_chart.CreateState('DeIssue Request MQ ACKNACK')
        state_chart.CreateState('DeIssue Request Pending')
        state_chart.CreateState('DeIssued')
        state_chart.CreateState('Active')
        state_chart.CreateState('New ISIN Failed Response')
        state_chart.CreateState('Topup Reduce Failed Response')
        state_chart.CreateState('Deissue Failed Response')
        state_chart.Commit()
        
        ready_state = state_chart.ReadyState()
        states = state_chart.StatesByName()
        state_new_isin_req_tbs = states['New ISIN Request to be sent']
        state_new_isin_req_ack = states['New ISIN Request MQ ACKNACK']
        state_new_isin_req_waiting = states['New ISIN Request Pending']
        state_amend_req_tbs = states['TopUp Reduce Request to be sent']
        state_amend_req_ack = states['TopUp Reduce Request MQ ACKNACK']
        state_amend_req_waiting = states['TopUp Reduce Request Pending']
        state_deissue_req_tbs = states['DeIssue Request to be sent']
        state_deissue_req_ack = states['DeIssue Request MQ ACKNACK']
        state_deissue_req_waiting = states['DeIssue Request Pending']
        state_inactive = states['DeIssued']
        state_active = states['Active']
        state_failed_new_request = states['New ISIN Failed Response']
        state_failed_amend_request = states['Topup Reduce Failed Response']
        state_failed_deissue_request = states['Deissue Failed Response']

        new_isin_event = acm.FStateChartEvent('Request ISIN')
        new_isin_request_sent_event = acm.FStateChartEvent('Sent ISIN Request')
        new_isin_request_received_event = acm.FStateChartEvent('ISIN response received')
        amend_event = acm.FStateChartEvent('Request Topup or Reduce')
        amend_request_sent_event = acm.FStateChartEvent('Sent Topup Reduce Request')
        amend_request_received_event = acm.FStateChartEvent('Topup Reduce Response Received')
        deissue_event = acm.FStateChartEvent('Request Deissue')
        deissue_request_sent_event = acm.FStateChartEvent('Sent Deissue Request')
        deissue_request_received_event = acm.FStateChartEvent('Deissue Response Received')
        failed_response_event = acm.FStateChartEvent('Failed Response Received')
        nack_event = acm.FStateChartEvent('NACK Received')
        ack_event = acm.FStateChartEvent('ACK Received')
        retry_event = acm.FStateChartEvent('Resend')
        cancel_event = acm.FStateChartEvent('Cancel')
        
        ready_state.CreateTransition(new_isin_event, state_new_isin_req_tbs)
        state_new_isin_req_tbs.CreateTransition(new_isin_request_sent_event, state_new_isin_req_ack)
        state_new_isin_req_ack.CreateTransition(ack_event, state_new_isin_req_waiting)
        state_new_isin_req_ack.CreateTransition(nack_event, state_failed_new_request)
        state_new_isin_req_waiting.CreateTransition(new_isin_request_received_event, state_active)
        state_new_isin_req_waiting.CreateTransition(failed_response_event, state_failed_new_request)

        state_amend_req_tbs.CreateTransition(amend_request_sent_event, state_amend_req_ack)
        state_amend_req_ack.CreateTransition(ack_event, state_amend_req_waiting)
        state_amend_req_ack.CreateTransition(nack_event, state_failed_amend_request)
        state_amend_req_waiting.CreateTransition(amend_request_received_event, state_active)
        state_amend_req_waiting.CreateTransition(failed_response_event, state_failed_amend_request)
        
        state_deissue_req_tbs.CreateTransition(deissue_request_sent_event, state_deissue_req_ack)
        state_deissue_req_ack.CreateTransition(ack_event, state_deissue_req_waiting)
        state_deissue_req_ack.CreateTransition(nack_event, state_failed_deissue_request)
        state_deissue_req_waiting.CreateTransition(deissue_request_received_event, state_inactive)
        state_deissue_req_waiting.CreateTransition(failed_response_event, state_failed_deissue_request)
        
        state_failed_new_request.CreateTransition(retry_event, state_new_isin_req_tbs)
        #state_failed_new_request.CreateTransition(cancel_event, state_active)      #Cancel not possible on New Isin Request Failed. - Only Resend
        
        state_failed_amend_request.CreateTransition(retry_event, state_amend_req_tbs)
        state_failed_amend_request.CreateTransition(cancel_event, state_active)
        
        state_failed_deissue_request.CreateTransition(retry_event, state_deissue_req_tbs)
        state_failed_deissue_request.CreateTransition(cancel_event, state_active)
        
        state_active.CreateTransition(amend_event, state_amend_req_tbs)
        state_active.CreateTransition(deissue_event, state_deissue_req_tbs)
        state_chart.Commit()
    except Exception, e:
        print 'Creation of State Chart Failed', e
        traceback.print_exc()

def run_steps():
    """
    Run the sequence of post-deployment steps.
    Add your steps here.
    """
    add_choice_list()
    create_mmss_isin_request_statechart()
    setup_parties()
    add_task_schedule()
    #demat_isin_mgmt.create_mmss_isin_request_statechart()

NEW_LINE = '\n'

DEMAT_CONTACT_RULE = [
                      ['Funding Desk', 'None', 'Demat Match Request', 'None'],
                      ['Money Market Desk', 'None', 'Demat Match Request', 'None'],
                      [None, 'None', 'Demat Match Request', 'None'],
                      ['Funding Desk', 'None', 'Demat PreSettle Conf', 'None'],
                      ['Money Market Desk', 'None', 'Demat PreSettle Conf', 'None'],
                      [None, 'None', 'Demat PreSettle Conf', 'None']
                      ]

DEMAT_CONF_INSTRUCTION = [ 
                           ['Demat None New Trade Email','None','Email','All','New Trade','Demat','ABSA_FI_Generic_Main'],
                           ['Demat None Network','None','Network','All','','Demat','SWIFT']
                         ]

"""
ciName, ciInsType, ciTransport, ciIntDept, ciEvent, ciInsCategory,  ciTemplate
"""

#DEMAT_ACQUIRERS       = ['Funding Desk','ACQ STRUCT DERIV DESK','Money Market Desk', 'IMPUMELELO']
DEMAT_EVENTS          = ['Demat Match Request','Demat PreSettle Conf','New Trade', 'Cancellation']
DEMAT_TEMPLATES       = ['SWIFT','ABSA_FI_Generic_Main']

demat_desks = dict()

def get_choice(choice, list):
    return acm.FChoiceList.Select01("list = '%s' and name = '%s' " % ( list ,choice), "")

def setup_mapping_data():
    """
    Set up of mapping data
    """

    global  demat_evnts,   demat_tmplates # demat_desks
    #demat_desks          = dict(zip(DEMAT_ACQUIRERS, list( map(lambda x: acm.FParty[x] or None, DEMAT_ACQUIRERS ) ) )  )
    demat_evnts          = dict(list(zip(DEMAT_EVENTS, list(map( lambda x: get_choice(x, 'Event'), DEMAT_EVENTS ) ) )))
    demat_tmplates       = dict(list(zip(DEMAT_TEMPLATES, list(map( lambda x: get_choice(x, 'Conf Template'), DEMAT_TEMPLATES ) ) )) )


def get_demat_settle_cat():
    """
    Gets the 'Demat' settle category
    """
    return acm.FChoiceList['Demat']

def update_alias(data):
    """
    Creates the party alias based on data in the extract

    The input for ALIAS should be of the format
         ALIAS,<party name>,<type>,<alias>

    """
    name, type, value  = data[1], data[2], data[3]

    party = acm.FParty[name]
    acm.BeginTransaction()
    if not party is  None:
        alias = acm.FPartyAlias.Select01("party = %i and type = '%s' and name = '%s' " % (party.Oid(), type, value),"") 
        print 'Party alias with [%s, %s] already exists for party [%s] !!  ' % ( type, value, name )
        if alias is None:
            alias = acm.FPartyAlias()
            alias.Type(type)
            alias.Name(value)
            alias.Party(party)
            try:
                alias.Commit()

                acm.CommitTransaction()
                print 'update_alias: Update alias [%s] for party [%s] , value [%s]committed' % (type, name, value) 
            except Exception, e:
                acm.AbortTransaction()
                print 'ERROR: Updating rows [%s] ' % (str(data)) 
                print 'ERROR: ' + str(e)  + NEW_LINE

def update_contacts(data):
    """
    Creates the party alias based on data in the extract as well as the demat contact
    The input for CONTACT should look like 
        CONTACT,<party name>,<contact name>,<email>,<network alias>
    """
    #name, contactname        = data[1], data[2]
    #email, networkalias      = data[3], data[4]
    name, contactname        = data[1], 'Demat'
    email, networkalias      = '', 'ZAGTZAJ0'
    party = acm.FParty[name]
    print 'Counterparty_Name:', name
    if not party is  None:
        alias = acm.FPartyAlias.Select01("party = %i and type = 'SWIFT' and name = '%s'" % (party.Oid(), networkalias ),"")
        if  alias is None:
            alias = acm.FPartyAlias()
            alias.Type('SWIFT')
            alias.Name(networkalias)
            alias.Party(party)
            try:
                alias.Commit()
                print 'update_alias: Update alias [%s] committed  ' % (networkalias)
            except Exception , e:
                print 'ERROR:  Setting alias value [%s] for party [%s] ' % (networkalias, name)
		print "email , networkalias", email , networkalias
				
        contact = acm.FContact.Select01( "party = %i and  email = '%s' and networkAlias = '%s' and networkAliasType = 'SWIFT' " % (party.Oid() , email , networkalias ) , "")
        #print contact
        if contact is None:
            contact = acm.FContact()
            contact.Fullname(contactname)
            contact.Email(email)
            contact.NetworkAliasType('SWIFT')
            contact.NetworkAlias(alias)
            contact.Party(party)
            try:
                contact.Commit()
                print 'update_contacts: Update contact [%s] committed  ' % (contactname)
            except Exception, e:
                print 'ERROR: Updating rows [%s] ' % (str(data)) 
                print 'ERROR: ' + str(e)  + NEW_LINE

            if not contact is None:
                for rule in DEMAT_CONTACT_RULE:
                    #contact_rule_data = ['All'] + rule
                    update_contact_rule(contact, rule )
                    contact.Fullname(contactname)
                    try:
                        contact.Commit()
                        print 'update_contacts: Update contact rule [%s] committed  ' % (contactname)
                    except Exception, e:
                        print 'ERROR: Updating rows [%s] ' % (str(data)) 
                        print 'ERROR: ' + str(e)  + NEW_LINE

def update_contact_rule(contact, data):
    """
    Creates the contact rule based on data in the extract
    """
    global demat_evnts
    acquirer, instype, event, currency = data[0], data[1], data[2], data[3]
    if not contact is None:
        contact_rule = acm.FContactRule()
        contact_rule.Contact(contact)
        contact_rule.Acquirer(acquirer)
        contact_rule.InsType(instype)
        contact_rule.UndInsType('None')
        contact_rule.EventChlItem(event)
        contact_rule.Currency(None)
        contact_rule.IssuanceType('None')
        try:
            contact_rule.Commit()
            #print 'update_contacts_rule : Update contact rule [%s] committed  ' % (str(','.join(data)))
            print 'update_contacts_rule : Update contact rule %s committed  ' % (str(data))
        except Exception, e:
            #print 'ERROR: Updating rows [%s] ' % (str(data)) 
            print 'ERROR: Updating rows %s ' % (str(data)) 
            print 'ERROR: ' + str(e)  + NEW_LINE

def update_settle_instruction(data):
    """
    Creates the list of Settlement Instructions
    The input for SETTLE_INSTR should look like 
        SETTLE_INSTR,<party name>
    """
    siParty = data[1]
    pty = acm.FParty[siParty]
    
    if not pty is None:
        acm.BeginTransaction()
        try:
            acc = acm.FAccount()
            acc.Name('ABSA//ALLN')
            acc.Account('GENERIC')
            acc.AccountType('Cash and Security')
            acc.NetworkAliasType('SWIFT')
            alias = [a for a in acm.FParty['ABSA BANK LTD'].Aliases() if a.Name() == 'ABSAZAJJ']
            acc.Bic(alias)
            acc.CorrespondentBank('ABSA BANK LTD')
            acc.NetworkAliasType('SWIFT')
            acc.Party(pty)
            #try:
            acc.Commit()
            #except Exception, e:
            #print 'Cant commit account:', e

            si = acm.FSettleInstruction()
            si.Name('DEMATGEN')
            si.Party(pty)
            si.InstrumentType('None')
            si.CashSettleCashFlowType('None')
            si.UndInsType('None')
            si.SettleDeliveryType('None')
            si.SettleCategoryChlItem(get_demat_settle_cat())
            si.OtcInstr('None')
            si.IssuanceType('None')
            si.DefaultInstruction('True')
            #try:
            si.Commit()
            #except Exception, e:
            #print 'Cant commit ssi:', e
                
            siRule = acm.FSettleInstructionRule()
            siRule.CashAccount(acc)
            siRule.EffectiveFrom(acm.Time().DateToday())
            siRule.SettleInstruction(si)
            #try:
            siRule.Commit()
            #except Exception, e:
            #print 'Cant commit ssi rule:', e
            
            acm.CommitTransaction()
            print 'update_settle_instruction : Settlement Instruction  [%s] on party [%s] committed ' % ('DEMATGEN', siParty)
        except Exception, e:
            acm.AbortTransaction()
            print 'Cant commit settle instruction and rule:', e
            print 'Counterparty_Name:', pty.Name()

def update_conf_instruction(data):
    """
    Creates a Confirmation
    
    The input for CONF_INSTR should look like 
        CONF_INSTR,<party name>

    """
    global demat_evnts

    name = data[1]
    party = acm.FParty[name]
    #print 'Counterparty_Name:', name
    for confinstr in DEMAT_CONF_INSTRUCTION:
        ciName, ciInsType, ciTransport, ciIntDept, ciEvent, ciInsCategory,  ciTemplate = confinstr[0], confinstr[1], confinstr[2], confinstr[3], confinstr[4], confinstr[5],  confinstr[6]
        acm.BeginTransaction()
        try:
            #print 'Counterparty_Name:', party.Name()
            #ci = acm.FConfInstruction.Select01("counterparty = %i and insType = '%s' and eventChlItem = '%s' and transport = '%s' " % (party.Oid(), ciInsType , ciEvent, ciTransport ),"")
            #if ci is None:
            ci = acm.FConfInstruction()
            ci.Counterparty(party)
            ci.Transport(ciTransport)
            if ciEvent in demat_evnts:
                ci.EventChlItem(demat_evnts[ciEvent]) 
            else:  
                ci.EventChlItem()
            ci.Name(ciName)
            ci.InternalDepartment()
            ci.Active(True)
            if not ciInsType is None:
                ci.InsType(ciInsType)
            ci.SettleCategoryChlItem(get_demat_settle_cat())
            #try:
            ci.Commit()
            #except Exception, e:
            #print 'Cant commit conf instruction:', e
            rule = acm.FConfInstructionRule()
            rule.Stp('True')
            rule.ChaserCutoffMethod('None')
            rule.ChaserCutoffPeriodCount(0)
            rule.ConfInstruction(ci)
            rule.Type('Default')
            rule.TemplateChoiceList(demat_tmplates[ciTemplate])
            #try:
            rule.Commit()
            #except Exception, e:
            #print 'Cant commit conf instruction rule:', e
            #try:
            #else:
            #raise Exception('Duplicate conf instruction')
            acm.CommitTransaction()
            print 'update_conf_instruction: Confirmation Instruction [%s] created' % (ciName)
        except Exception, e:
            acm.AbortTransaction()
            print 'Cant commit conf instruction [%s]:' % (ciName), e
        #else:
        #print 'update_conf_instruction : Confirmation Instruction [%s, %s, %s] for party [%s] exists !!' % (ciInsType , ciEvent , ciTransport, name)

def create_add_info(ins, ai_name, ai_value):
    """
    Creates additional info "add_info_name", "add_info_Value"
    """

    try:

        ais = acm.FAdditionalInfoSpec[ai_name]
        if not ais is None:
            ai = acm.FAdditionalInfo.Select01("addInf = %i and recaddr =  %i " % (ais.Oid() , ins.Oid() ) , "")
            if ai is None:
                ai = acm.FAdditionalInfo()
            ai.Recaddr(ins.Oid())
            ai.AddInf(ais)
            ai.FieldValue(ai_value)
            ai.Commit()
    except Exception, e:
        print " Error: Creating an additional info   ", e


def get_first_trade(ins):
    """
    Gets the first trade on an instrument
    """

    first_trade = None
    ins_trade_start = 0

    for trd in ins.Trades():
 
        if trd.Status() in ['FO Confirmed','BO Confirmed','BO-BO Confirmed','Void']:

            if ins_trade_start == 0:
                ins_trade_start = trd.CreateTime()
                first_trade = trd

            elif ins_trade_start > trd.CreateTime():
                first_trade = trd
                ins_trade_start = trd.CreateTime()

    return first_trade

def update_instrument(row):
    """
    Updates instrument to flag the demat instruments
    The format of the input line is 
          INSTRUMENT,<isin>,<amount>,<mm instype>,<withhold tax flag>,<sor account>,<issuer bpid>,<short_code.

    """
    import demat_config
    import demat_swift_mt598

    isin, amount, mminstype, wtaxflag, soracc, issbpid, shortcode  = row[1], row[2], row[3], row[4], row[5], row[6], row[7]
    wtaxflag = (wtaxflag== 'Yes') and 'Yes' or 'No'
    ins = acm.FInstrument.Select01("isin = %s" % (isin),"")
    sc = acm.FStateChart[MMSS_ISIN_REQUEST_STATE_CHART_NAME]

    if not ins is None:
        print 'Instrument:', ins.Name()
        bp = acm.FBusinessProcess.Select01("subject_seqnbr = %d " % (ins.Oid()) , "")
        if bp == None:
            bp = acm.BusinessProcess.InitializeProcess(ins, sc)
            bp.ForceToState('Active', str(amount))
            try:
                bp.Commit()
                #print 'Instrument [%s] inserted into Business process ' % (ins.Name())
                print 'Commit 1 done'
            except Exception, e:
                'Commit 1 failed', e
        create_add_info(ins, 'Demat_Instrument', 'Yes')
        """
        Get the pre settle trade
        """
        ps_trade = get_first_trade(ins)
        if not ps_trade is None:
            create_add_info(ps_trade, 'MM_DEMAT_PRE_SETT', 'Yes')

        create_add_info(ins, 'MM_MMInstype',mminstype)
        create_add_info(ins, 'Demat_MinTrdDeno',0.01)
        create_add_info(ins, 'Demat_WthhldTax',wtaxflag)
        create_add_info(ins, 'Demat_Ins_SOR_Acc',soracc)
        create_add_info(ins, 'Demat_Issuer_BPID',issbpid)

        try:
            ins.Commit()
            #print 'update Instrument: Instrument [%s] updated ' % (ins.Name())
            print 'Commit 2 done'
        except Exception, e:
            #print 'update Instrument: Could not coomit  instrument [%s]' % (ins.Name()), e
            'Commit 2 failed', e

        print 'Demat_Issuer_BPID', ins.AdditionalInfo().Demat_Issuer_BPID()
        """
        helper = demat_swift_mt598.Demat_MT598_Helper(ins)
        short_code = helper.IdentificationSecurities()
        """
        create_add_info(ins, 'Demat_IsinShortDesc',shortcode)
        try:
            ins.Commit()
            #print 'update Instrument: Instrument [%s] updated ' % (ins.Name())
            print 'Commit 3 done'
        except Exception, e:
            #print 'update Instrument: Could not commit  instrument [%s]' % (ins.Name()), e
            print 'Commit 3 failed', e

def upload_data(filepath):
    """
    This function is used to update party details for MM Demat rollout
    """
    upload_party_funcs = dict()

    upload_party_funcs['ALIAS']                 = update_alias
    upload_party_funcs['INSTRUMENT']            = update_instrument
    #upload_party_funcs['CONTACT']       = update_contacts
    #upload_party_funcs['SETTLE_INSTR']  = update_settle_instruction
    #upload_party_funcs['CONF_INSTR']    = update_conf_instruction
    '''upload_party_funcs['CONTACT_RULE']  = update_contact_rule'''

    csvfile = open(filepath,'r')
    csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in csvreader:
        opcode = len(row) > 0 and row[0] or None
        if opcode in upload_party_funcs:
            upload_party_funcs[opcode](row)
        elif opcode == 'CONTACTSETTLECONF':
            update_contacts(row)
            update_settle_instruction(row)
            update_conf_instruction(row)
        #elif opcode == 'INSTRUMENT':
        #    update_instrument(row)
        else:
            print 'upload_party : No Operation found for the row [%s]' % (str(row))

#run_steps()

'''
**************************************
Path must contain double slashes \\
Disable rule 130 and rule 131 in FValidation_General by commenting out the validate_entity lines and restart FA before running the below
    OR, run with FMaintenance user.
Comment out run_steps before running these manually.
'''
#setup_mapping_data()
#upload_data("demat_live_data_alias.csv")
#upload_data("demat_live_data_contact_ssi_confinstr.csv")

#create_mmss_isin_request_statechart
#upload_data("demat_live_data_ins.csv")
