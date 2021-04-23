import acm
import csv
from at_logging import getLogger
from at_ael_variables import AelVariableHandler
ael_variables = AelVariableHandler()

TODAY = acm.Time().DateToday()
LOGGER = getLogger(__name__)

CALC_SPACE = acm.Calculations().CreateStandardCalculationsSpaceCollection()

ael_variables.add('start_date',
                      label='Start Date',
                      default=TODAY,
                      alt=('Execution date from which swwr should '
                           'be reported.'))
                           
ael_variables.add('end_date',
                      label='End Date',
                      default=TODAY,
                      alt=('Execution date from which swwr should '
                           'be reported.'))
    
ael_variables.add('out_path',
    label='Output Path',
    default='/services/frontnt/Task/')

ael_variables.add('result_output_filename',
                      label='Result file name',
                      default='SWWR-REPORT.csv')
    
    
results_list = []
results_headers = ['Trade_ID', 'Trader', 'Instrument', 'Instrument Type', 'ISIN', 'Issuer', 'Agent ID', 'MTM', 'MTM Currency', 'Call_Put', 'Sign', 'Pay_Leg', 'Pay_Leg_Currency', 'Receive_Leg', 'Receive_Leg_Currency', 'Trade Date', 'Maturity Date', 'Counterparty', 'Relationship', 'Parent', 'Group Parent', 'SDS Issuer', 'SDS Party', 'SDS Party Parent', 'SDS Party Group Parent']


def write_csv_file(output_file_location, results_list, header_list):
    """
    Create a file to store all results
    """
    with open(output_file_location, 'wb') as swwr_file:
        swwr_writer = csv.writer(swwr_file, quoting=csv.QUOTE_ALL)
        swwr_writer.writerow(header_list)
        for item in results_list:
            swwr_writer.writerow(item)


def select_trade_population(start_date, end_date):

    query = acm.CreateFASQLQuery(acm.FTrade, 'AND')
    query.AddAttrNode('TradeTime', 'GREATER_EQUAL', start_date)
    query.AddAttrNode('TradeTime', 'LESS_EQUAL', end_date)
    query.AddAttrNodeString('Status', ['FO Confirmed', 'BO Confirmed', 'BO-BO Confirmed'], 'EQUAL')
    query.AddAttrNode('Instrument.InsType', 'NOT_EQUAL', 'SecurityLoan')
        
    op = query.AddOpNode('OR')
    op.AddAttrNode('Instrument.UnderlyingType', 'EQUAL', 'Stock')
    op.AddAttrNode('Instrument.Legs.IndexRef.InsType', 'EQUAL', 'Stock')
    op.AddAttrNode('Instrument.Legs.IndexRef.InsType', 'EQUAL', 'Bond')
    
    trades = query.Select()
    
    return trades


def issuer_valid(trade):
    """issuer details"""
    issuer_id = None
    if trade.Instrument().UnderlyingType() == 'Stock':
        if trade.Instrument().Underlying().Issuer():
            issuer_id = trade.Instrument().Underlying().Issuer().Oid()
            underlying_type = trade.Instrument().InsType()
            
    elif len(trade.Instrument().Legs()) != 0:
        if trade.Instrument().Legs()[0].IndexRef() and trade.Instrument().Legs()[0].IndexRef().InsType() in ['Stock', 'Bond']:
            if trade.Instrument().Legs()[0].IndexRef().Issuer():
                issuer_id = trade.Instrument().Legs()[0].IndexRef().Issuer().Oid()
                underlying_type = trade.Instrument().Legs()[0].IndexRef().InsType()
        elif len(trade.Instrument().Legs()) != 1 and trade.Instrument().Legs()[1].IndexRef() and trade.Instrument().Legs()[1].IndexRef().InsType() in ['Stock', 'Bond']:
            if trade.Instrument().Legs()[1].IndexRef().Issuer():
                issuer_id = trade.Instrument().Legs()[1].IndexRef().Issuer().Oid()
                underlying_type = trade.Instrument().Legs()[1].IndexRef().InsType()
            
    return issuer_id


def issuer_details(issuer_id):
    issuer_party = acm.FParty[issuer_id]
    issuer_name = issuer_party.Name()
    SDS_issuer = issuer_party.AdditionalInfo().BarCap_Eagle_SDSID()
    
    return issuer_party, issuer_name, SDS_issuer
    

def counterparty_details(trade):
    counterparty = trade.Counterparty()
    party_name = counterparty.Name()
    party_parent_id = counterparty.AdditionalInfo().Parent_ID()
    party_group_parent_id = counterparty.AdditionalInfo().Group_Parent_ID()
    SDS_party = counterparty.AdditionalInfo().BarCap_Eagle_SDSID()
    
    if party_group_parent_id:
        party_group_parent = acm.FParty[party_group_parent_id]
        party_group_parent_name = party_group_parent.Name()
        SDS_party_group_parent_name = party_group_parent.AdditionalInfo().BarCap_Eagle_SDSID()
    else:
        party_group_parent_name = 'None'
        SDS_party_group_parent_name = 'None'
        
    if party_parent_id:
        party_parent = acm.FParty[party_parent_id]
        party_parent_name = party_parent.Name()
        SDS_party_parent_name = party_parent.AdditionalInfo().BarCap_Eagle_SDSID()
        
    else:
        party_parent_name = 'None'
        SDS_party_parent_name = 'None'
        
    return party_parent_id, party_group_parent_id, party_name, SDS_party, party_group_parent_name, SDS_party_group_parent_name, party_parent_name, SDS_party_parent_name


def trade_details(trade): 
    trade_id = trade.Oid()
    sign = trade.Direction()
    trade_date = trade.TradeTime()  
    maturity_date = trade.Instrument().ExpiryDate()
    agent_id = ''
    mtm = mtm = trade.Calculation().MarkToMarketPrice(CALC_SPACE, TODAY, 'ZAR').Value().Number()
    mtm_currency = 'ZAR'
    
    if trade.Trader():
        trader = trade.Trader().Name()

    return trade_id, sign, trade_date, maturity_date, agent_id, mtm, mtm_currency, trader
   

def instrument_details(trade):
    ins_name = trade.Instrument().Name()
    ins_type = trade.Instrument().InsType()
    isin = trade.Instrument().Isin()
    
    if trade.Instrument().InsType() == 'Option':
        if trade.Instrument().IsCallOption():
            call_put = 'call'
        else:
            call_put = 'put'
    else:
        call_put = ''
        
    return ins_name, ins_type, isin, call_put


def leg_details(trade):
    if len(trade.Instrument().Legs()) > 1:
        for leg in trade.Instrument().Legs():
            if leg.PayLeg():
                pay_leg = 'Pay'
                pay_leg_currency = leg.Currency().Name()
            else:
                receive_leg = 'Receive'
                receive_leg_currency = leg.Currency().Name()
                
    elif len(trade.Instrument().Legs()) == 1:
        leg  = trade.Instrument().Legs()[0]
        if leg.PayLeg():
            pay_leg = 'Pay'
            pay_leg_currency = leg.Currency().Name()
            receive_leg = ''    
            receive_leg_currency = ''
            
        else:
            receive_leg = 'Receive'
            receive_leg_currency = leg.Currency().Name()
            pay_leg = ''
            pay_leg_currency = ''
                
    else:
        pay_leg = ''
        pay_leg_currency = ''
        receive_leg = ''    
        receive_leg_currency = ''
        
    return pay_leg, pay_leg_currency, receive_leg, receive_leg_currency
                    

def relationship_check(trades, out_path, file_name):
    """issuer valid"""
    for trade in trades:
        issuer_id = issuer_valid(trade)
        if issuer_id:
            """issuer details"""
            [issuer_party, issuer_name, SDS_issuer] = issuer_details(issuer_id)
            
            """counterparty details"""
            [party_parent_id, party_group_parent_id, party_name, SDS_party, party_group_parent_name, SDS_party_group_parent_name, party_parent_name, SDS_party_parent_name] = counterparty_details(trade)
            
            if str(party_parent_id) == str(issuer_id) or str(party_group_parent_id) == str(issuer_id):
                """trade details"""
                [trade_id, sign, trade_date, maturity_date, agent_id, mtm, mtm_currency, trader] = trade_details(trade)
                
                """instrument details"""
                [ins_name, ins_type, isin, call_put] = instrument_details(trade)
                
                """leg details"""
                [pay_leg, pay_leg_currency, receive_leg, receive_leg_currency] = leg_details(trade)
                
                """relationship check"""
                if str(party_parent_id) == str(issuer_id):
                    """direct relationship between counterparty and issuer"""
                    relationship = 'PARENT'
                    results_list.append([trade_id, trader, ins_name, ins_type, isin, issuer_name, agent_id, mtm, mtm_currency, call_put, sign, pay_leg, pay_leg_currency, receive_leg, receive_leg_currency, trade_date, maturity_date, party_name, relationship, party_parent_name, party_group_parent_name, SDS_issuer, SDS_party, SDS_party_parent_name, SDS_party_group_parent_name])
                    
                elif str(party_group_parent_id) == str(issuer_id):
                    """indirect relationship between counterparty and issuer"""
                    relationship = 'GROUP PARENT'
                    results_list.append([trade_id, trader, ins_name, ins_type, isin, issuer_name, agent_id, mtm, mtm_currency, call_put, sign, pay_leg, pay_leg_currency, receive_leg, receive_leg_currency, trade_date, maturity_date, party_name, relationship, party_parent_name, party_group_parent_name, SDS_issuer, SDS_party, SDS_party_parent_name, SDS_party_group_parent_name])
                
    output_file_location =  out_path + file_name
    
    try:
        write_csv_file(output_file_location, results_list, results_headers)
        LOGGER.info("Completed successfully.")
    except Exception as exc:
        LOGGER.exception("Error writing to file: %s", exc)
   


def ael_main(ael_dict):
    
    trades = select_trade_population(ael_dict['start_date'], ael_dict['end_date'])
    relationship_check(trades, str(ael_dict['out_path']), str(ael_dict['result_output_filename']))
