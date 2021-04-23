import acm
from FRoutingCommon import SOURCE_PORTFOLIO, is_member_of_or_same_as
'''================================================================================================
================================================================================================'''
def get_value(m, object):
    node = m.mbf_find_object(object)
    return node.mbf_get_value() if node != None else None
'''================================================================================================
================================================================================================'''
def sender_modify(m, s):
    source = get_value(m, 'SOURCE')
    type = get_value(m, 'TYPE')
    if type == 'UPDATE_TRADE' or type == 'INSERT_TRADE':
        trade = m.mbf_find_object('TRADE', 'MBFE_BEGINNING')
        port = get_value(trade, 'PRFNBR.PRFID')
        if is_member_of_or_same_as(acm.FPhysicalPortfolio[port], SOURCE_PORTFOLIO):
            print '@' * 100
            print m.mbf_object_to_string_xml()
            print '@' * 100
            return (m, s)
'''================================================================================================
================================================================================================'''
