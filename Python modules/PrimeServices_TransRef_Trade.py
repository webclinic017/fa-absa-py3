import acm, ael

'''

Purpose : script is used to - replace counterparty with the portfolio name of the PB agency trade in the ASQL 
                            - replace hostid with the nutron client code (i.e. the value of the portfolio add_info field 'AgencyTradPrincipal') of the PB agency trade
                            - if thr trans ref points to an PB agency trade then reflect the unexcor code (i.e. the value of the portfolio add_info field 'CapMkt Unexcor Code') of the PB agency trade
                            - added party_check_transref_trade
Department and Desk  : OPS, OPS
Requester Miguel da Silva, Sipho Ndlalane
Developer Anil Parbhoo, Willie van der Bank
CR Number 713436, 128652 2012-04-12
Jira call PSB-56, ABITFA-1296
'''

def party_check_transref_trade(temp,t,*rest):

    # when called from asql this function is used to replace a CP with a blank space if the acq of the trans ref trade is 'PRIME SERVICES DESK'
    trd = acm.FTrade[t]

    if trd.TrxTrade().Acquirer().Name()=='PRIME SERVICES DESK':
        return ''
    else:
        party = ael.Party[trd.Counterparty().Oid()]
        return party.add_info('UnexCor Code')

def portfolio_of_transref_trade(temp,t,*rest):

    # when called from asql this function is used to replace a CP with the portfolio of the transref trade if the acq of the trans ref trade is 'PRIME SERVICES DESK'
    trd = acm.FTrade[t]

    if trd.TrxTrade().Acquirer().Name()=='PRIME SERVICES DESK':
        return trd.TrxTrade().Portfolio().Name()
    else:
        return trd.Counterparty().Name()
    

def portfolio_add_info_AgencyTradPrincipal(temp,t,*rest):
    # when called from asql This function is used to replace the hostid of the cp with the add info AgencyTradPrincipal of the portfolio of the transref trade if the acq of the trans ref trade is 'PRIME SERVICES DESK'
    trd = acm.FTrade[t]
    

    if trd.TrxTrade().Acquirer().Name()=='PRIME SERVICES DESK':
        return trd.TrxTrade().Portfolio().add_info('AgencyTradPrincipal')
    else:
        return trd.Counterparty().HostId()



def portfolio_add_info_CapMktUnexcorCode(temp,t,*rest):
    # when called from asql this function is used to display the add info CapMkt Unexcor Code of the portfolio of the transref trade if the acq of the trans ref trade is 'PRIME SERVICES DESK'
    # this function does not replace any other value
    trd = acm.FTrade[t]


    if trd.TrxTrade().Acquirer().Name()=='PRIME SERVICES DESK':
        return trd.TrxTrade().Portfolio().add_info('CapMkt Unexcor Code')
    else:
        return ''
        





