""" Settlement:1.2.2.hotfix23 """

import ael, FSettlementGeneral2, FSettlementGeneral, FSettlementGeneral3, FSettlementVariables
import FSettlementGeneralRT, sets

key_names = ['trdnbr', 'amount', 'curr', 'value_day',
                  'to_prfnbr', 'from_prfnbr', 'status',
                  'type', 'delivery_type', 'acquirer_ptyid',
                  'acquirer_account', 'acquirer_accname',
                  'party_ptyid', 'party_account', 'party_accname']
                  

def set_values_in_dictionary(d, s):

    for key_name in key_names:
        d[key_name] = 0
        
    if s.trdnbr:
        d['trdnbr'] = s.trdnbr.trdnbr
    if s.curr:
        d['curr'] = s.curr.insaddr
    if s.value_day:
        d['value_day'] = s.value_day.to_string() 
    if s.to_prfnbr:
        d['to_prfnbr'] = s.to_prfnbr.prfnbr
    if s.from_prfnbr:
        d['from_prfnbr'] = s.from_prfnbr.prfnbr
    if s.type:
        d['type'] = s.type
    if s.delivery_type:
        d['delivery_type'] = s.delivery_type
    if s.acquirer_ptyid:
        d['acquirer_ptyid'] = s.acquirer_ptyid
    if s.acquirer_account:
        d['acquirer_account'] = s.acquirer_account
    if s.acquirer_accname:
        d['acquirer_accname'] = s.acquirer_accname
    if s.acquirer_accname:
        d['acquirer_accname'] = s.acquirer_accname
    if s.party_ptyid:
        d['party_ptyid'] = s.party_ptyid
    if s.party_account:
        d['party_account'] = s.party_account
    if s.party_accname:
        d['party_accname'] = s.party_accname
    d['amount'] = s.amount


def is_updated(old_s, new_s):
    old_d = {}
    new_d = {}
    set_values_in_dictionary(old_d, old_s)
    set_values_in_dictionary(new_d, new_s)
    ret = False
    for k in old_d.keys():
       if (old_d[k] and not new_d[k]) or \
       (not old_d[k] and new_d[k]):
           ret = True
           break
       else:
           if not (old_d[k] == new_d[k]):
               ret = True
               break
    return ret
    

def get_amount(t, closed_tr = None, case = 1, closing_trs = None):
    i = t.insaddr
    if case == 1: #Settlement amount for non closed trade
        nominal = t.nominal_amount()
        return nominal * (i.mtm_price(i.exp_day) - t.price )
    elif case == 2: #Settlement amount for the closing trade
        t_nominal = t.nominal_amount()
        return t_nominal * (closed_tr.price - t.price)
    elif case == 3: #Settlement amount for closed trade
        close_nom = 0.0
        for c_t in closing_trs:
            close_nom = close_nom + c_t.nominal_amount()
        t_nominal = t.nominal_amount()
        nominal = t_nominal + close_nom
        return nominal * (i.mtm_price(i.exp_day) - t.price)
        
default = ael.date_today().to_string(ael.DATE_ISO)
default_list = default.split('-')

ael_variables = [['year', 'Year (yyyy)', 'string', None, default_list[0], 1, 0],
                 ['month', 'Month (mm)', 'string', None, default_list[1], 1, 0],
                 ['day', 'Day (dd)', 'string', None, default_list[2], 1, 0]]

def create_new(trade, update = 0):
    s = None
    if trade.status in FSettlementVariables.status:
        if FSettlementGeneral2.is_closing(trade):
            closed_tr = ael.Trade[trade.contract_trdnbr]
            s = FSettlementGeneral3.create_payout_settlement(trade, 2, closed_tr)
        elif FSettlementGeneral2.is_closed(trade):
            if trade.insaddr.settlement != 'Physical Delivery':
                closing_trs = FSettlementGeneral2.get_closing_trades(trade.trdnbr)
                s = FSettlementGeneral3.create_payout_settlement(trade, 3, None, closing_trs)
        else:
            if trade.insaddr.settlement != 'Physical Delivery':
                s = FSettlementGeneral3.create_payout_settlement(trade)
    if s and s.amount != 0.0 and not update and FSettlementGeneral.paydayOK(s.value_day, trade, 1, 'Payout'):
        FSettlementGeneral.append_transaction(s)
        return (None, 1)   
    else:
        return (s, 1)
        
        
def ael_main(dict):

    date_str = dict['year'] + '-' + dict['month'] + '-' + dict['day']

    query = """SELECT t.trdnbr
               FROM Trade t,
                    Instrument i
               WHERE t.insaddr = i.insaddr AND
                     i.instype = \'Future/Forward\' AND
                     i.otc = \'Yes\' AND
                     (i.settlement = 'Cash' OR i.settlement = 'Physical Delivery') AND
                     i.exp_day = """ + '\'' + date_str + '\''
    
    commit_count = 0
    created_count = 0
    query_list1 = None
    try:
        query_list1 = ael.asql(query, 1)[1][0]
    except Exception as e:
        ael.log('Exception in FUpdateFuturForward! Cause: %s' % e)
    if query_list1:
        for (trade,) in query_list1:
            query_2 = """SELECT seqnbr
                         FROM Settlement
                         WHERE trdnbr = """ + str(trade.trdnbr)
            settle_found = False
            query_list2 = None
            try:
                query_list2 = ael.asql(query_2, 1)[1][0]
            except Exception as e:
                ael.log('Exception in FUpdateFuturForward! Cause: %s' % e)
            if query_list2:
                for (s,) in query_list2:
                    settle_found = True
                    if s.status not in FSettlementGeneralRT.noupdate_stl_status and FSettlementGeneral3.is_updatable(s) \
                        and FSettlementGeneral.paydayOK(s.value_day, trade, 1, 'Payout'):
                        (new_s, count) = create_new(trade, 1)
                        if new_s and (not s.ref_seqnbr or (s.ref_seqnbr and s.ref_type == 'Net Part')) \
                        and is_updated(s, new_s):
                            if new_s.amount != 0:
                                FSettlementGeneralRT.update_setl_row(s, new_s, 'Updated')
                            else:
                                FSettlementGeneralRT.update_setl_row(s, new_s, 'Recalled')

            if not settle_found:
                create_new(trade)
        FSettlementGeneral.commit_transaction()



