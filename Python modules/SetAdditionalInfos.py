import acm

trade_key = '0'

def _set_add_info(field_name, recaddr, field_value):
    ''''Set additional info entry field_name for object recaddr to
    field_value, regardless of whether it was already set or not.
    '''
    ai_spec = acm.FAdditionalInfoSpec.Select01(
        'fieldName = "%s"' % field_name, '')
    add_info = acm.FAdditionalInfo.Select01(
        'recaddr = %s addInf = %s' % (
            recaddr, ai_spec.Oid()),
        '')
    if not add_info:
        add_info = acm.FAdditionalInfo()
        add_info.AddInf(ai_spec)
        add_info.Recaddr(recaddr)
    add_info.FieldValue(field_value)
    add_info.Commit()    
    
def _delete_add_info(field_name, recaddr):
    ''''delete additional info object
    '''
    ai_spec = acm.FAdditionalInfoSpec.Select01(
        'fieldName = "%s"' % field_name, '')
    add_info = acm.FAdditionalInfo.Select01(
        'recaddr = %s addInf = %s' % (
            recaddr, ai_spec.Oid()),
        '')
    if add_info:
        add_info.Delete()        
    
    
    
ael_variables = [[trade_key, 'Trades Selection', 'string', None,
        'G1_MirrorTrades', 0, 1, 'Global One trade selection.', None, 1]]

def ael_main(parameters): 
    print parameters[trade_key][0]
    trades = acm.FTradeSelection[parameters[trade_key][0]]    
            
    for trade in trades.Trades():
        try:
        
            if trade.AdditionalInfo().SL_G1Counterparty1() == None or trade.AdditionalInfo().SL_G1Counterparty2() == None or trade.AdditionalInfo().SL_G1Fee2() == None:
                continue
            else:
                if trade.Status() not in ['Void', 'Simulated']:
                    print 'Trade Number', trade.Oid(), trade.AdditionalInfo().SL_G1Counterparty1(), trade.AdditionalInfo().SL_G1Counterparty2(), trade.AdditionalInfo().SL_G1Fee2(), trade.Instrument().OpenEnd()
                    _delete_add_info('SL_G1Counterparty1', trade.Oid())
                    _delete_add_info('SL_G1Counterparty2', trade.Oid())
                    print 'Trade Number', trade.Oid(), ' Add Info deleted..'
                
        except Exception, ex:
            print 'Exception', trade.Oid()
