
import ael, amb

# Default Instrument types that are supported
# In order to exclude some Instrument types you are allowed to 
# reduce a number of items in this list (do not add anything)
valid_instrument_types = ['Future/Forward', 'FRA', 'Swap', 'Cap', 'IndexLinkedSwap', 'Floor', 'CurrSwap', 'Option', 'Curr', 'Deposit']

def trade_message_can_be_skippped(amb_message):
    skip = False
    for trade_obj in objects_by_name(amb_message, ['', '+', '!'], 'TRADE'):
        #Instrument types that can be skipped
        insaddr_obj = trade_obj.mbf_find_object('INSADDR')
        if insaddr_obj:
           insaddr = insaddr_obj.mbf_get_value()
           if insaddr:           
               instrument = ael.Instrument[int(insaddr)]
               if instrument:           
                   instrument_type = instrument.instype
                   if instrument_type not in valid_instrument_types:
                       skip = True
        #If updated Premium is the same as the original Premium then skip message
        updat_premium_obj = trade_obj.mbf_find_object('!PREMIUM')
        if updat_premium_obj:
            new_premium_obj = trade_obj.mbf_find_object('PREMIUM')
            if new_premium_obj:
                updat_premium = round(float(updat_premium_obj.mbf_get_value()), 2)
                new_premium = round(float(new_premium_obj.mbf_get_value()), 2)
                if updat_premium == new_premium:
                    skip = True
        #If updated Price is the same as the original Price then skip message
        updat_price_obj = trade_obj.mbf_find_object('!PRICE')
        if updat_price_obj:
            new_price_obj = trade_obj.mbf_find_object('PRICE')
            if new_price_obj:
                updat_price = round(float(updat_price_obj.mbf_get_value()), 2)
                new_price = round(float(new_price_obj.mbf_get_value()), 2)
                if updat_price == new_price:
                    skip = True
        
        #If the execution time of the trade is prior to 08/11/2010 then skip
        exec_time_obj = trade_obj.mbf_find_object('EXECUTION_TIME')
        if exec_time_obj:
            exec_time = exec_time_obj.mbf_get_value()
            if exec_time != '0':
                time_time = ael.date_from_string(exec_time[:10], '%Y-%m-%d')
                if time_time < ael.date_from_string('2010-11-08', '%Y-%m-%d'):
                    skip = True
            else:
                skip = True
        
    return skip

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
    return (m, s)

def modify_sender(m, s):
 
    result = (m, s)
    type_obj = m.mbf_find_object('TYPE', 'MBFE_BEGINNING')
    type_value = type_obj.mbf_get_value() 

    if type_value in ['INSERT_INSTRUMENT', 'UPDATE_INSTRUMENT']:
        result = modify_instrument_message(m, s)
    elif type_value in ['INSERT_TRADE', 'UPDATE_TRADE']:
        if trade_message_can_be_skippped(m):    
            return None
    return result
