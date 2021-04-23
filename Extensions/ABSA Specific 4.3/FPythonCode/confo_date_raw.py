import acm
from at_type_helpers import to_ael
from at_time import acm_datetime

def _get_add_info_if_exists(obj, record_type, field_name):
    query = 'fieldName="%s" recType="%s"' % (field_name, record_type)
    try:
        add_info_spec = acm.FAdditionalInfoSpec.Select01(query, '')
        query = 'recaddr=%s addInf="%s"' % (obj.Oid(), add_info_spec.Oid())
        add_info = acm.FAdditionalInfo.Select01(query, '')
        return add_info
    except Exception as e:
        ael.log(e)
    
def Confo_Date_Sent(trade, *args, **kwargs):
    add_info = _get_add_info_if_exists(trade, 'Trade', 'Confo Date Sent')
    value = None
    if add_info != None:
        add_info = to_ael(add_info)
        value = acm_datetime(add_info.value)
    return value
