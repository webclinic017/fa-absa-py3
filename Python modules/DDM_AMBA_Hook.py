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
    
def modify_instrument_message(m, s):
    instrument_obj = object_by_name(m, ['', '+', '!'], 'INSTRUMENT')
    for leg_obj in objects_by_name(instrument_obj, ['', '+', '!'], 'LEG'):
        for cashflow_obj in objects_by_name(leg_obj, ['', '+', '!'], 'CASHFLOW'):
            for reset_obj in objects_by_name(cashflow_obj, ['', '+', '!'], 'RESET'):
                cashflow_obj.mbf_remove_object()
            leg_obj.mbf_remove_object()
    
    for add_info_obj in objects_by_name(instrument_obj, ['', '+', '!'], 'ADDITIONALINFO'):
        instrument_obj.mbf_remove_object()
                
    return (m, s)

def modify_trade_message(m, s):
    trade_obj = object_by_name(m, ['', '+', '!'], 'TRADE')
    for payment_obj in objects_by_name(trade_obj, ['', '+', '!'], 'PAYMENT'):
        trade_obj.mbf_remove_object()
    
    for add_info_obj in objects_by_name(trade_obj, ['', '+', '!'], 'ADDITIONALINFO'):
        trade_obj.mbf_remove_object()
                
    return (m, s)

def modify_sender(m, s):
    result = (m, s)
    type_obj = m.mbf_find_object('TYPE', 'MBFE_BEGINNING')
    type_value = type_obj.mbf_get_value() 
    
    if type_value in ['INSERT_INSTRUMENT', 'UPDATE_INSTRUMENT']:
        result = modify_instrument_message(m, s)
    elif type_value in ['INSERT_TRADE', 'UPDATE_TRADE']:
        result = modify_trade_message(m, s)
    
    return result
