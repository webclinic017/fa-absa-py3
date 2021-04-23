""" Trade_Allocation:1.2.5 """

'''---------------------------------------------------------------------------------
 MODULE
     FMessageAdaptations - Includes functions to modify messages in the AMBA.
     
     (c) Copyright 2000 by Front Capital Systems AB. All rights reserved.
 
 DESCRIPTION    
     This module should not be modified at customer site. It includes all message
     modifications defined by Front Capital Systems. This module is overwritten
     with a new version for every new release of AMBA.
     
     The module will call the FTradeAllocation module to perform trade allocation.
     
     The module will check the acquirer, and perhaps set an acquirer if necessary.
     
     The module can check so that:
     1. Currencies are not overwritten by other instruments with the same INSID.
     2. Instruments with the same insid but different isin are not overwritten. In
        this case the market name is appended to the INSID.
     3. We ensure that SWX long name are unique the short name is appended to the
        long name if needed.
     4. Instruments with the same ISIN but different INSID or CURRENCIES are not
        overwritten.
     5. Remove the message if it is a Bond that already has expired. May happen on
        on SWX.
     6. Replace incoming 00000000 in leg start_day with today's date.
     7. Replace underlying instrument as specified in InstrUploadSettings.
     8. Equity index futures are inserted to the page: hedgeChoice.
     9. CombinationLinks are created for Basis instruments traded on Xetra (EUREX BONDS).
     10. Equity index are inserted to the page: NonSplitIndexes.
     11. Equity index are inserted to the page: betaIndexChoice.
     
     The following variables in InstrUploadSettings, shall be set to "1" to have 
     the checks being performed: 
     
     check_currency
     check_insid
     check_swx_long
     check_isin
     check_der_und
     check_expired_bond
     check_start_day_leg
     create_xetra_basis_comb_link
     insert_eq_index_fut_into_hedgechoice
     insert_eq_index_into_nonsplitindexes
     insert_eq_index_into_betaindexchoice
     
     Trades in Repo instruments will generate the creation of a non-generic instrument
     if the flag: create_repo_instrument, in module TradeAllocationRule, is set to "1".

     The module will set the user to EXERCISE and ASSIGNMENT for the respective trade
     type if the flag: use_exe_ass_userid, in module TradeAllocationRule, is set to "1"
     
     Trades made in instruments of type Combination (on OM and Basis instruments
     on EurexBonds) are allocated to the portfolio: COMBINATION_TRADES, if the flag:
     allocate_combination_trades, in module TradeAllocationRule, is set to "1"
     
     The module will remove existing TickSizeIntervals when a new TickSizeList is 
     received that already exists. This is to prevent overlapping intervals.
     
 NOTE     
     The SWX long and short name used in this module must match the names used in
     the Local TTT file for SWX Instruments.
      
 REFERENCES
     Regular expressions in python:

     http://www.python.org/doc/current/lib/module-re.html
 
 ENDDESCRIPTION
---------------------------------------------------------------------------------'''
import ael
import string
import sys
import FTradeAllocation
import InstrUploadSettings
import TradeAllocationRule

# If you change the SWX long and short name you also need to update the names
# used in the TTT local file for SWX for instruments.
swx_long_name = 'SWX Long' 
swx_short_name = 'SWX Short'

check_swx_long = InstrUploadSettings.check_swx_long
check_insid = InstrUploadSettings.check_insid
check_isin = InstrUploadSettings.check_isin
check_currency = InstrUploadSettings.check_currency
check_der_und = InstrUploadSettings.check_der_und
check_expired_bond = InstrUploadSettings.check_expired_bond
check_start_day_leg = InstrUploadSettings.check_start_day_leg
create_xetra_basis_comb_link = InstrUploadSettings.create_xetra_basis_comb_link
create_repo_instrument = TradeAllocationRule.create_repo_instrument
insert_eq_index_fut_into_hedgechoice = InstrUploadSettings.insert_eq_index_fut_into_hedgechoice
insert_eq_index_into_nonsplitindexes = InstrUploadSettings.insert_eq_index_into_nonsplitindexes
insert_eq_index_into_betaindexchoice = InstrUploadSettings.insert_eq_index_into_betaindexchoice
allocate_combination_trade = TradeAllocationRule.allocate_combination_trade

def receiver_modify(m):
    message = FTradeAllocation.trade_allocation(m)

    if get_message_type(m) in ('INSERT_TRADE', \
                                'ASSIGNMENT_TRADE', \
                                'EXERCISE_TRADE'):
        message = set_acquirer(m)
        if get_message_type(m) in ('ASSIGNMENT_TRADE', 'EXERCISE_TRADE'):
             if TradeAllocationRule.use_exe_ass_userid:
                message = set_exe_ass_userid(m)
        message = divide_bond_trade_qty(m)
        if create_repo_instrument: message = check_and_set_if_repo(m)
        if allocate_combination_trade: message = alloc_comb_trade(m)

    elif get_message_type(m) == 'INSERT_INSTRUMENT':
        if check_swx_long or check_isin or check_insid \
            or check_der_und or check_expired_bond \
            or check_start_day_leg: message = check_duplicates(m)
        if check_currency and message : message = check_if_currency(m)
        if create_xetra_basis_comb_link : message = create_comb_link(m)
        if insert_eq_index_fut_into_hedgechoice : message = insert_into_hedgechoice(m)
        if insert_eq_index_into_nonsplitindexes : message = insert_into_nonsplitindexes(m)
        if insert_eq_index_into_betaindexchoice : message = insert_into_betaindexchoice(m)

    elif get_message_type(m) == 'INSERT_TICKSIZELIST':
        message = remove_tsi(m)   
       
    return message



'''----------------------------------------------------------------------------------
 FUNCTION
     get_message_type - Returns the name of the message type
     
 DESCRIPTION
     This function reads the received messages and extracts the message type and
     returns the value of the TYPE object in the message
     
 ARGUMENTS     
     m  MBFE-object  The message object received.
      
 RETURNS
     message type  String  The message type name.
         
----------------------------------------------------------------------------------'''
def get_message_type(m):
    type = m.mbf_find_object('TYPE', 'MBFE_BEGINNING')
    return type.mbf_get_value()


'''----------------------------------------------------------------------------------
 FUNCTION
     get_insaddr - Gets the instrument entity from the alias table
     
 DESCRIPTION
     Extracts the instrument address from the alias type and alias name in the
     trade message.
     
 ARGUMENTS     
     ael_string  string  The INSADDR tag value in the trade message.
      
 RETURNS
     instrument entity  object.
         
----------------------------------------------------------------------------------'''
def get_insaddr(ael_string):
    
    if sys.version[0] == '1':
        if string.find(ael_string, 'ael.InstrumentAlias.read') == -1:
            return 'None'
    else:
        if ael_string.find('ael.InstrumentAlias.read') == -1:
            return 'None'
    
    if sys.version[0] == '1':
        s = string.split(ael_string, '(')
    else:
        s = ael_string.split('(')

    if sys.version[0] == '1':
        s = string.split(s[1], ')')
    else:
        s = s[1].split(')')
    try:
        a = ael.InstrumentAlias.read('%s'%(s[0]))
    except:
        return 'None'
    if a:
        return a.insaddr
    else:
        return 'None'        
'''----------------------------------------------------------------------------------
 FUNCTION
     get_aqcuirer - Gets the name of the acquirer party of the trade.
     
 DESCRIPTION
     This function assigns the Trade acquirer party id to the Portfolio owner party
     id if it is of type 'Intern Dept'. Else the acquirer party id will be set to
     'Default Dept'.
     
 ARGUMENTS     
     m      MBFE-object         The message object received.
     s      string              Name to be set for the tag.
     tag    string              The message tag to be set.
     
 RETURNS
     m          MBFE-object  The message object received.
         
----------------------------------------------------------------------------------'''

def get_acquirer(p):
    
    aq = ael.Portfolio[p].owner_ptynbr
    if aq and aq.type == 'Intern Dept': return aq.ptyid # Return Portfolio owner
    aq = ael.Party[ael.Portfolio['DEFAULT_POOL'].owner_ptynbr.ptyid] 
    if aq : 
        if aq.type == 'Intern Dept': return aq.ptyid    # Return Default Dept
        else:
            ael.log('ERROR: %s is not of type Internal Department' % (aq.ptyid))
            return None
    return aq.ptyid     


'''----------------------------------------------------------------------------------
 FUNCTION
     set_acquirer - Sets the acquirer field to the owner of the portfolio
     
 DESCRIPTION
     This function sets the acquirer field in the trade message to the owner of
     the portfolio if this is an internal department and the acquirer field is not
     set already.
     
 ARGUMENTS     
     m  MBFE-object  The message object received.
      
 RETURNS
     m  MBFE-object  The message object.
         
----------------------------------------------------------------------------------'''
def set_acquirer(m):
    t = m.mbf_find_object('TRADE', 'MBFE_BEGINNING')

# If Acquirer of type "Intern Dept" exist then use it.
    acq = t.mbf_find_object('ACQUIRER_PTYNBR.PTYID', 'MBFE_BEGINNING')
    if acq:
        if ael.Party["%s" %(acq.mbf_get_value())].type == 'Intern Dept':
            return m
# Fetch the portfolio name    
    pf = t.mbf_find_object('PRFNBR.PRFID', 'MBFE_BEGINNING')
    if pf: pf_name = pf.mbf_get_value()
    if not pf_name:
        pf = t.mbf_find_object('ASSINF.PRFID', 'MBFE_BEGINNING')
        if pf:
            ai = pf.mbf_get_value()
            pf_name = ael.Portfolio.read('assinf='+ai).prfid

# Set the acquirer to portfolio owner, or default_aquirer
    if pf_name:
        aq_id = get_acquirer(pf_name)
        if aq_id:
            FTradeAllocation.set_tag(m, aq_id, 'ACQUIRER_PTYNBR.PTYID', 1)
    return m

'''----------------------------------------------------------------------------------
 FUNCTION
     set_exe_ass_userid - Sets the trader_usrnbr.userid field to EXERCISE and ASSIGNMENT respectively.
                          Checks if exchange trader id should be forwarded.     
     
 DESCRIPTION
     This function sets the userid field in the trade message for trades of type:
     EXERCISE_TRADE, ASSIGNMENT_TRADE to EXERCISE or ASSIGNMENT.
     It checks flag: exercise_user_field in TradeAllocationRule and puts Exchange Id in defined field.
     
 ARGUMENTS     
     m  MBFE-object  The message object received.
      
 RETURNS
     m  MBFE-object  The message object.
         
----------------------------------------------------------------------------------'''
def set_exe_ass_userid(m):
    exchange_trader = None
    
    if get_message_type(m) == 'ASSIGNMENT_TRADE':
        t = m.mbf_find_object('TRADE', 'MBFE_BEGINNING')
        if t:
            trader_obj = t.mbf_find_object('TRADER_USRNBR.USERID', 'MBFE_BEGINNING')
            if trader_obj:
                t.mbf_replace_string('TRADER_USRNBR.USERID', 'ASSIGNMENT')
            else:
                t.mbf_add_string('TRADER_USRNBR.USERID=ASSIGNMENT')
    elif get_message_type(m) == 'EXERCISE_TRADE':
        t = m.mbf_find_object('TRADE', 'MBFE_BEGINNING')
        if t: 
            trader_obj = t.mbf_find_object('TRADER_USRNBR.USERID', 'MBFE_BEGINNING')
            if trader_obj:
                exchange_trader = trader_obj.mbf_get_value()
                if exchange_trader == 'MISSING': # Hardcoded in XMBA.
                    exchange_trader = None
                t.mbf_replace_string('TRADER_USRNBR.USERID', 'EXERCISE')
            else:
                t.mbf_add_string('TRADER_USRNBR.USERID', 'EXERCISE')
            exercise_user_field = TradeAllocationRule.exercise_user_field
            if exercise_user_field:
                if exercise_user_field not in ('TEXT1', 'TEXT2'):
                    ael.log("INFORMATION: TradeAllocationRule: exercise_user_field, not valid.")
                if exercise_user_field == 'TEXT1':
                    text_obj = t.mbf_find_object('TEXT1', 'MBFE_BEGINNING')
                    if text_obj and exchange_trader:
                        t.mbf_replace_string('TEXT1', exchange_trader)
                    if not text_obj and exchange_trader:
                        t.mbf_add_string('TEXT1', exchange_trader)                        
                if exercise_user_field == 'TEXT2':
                    text_obj = t.mbf_find_object('TEXT2', 'MBFE_BEGINNING')
                    if text_obj and exchange_trader:
                        t.mbf_replace_string('TEXT2', exchange_trader)
                    if not text_obj and exchange_trader:
                        t.mbf_add_string('TEXT2', exchange_trader)
    return m


'''----------------------------------------------------------------------------------
 FUNCTION
     get_and_check_fut_code - Gets the alias of type Eurex for the future used in a 
                    Basis combination on EUREX BONDS.
     
 DESCRIPTION
     This function checks alias of type Xetra in incoming message. It translates the
     future code to Eurex future code using the dictionary xetra_basis_fut_code_dict, 
     defined in InstrUploadSettings. It checks that the future exist in ADS.     

 ARGUMENTS     
     base              string              The type of future: (FGBL etc.)
     monthyear_in      string              Future code (month/year) as sent from EUREX BONDS.
     
 RETURNS
     monthyear_out     string              Future code (yearmonth) as created in an Eurex integration.
         
----------------------------------------------------------------------------------'''
def get_and_check_fut_code(base, monthyear_in):

    monthyear_out = ''
    fut_name = ''
    ael_statement = ''
    month_in = ''
    month_out = ''
    year_in = ''
    if len(monthyear_in) == 5:
        month_in = monthyear_in[0:2]
        year_in = monthyear_in[3:]
        if month_in == '03': month_out = 'H'
        elif month_in == '06': month_out = 'M'
        elif month_in == '09': month_out = 'U'
        elif month_in == '12': month_out = 'Z'  
    
    monthyear_out = year_in + month_out
    fut_name = base + monthyear_out
    ael_statement = "ael.InstrumentAlias.read(alias='%s' and type.alias_type_name=EUREX).insaddr" % (fut_name)
    if get_insaddr(ael_statement) == 'None':        
        monthyear_out = 'Future has no valid alias (EUREX).'
        ael.log("INFORMATION: '%s'" % monthyear_out)
            
    return monthyear_out
'''----------------------------------------------------------------------------------
 FUNCTION
     check_listnode - Checks if ListNode with name list_name exist. Create it if 
     it does not exist. 
     
 DESCRIPTION
     This function returns the ListNode path to the list: list_name. If the ListNode
     does not exist, the function checks if the standard ListNode FPages exist. If Fpages 
     exist the page list_name is created under it. Else, FPages is created on top
     level and list_name under it.
     
 ARGUMENTS     
     
 RETURNS
     full_id       string               Full_id ListNode path to ListNode: hedgeChoice.
     
         
----------------------------------------------------------------------------------'''
def check_listnode(list_name):
    fpage_ln = None
    full_id = None
    find_list_ln = None

    if not list_name: return None
    
    pages = ael.ListNode.select()
    for p in pages:
        if p.id == list_name:
            find_list_ln = p
        if p.id == 'FPages':
            fpage_ln = p
    
    # Getting FULL_ID path for hedgeChoice ListNode.
    if find_list_ln:
        full_id = find_list_ln.id
        lev1 = find_list_ln.father_nodnbr
        if lev1:
            full_id = lev1.id + '/' + full_id
            lev2 = lev1.father_nodnbr
            if lev2:
                full_id = lev2.id + '/' + full_id
                lev3 = lev2.father_nodnbr
                if lev3:
                    full_id = lev3.id + '/' + full_id
                    lev4 = lev3.father_nodnbr
                    if lev4:
                        full_id = lev4.id + '/' + full_id
                 
    # Creating ListNode: list_name, under FPages.
    if not find_list_ln and fpage_ln:
        node_new = ael.ListNode.new()
        node_new.id = list_name
        node_new.father_nodnbr = fpage_ln
        node_new.terminal = 1
        node_new.page_type = 'Instruments'
        try:
            node_new.commit()
        except:
            ael.log('INFORMATION: Commit failed for ListNode, %s.' % (list_name))
            return None
        full_id = 'FPages/' + list_name
        
    # Creating FPages on top level and ListNode: list_name under it.
    if not find_list_ln and not fpage_ln:
        fpage_new = ael.ListNode.new()
        fpage_new.id = 'FPages'
        try:
            fpage_new.commit()
        except:
            ael.log('INFORMATION: Commit failed for ListNode, FPages')
            return None
        ael.poll()
        for ln in ael.ListNode.select():
            if ln.id == 'FPages':
                node_new = ael.ListNode.new()
                node_new.id = list_name
                node_new.father_nodnbr = ln
                node_new.terminal = 1
                node_new.page_type = 'Instruments'
                try:
                    node_new.commit()
                except:
                    ael.log('INFORMATION: Commit failed for ListNode, %s.' % (list_name))
                    return None
                full_id = 'FPages/' + list_name
    return full_id  
        
'''----------------------------------------------------------------------------------
 FUNCTION
     check_if_currency - Deletes the message if you try to overwrite a currency
     
 DESCRIPTION
     The function loggs an error message and deletes the message if you try
     to insert an instrument with the same name as an existing currency.
     
 ARGUMENTS     
     m  MBFE-object  The message object received.
      
 RETURNS
     message type  String  The message type name.
         
----------------------------------------------------------------------------------'''
def check_if_currency(m):

    t = m.mbf_find_object('INSTRUMENT', 'MBFE_BEGINNING')

# Delete the message if you try to Insert an instrument with the same name
# (insid) as an existing Currency.
    
    if t:
        id = t.mbf_find_object('INSID', 'MBFE_BEGINNING')
        if id:
            ins_obj = ael.Instrument["%s" %(id.mbf_get_value())]
            if ins_obj:
                if ins_obj.instype == 'Curr':
                    ael.log("INFORMATION: Error inserting instrument %s.\
                           Currency already exist." % (id.mbf_get_value()))
                    return None
    return m

'''----------------------------------------------------------------------------------
 FUNCTION
     check_duplicates - Prevents instruments from being overwritten.
     
 DESCRIPTION
     If two instruments have the same INSID but different ISIN the market name will
     be appended to the INSID.
     If two instruments have the same Alias of type LONG_NAME the SHORT_NAME alias
     will be appended to the LONG_NAME alias.     
 ARGUMENTS     
     m  MBFE-object  The message object received.
      
 RETURNS
     message MBFE-object  The message object received.
         
----------------------------------------------------------------------------------'''
def check_duplicates(m):
    alias_dict = {}
    insid = None
    isin = None
    curr = None
    source = None
    
    if check_swx_long:
        ia = m.mbf_find_object('INSTRUMENTALIAS', 'MBFE_BEGINNING')
        while ia:
            if ia.mbf_get_name() == 'INSTRUMENTALIAS':
                at = ia.mbf_find_object('TYPE.ALIAS_TYPE_NAME', 'MBFE_BEGINNING')
                io = ia.mbf_find_object('INSADDR', 'MBFE_BEGINNING')
                ins = None
                if io:
                    ins = get_insaddr(io.mbf_get_value())
                a = ia.mbf_find_object('ALIAS', 'MBFE_BEGINNING')
                alias_dict[at.mbf_get_value()] = [a.mbf_get_value(), ia, ins]
            ia = m.mbf_next_object()
    i = m.mbf_find_object('INSTRUMENT', 'MBFE_BEGINNING')
    if i:
        insid_obj = i.mbf_find_object('INSID', 'MBFE_BEGINNING')
        if insid_obj: insid = insid_obj.mbf_get_value()
        isin_obj = i.mbf_find_object('ISIN', 'MBFE_BEGINNING')
        if isin_obj: isin = isin_obj.mbf_get_value()
        curr_obj = i.mbf_find_object('CURR.INSID', 'MBFE_BEGINNING')
        if curr_obj: curr = curr_obj.mbf_get_value()
        pd = m.mbf_find_object('PRICEDEFINITION', 'MBFE_BEGINNING')
        orderb_obj = m.mbf_find_object('ORDERBOOK', 'MBFE_BEGINNING')
        if pd:
            source_obj = pd.mbf_find_object('SOURCE_PTYNBR.PTYID', 'MBFE_BEGINNING')
            source = source_obj.mbf_get_value()
        if not pd and orderb_obj:
            source_obj = orderb_obj.mbf_find_object('MARKET_PTYNBR.PTYID', 'MBFE_BEGINNING') # Only found in AMB 3.4.2 and higher
            if source_obj:
                source = source_obj.mbf_get_value()
                if not source:
                    source = 'IM' # Source must be set.
        if check_swx_long:
            ia = i.mbf_find_object('INSTRUMENTALIAS', 'MBFE_BEGINNING')
            while ia:
                if ia.mbf_get_name() == 'INSTRUMENTALIAS':
                    at = ia.mbf_find_object('TYPE.ALIAS_TYPE_NAME', 'MBFE_BEGINNING')
                    io = ia.mbf_find_object('INSADDR', 'MBFE_BEGINNING')
                    ins = None
                    if io:
                        ins = get_insaddr(io.mbf_get_value())
                    a = ia.mbf_find_object('ALIAS', 'MBFE_BEGINNING')
                    alias_dict[at.mbf_get_value()] = [a.mbf_get_value(), ia, ins]
                ia = i.mbf_next_object()

    # Same INSID but different ISIN, append market name to INSID.
    if check_insid and insid and isin:
        ins_obj = ael.Instrument[insid]
        if ins_obj and ins_obj.isin != isin:
            new_name = insid+'/'+source
            ins_obj = ael.Instrument[new_name]
            if ins_obj and ins_obj.isin != isin:
                ael.log("ERROR: Both %s and %s exist with other isin than %s." %\
                       (insid, new_name, isin))
                return None
            ia = i.mbf_find_object('INSID', 'MBFE_BEGINNING')       
            i.mbf_replace_string('INSID', new_name)
            insid = new_name
            ael.log("INFORMATION: INSID changed to %s" % (new_name))

    # If same long name append short name to long name
    if check_swx_long and (swx_long_name in alias_dict.keys()):
        cmd = "alias='"+alias_dict[swx_long_name ][0] + \
              "' and type.alias_type_name='%s'" % (swx_long_name)
        ins_alias = ael.InstrumentAlias.read(cmd)
        if ins_alias:
           if ins_alias.insaddr is not alias_dict[swx_long_name ][2]:
                new_name = alias_dict[swx_long_name][0] + '/' + alias_dict[swx_short_name][0]
                alias_dict[swx_long_name ][1].mbf_replace_string('ALIAS', '%s'%(new_name))                                  
                ael.log("INFORMATION: ALIAS for %s changed to %s" % (swx_long_name, new_name))
                                
    # Same ISIN but different INSID or CURRENCY, log and delete message.
    if check_isin and insid and isin and curr:
        ins_obj = ael.Instrument.read('ISIN='+isin)
        if ins_obj and ins_obj.isin == isin and (ins_obj.curr.insid != curr or ins_obj.insid != insid):
            i = m.mbf_find_object('INSTRUMENT', 'MBFE_BEGINNING')
            m.mbf_remove_object()
            ael.log("INFORMATION: Instrument %s already exists, instrument object removed" % (isin))

    # If the bond already has expired, delete the instrument message.
    if check_expired_bond:
        i = m.mbf_find_object('INSTRUMENT', 'MBFE_BEGINNING')
        if i:
            l = i.mbf_find_object('LEG', 'MBFE_CURRENT')
            if l:
                insid_obj = i.mbf_find_object('INSID', 'MBFE_BEGINNING')
                maturity_obj = l.mbf_find_object('END_DAY', 'MBFE_BEGINNING')
                if maturity_obj and insid_obj: 
                    insid = insid_obj.mbf_get_value()
                    maturity = maturity_obj.mbf_get_value()
                    date = ael.date_from_string(maturity)               
                    today = ael.date_today()
                    if today > date:
                        ael.log("INFORMATION: maturity date for insid %s is %s assumed to be expired, message suppressed." % (insid, date))
                        return None

    # If START_DAY = 00000000, then START_DAY=TODAY.
    if check_start_day_leg:
        i = m.mbf_find_object('INSTRUMENT', 'MBFE_BEGINNING')
        if i:
            l = i.mbf_find_object('LEG', 'MBFE_CURRENT')
            if l:
                insid_obj = i.mbf_find_object('INSID', 'MBFE_BEGINNING')
                start_obj = l.mbf_find_object('START_DAY', 'MBFE_BEGINNING')
                if start_obj and insid_obj: 
                    ins_id = insid_obj.mbf_get_value()
                    start = start_obj.mbf_get_value()
                    today = ael.date_today()
                    if start == '00000000':
                        ael.log("INFORMATION: START_DAY for insid %s is 00000000, START_DAY replaced to %s." % (ins_id, today))
                        l.mbf_replace_string('START_DAY', '%s' % (today))

    # If new ISIN specified, map UND_INSADDR.ISIN. 
    if check_der_und:
        und_isin = None
        i = m.mbf_find_object('INSTRUMENT', 'MBFE_BEGINNING')
        if i:    
            und_isin_obj=i.mbf_find_object('UND_INSADDR.ISIN', 'MBFE_BEGINNING')
            if und_isin_obj:
                und_isin = und_isin_obj.mbf_get_value()
                if und_isin:
                    und_isin_dict = InstrUploadSettings.map_underlying_isin_dict
                    if und_isin_dict.has_key(und_isin):
                        new_und_isin = und_isin_dict.get(und_isin)
                        i.mbf_replace_string('UND_INSADDR.ISIN', new_und_isin)

    return m
'''----------------------------------------------------------------------------------
 FUNCTION
     create_comb_link - Creates CombinationLinks for Basis instruments tradable on Xetra.
     
 DESCRIPTION
     
 ARGUMENTS     
     m  MBFE-object  The message object received.
      
 RETURNS
     message MBFE-object  The message object received.
         
----------------------------------------------------------------------------------'''
def create_comb_link(m):
    i = m.mbf_find_object('INSTRUMENT', 'MBFE_BEGINNING')
    insid = None
    isin = None
    instype = None
    list = None
    und_isin = None
    alias_basis = None
    basis_list_name = 'BASE BASIS INSTRUMENTS'
    
    if i:
        instype_obj = i.mbf_find_object('INSTYPE', 'MBFE_BEGINNING')
        if instype_obj: instype = instype_obj.mbf_get_value()
        if instype == 'INS_COMBINATION':
            l = m.mbf_find_object('LISTLEAF', 'MBFE_BEGINNING')
            if l:
                list_obj = l.mbf_find_object('NODNBR.FULL_ID', 'MBFE_BEGINNING')
                if list_obj: list = list_obj.mbf_get_value()
                if not list.find(basis_list_name) == -1:
                    ac = m.mbf_find_object('INSTRUMENTALIAS', 'MBFE_BEGINNING')
                    if ac:
                        while ac.mbf_get_value() == 'INSTRUMENTALIAS':
                            ac_obj = ac.mbf_find_object('TYPE.ALIAS_TYPE_NAME', 'MBFE_BEGINNING')
                            if ac_obj:
                                act = ac_obj.mbf_get_value()
                                if act == 'Xetra':
                                    ac_ai_obj = ac.mbf_find_object('ALIAS', 'MBFE_BEGINNING')
                                    if ac_ai_obj:
                                        alias_basis = ac_ai_obj.mbf_get_value()
                                        break
                            ac = m.mbf_next_object()

                    isin_obj = i.mbf_find_object('ISIN', 'MBFE_BEGINNING')
                    if isin_obj: isin = isin_obj.mbf_get_value()
                    und_isin_obj = i.mbf_find_object('UND_INSADDR.ISIN', 'MBFE_BEGINNING')
                    if und_isin_obj: und_isin = und_isin_obj.mbf_get_value()
            
                    if alias_basis and isin and list and und_isin:
                        insid_new = ''
                        memb_isin = ''
                        month_year = get_and_check_fut_code(alias_basis[0:4], alias_basis[4:9])
                        if not month_year[0:3] == 'Fut':
                            insid_new = alias_basis[0:4] + month_year
                            memb_isin = und_isin
                            # Creating first link
                            comb_link_obj_1 = m.mbf_start_list("COMBINATIONLINK")
                            comb_link_obj_1.mbf_add_string( "OWNER_INSADDR.ISIN", "%s" % (isin))
                            comb_link_obj_1.mbf_add_string( "MEMBER_INSADDR.INSID", "%s" % (insid_new))
                            comb_link_obj_1.mbf_add_string( "WEIGHT", "-10")
                            comb_link_obj_1 = m.mbf_end_list()  
                            # Creating 2nd link
                            comb_link_obj_2 = m.mbf_start_list("COMBINATIONLINK")
                            comb_link_obj_2.mbf_add_string( "OWNER_INSADDR.ISIN", "%s" % (isin))
                            comb_link_obj_2.mbf_add_string( "MEMBER_INSADDR.ISIN", "%s" % (memb_isin))
                            comb_link_obj_2.mbf_add_string( "WEIGHT", "1")
                            comb_link_obj_2 = m.mbf_end_list()
                        
                        # Removing the: UND_INSADDR.ISIN, line
                        rem_obj = i.mbf_find_object('UND_INSADDR.ISIN', 'MBFE_BEGINNING')
                        if rem_obj: i.mbf_remove_object()

    return m
'''----------------------------------------------------------------------------------
 FUNCTION
     insert_into_hedgechoice - Inserts EquityIndexFutures into page: hedgeChoice.
     
 DESCRIPTION
     This function checks if the instrument type is Future. If so, it checks if the underlying
     instrument type is EquityIndex.
     The function checks if the list: hedgeChoice exist. If it doesn't it checks if the list:
     FPages exist. If neither FPages nor hedgeChoice exist, then both are created as FPages/hedgeChoice. 
 ARGUMENTS     
     m  MBFE-object  The message object received.
      
 RETURNS
     message MBFE-object  The message object received.
         
----------------------------------------------------------------------------------'''
def insert_into_hedgechoice(m):
    insaddr_isin = 0
    full_id = None
    i = m.mbf_find_object('INSTRUMENT', 'MBFE_BEGINNING')
    if i:
        type_obj = i.mbf_find_object('INSTYPE', 'MBFE_BEGINNING')
        if type_obj:
            if type_obj.mbf_get_value() == 'INS_FUTURE':
                und_ins_obj = i.mbf_find_object('UND_INSADDR.ISIN', 'MBFE_BEGINNING')
                if und_ins_obj:
                    und_isin = und_ins_obj.mbf_get_value()
                    und_ins = ael.Instrument.read('ISIN=%s' % und_isin)
                    if und_ins:
                        if und_ins.instype == 'EquityIndex':
                            leaf_obj = m.mbf_find_object('LISTLEAF', 'MBFE_BEGINNING')
                            if leaf_obj:
                                leaf_insaddr_obj = leaf_obj.mbf_find_object('INSADDR', 'MBFE_BEGINNING')
                                if not leaf_insaddr_obj:
                                    leaf_insaddr_obj = leaf_obj.mbf_find_object('INSADDR.ISIN', 'MBFE_BEGINNING')
                                    insaddr_isin=1
                                if leaf_insaddr_obj:
                                    # Check if possible to find/create path to FPages/hedgeChoice
                                    full_id = check_listnode('hedgeChoice')
                                    if full_id:
                                        # Add ListLeaf
                                        leaf_insaddr = leaf_insaddr_obj.mbf_get_value()
                                        list_leaf_obj = m.mbf_start_list("LISTLEAF")
                                        if insaddr_isin:
                                            list_leaf_obj.mbf_add_string( "INSADDR.ISIN", "%s" % (leaf_insaddr))
                                        else:
                                            list_leaf_obj.mbf_add_string( "INSADDR", "%s" % (leaf_insaddr))
                                        list_leaf_obj.mbf_add_string( "NODNBR.FULL_ID", "%s" % (full_id))
                                        list_leaf_obj = m.mbf_end_list()
    return m

'''----------------------------------------------------------------------------------
 FUNCTION
     insert_into_nonsplitindexes - Inserts EquityIndex into page: NonSplitIndexes.
     
 DESCRIPTION
     This function checks if the instrument type is EquityIndex. 
     The function checks if the list: NonSplitIndexes exist. If it doesn't it checks if the list:
     FPages exist. If neither FPages nor NonSplitIndexes exist, then both are created as FPages/NonSplitIndexes. 
 ARGUMENTS     
     m  MBFE-object  The message object received.
      
 RETURNS
     message MBFE-object  The message object received.
         
----------------------------------------------------------------------------------'''
def insert_into_nonsplitindexes(m):
    insaddr_isin = 0
    full_id = None
    i = m.mbf_find_object('INSTRUMENT', 'MBFE_BEGINNING')
    if i:
        type_obj = i.mbf_find_object('INSTYPE', 'MBFE_BEGINNING')
        if type_obj:
            if type_obj.mbf_get_value() == 'INS_EQUITY_INDEX':
                leaf_obj = m.mbf_find_object('LISTLEAF', 'MBFE_BEGINNING')
                if leaf_obj:
                    leaf_insaddr_obj = leaf_obj.mbf_find_object('INSADDR.ISIN', 'MBFE_BEGINNING')
                    if leaf_insaddr_obj:
                        # Check if possible to find/create path to FPages/NonSplitIndexes
                        full_id = check_listnode('NonSplitIndexes')
                        if full_id:
                            # Add ListLeaf
                            leaf_insaddr = leaf_insaddr_obj.mbf_get_value()
                            list_leaf_obj = m.mbf_start_list("LISTLEAF")
                            list_leaf_obj.mbf_add_string( "INSADDR.ISIN", "%s" % (leaf_insaddr))
                            list_leaf_obj.mbf_add_string( "NODNBR.FULL_ID", "%s" % (full_id))
                            list_leaf_obj = m.mbf_end_list()
    return m

'''----------------------------------------------------------------------------------
 FUNCTION
     insert_into_betaindexchoice - Inserts EquityIndex into page: betaIndexChoice.
     
 DESCRIPTION
     This function checks if the instrument type is EquityIndex. 
     The function checks if the list: betaIndexChoice exist. If it doesn't it checks if the list:
     FPages exist. If neither FPages nor betaIndexChoice exist, then both are created as FPages/NonSplitIndexes. 
 ARGUMENTS     
     m  MBFE-object  The message object received.
      
 RETURNS
     message MBFE-object  The message object received.
         
----------------------------------------------------------------------------------'''
def insert_into_betaindexchoice(m):
    insaddr_isin = 0
    full_id = None
    i = m.mbf_find_object('INSTRUMENT', 'MBFE_BEGINNING')
    if i:
        type_obj = i.mbf_find_object('INSTYPE', 'MBFE_BEGINNING')
        if type_obj:
            if type_obj.mbf_get_value() == 'INS_EQUITY_INDEX':
                leaf_obj = m.mbf_find_object('LISTLEAF', 'MBFE_BEGINNING')
                if leaf_obj:
                    leaf_insaddr_obj = leaf_obj.mbf_find_object('INSADDR.ISIN', 'MBFE_BEGINNING')
                    # Check if possible to find/create path to FPages/betaIndexChoice
                    full_id = check_listnode('betaIndexChoice')
                    if full_id:
                        if leaf_insaddr_obj:
                            # Add ListLeaf
                            leaf_insaddr = leaf_insaddr_obj.mbf_get_value()
                            list_leaf_obj = m.mbf_start_list("LISTLEAF")
                            list_leaf_obj.mbf_add_string( "INSADDR.ISIN", "%s" % (leaf_insaddr))
                            list_leaf_obj.mbf_add_string( "NODNBR.FULL_ID", "%s" % (full_id))
                            list_leaf_obj = m.mbf_end_list()
    return m

'''----------------------------------------------------------------------------------
 FUNCTION
     remove_tsi - Prevents overlapping tick size intervals.
     
 DESCRIPTION
     When a new Tick Size List is received that already exists, the intervals of that
     list are removed to prevend overlapping intervals.
 ARGUMENTS     
     m  MBFE-object  The message object received.
      
 RETURNS
     message MBFE-object  The message object received.
         
----------------------------------------------------------------------------------'''
def remove_tsi(m):
    tsl_obj = None   

    tsl_obj = m.mbf_find_object('TICKSIZELIST', 'MBFT_BEGINNING')    
    tsl_name_obj = tsl_obj.mbf_find_object('NAME', 'MBFT_BEGINNING')
    if tsl_name_obj:
        tsl_name= tsl_name_obj.mbf_get_value()
    else:
        ael.log("ERROR: NAME object missing in TICKSIZELIST message")
        return m
    if tsl_name:
        tsl = ael.TickSizeList[tsl_name]
        if tsl:
            tsl_clone = tsl.clone()
            tsi = tsl_clone.intervals()
            for i in tsi:
                i.delete()
            try:
                tsl_clone.commit() 
            except:
                ael.log('INFORMATION: Commit failed for TickSizeList, %s. Verify TickSizeIntervals.' % (tsl_name))
        else:
            return m
    else: 
        ael.log("ERROR: NAME object empty in TICKSIZELIST message")
        return m

'''----------------------------------------------------------------------------------
 FUNCTION
     divide_bond_trade_qty - Divide trade qty for leg-instruments with ContractSize.
     
 DESCRIPTION
     For instruments of types: Zero, Bill, Convertible, Bond, IndexLinkedBond,
     FRN and DualCurrencyBond, the Nominal is set to the RoundLot on the exchange.
     
 ARGUMENTS     
     m  MBFE-object  The message object received.
      
 RETURNS
     message MBFE-object  The message object received.
         
----------------------------------------------------------------------------------'''
def divide_bond_trade_qty(m):
    t = m.mbf_find_object('TRADE', 'MBFE_BEGINNING')
    leg_types = ['Repo', 'Zero', 'Bill', 'Convertible', 'Bond', 'IndexLinkedBond', 'FRN', 'DualCurrencyBond']
    got_ins = None
    ins = None
    leg_ins = None
    if t:
        ins_obj = t.mbf_find_object('INSADDR', 'MBFE_BEGINNING')
        ins_obj_isin = t.mbf_find_object('INSADDR.ISIN', 'MBFE_BEGINNING')
        if ins_obj:
            ins = FTradeAllocation.get_instrument_from_order_book_string(ins_obj.mbf_get_value(), 0)
            if ins:
                got_ins = 1
        if ins_obj_isin and not ins_obj:
            ins_isin = ins_obj_isin.mbf_get_value()
            if ins_isin:
                ins = ael.Instrument.read('ISIN=%s' % ins_isin)
                if ins: got_ins = 1
                    
        if got_ins:
            if ins.instype in leg_types:
                csize = ins.contr_size
                quant_obj = t.mbf_find_object('QUANTITY', 'MBFE_BEGINNING')
                if quant_obj:
                    quant_in = quant_obj.mbf_get_value()
                    quant_out = float(quant_in)/csize
                    t.mbf_replace_string('QUANTITY', str(quant_out))                   
            
    return(m)
    
'''----------------------------------------------------------------------------------
 FUNCTION
     alloc_comb_trade - Allocate trades received in standard combination instrument
                        where trades in the legs are also received to a portfolio
                        called COMBINATION_TRADES.
     
 DESCRIPTION
     Trades made in instruments of type Combination (on OM and Basis instruments
     on EurexBonds) are allocated to the portfolio: COMBINATION_TRADES, if the flag:
     allocate_combination_trades, in module TradeAllocationRule, is set to "1"
     
 ARGUMENTS     
     m  MBFE-object  The message object received.
      
 RETURNS
     message MBFE-object  The message object received.

----------------------------------------------------------------------------------'''
def alloc_comb_trade(m):
    ads_ordrno = None
    comb_ins = None
    mess_ins = None
    t_ins = None
    t_ins2 = None
    market = None
    do_allocate = None
        
    t = m.mbf_find_object('TRADE', 'MBFE_BEGINNING')
    if t:
        mess_ordrno_obj = t.mbf_find_object('ORDNBR', 'MBFE_BEGINNING')
        ins_obj = t.mbf_find_object('INSADDR', 'MBFE_BEGINNING')
        if ins_obj:
            t_ins = ins_obj.mbf_get_value()
        if not ins_obj:
            ins_obj2 = t.mbf_find_object('INSADDR.ISIN', 'MBFE_BEGINNING')
            if ins_obj2:
                t_ins2 = ins_obj2.mbf_get_value()
        market_obj = t.mbf_find_object('MARKET_PTYNBR.PTYID', 'MBFE_BEGINNING')
        if market_obj:
            market = market_obj.mbf_get_value()
        if t_ins:
            mess_ins = FTradeAllocation.get_instrument_from_order_book_string(t_ins, 0)
        if t_ins2:
            try:
                mess_ins = ael.Instrument.read('isin = "%s"' % t_ins2)
            except:
                mess_ins = None
        if mess_ins:
            if mess_ins.instype == 'Combination':
                # Check if Combination Category is Basis
                if mess_ins.category_chlnbr:
                    if mess_ins.category_chlnbr.entry == 'Basis':
                        do_allocate = 1
                if market == 'OM':
                    do_allocate = 1
        # Workaround for SPR 231193
        if mess_ordrno_obj:
            mess_ordrno = mess_ordrno_obj.mbf_get_value()
            if mess_ordrno:
                ads_ordrno = ael.OwnOrder.read('ordnbr="%s"' % mess_ordrno)
        if ads_ordrno:
            if ads_ordrno.insaddr.instype:
                if ads_ordrno.insaddr.instype == 'Combination':
                    comb_ins = ads_ordrno.insaddr
                    if comb_ins != mess_ins:
                       ordrno_obj = t.mbf_find_object('ORDNBR', 'MBFE_BEGINNING')
                       t.mbf_remove_object()
                       ael.log("INFORMATION: ORDNBR row removed.")
        # End workaround SPR 231193               
        if do_allocate:
            prf_obj = t.mbf_find_object('PRFNBR.PRFID', 'MBFE_BEGINNING')
            if prf_obj:
                t.mbf_replace_string('PRFNBR.PRFID', 'COMBINATION_TRADES')
    return m


'''----------------------------------------------------------------------------------
 FUNCTION
     check_and_set_if_repo - Creates non generic repo instrument.
     
 DESCRIPTION
     Fredrik
 ARGUMENTS     
     m  MBFE-object  The message object received.
      
 RETURNS
     message MBFE-object  The message object received.
         
----------------------------------------------------------------------------------'''

def adjust_date(date, period, calendar, pay_day_method):
    return date.add_period(period).adjust_to_banking_day(calendar, pay_day_method)

def check_and_set_if_repo(m):
    trade_obj = m.mbf_find_object('TRADE', 'MBFE_BEGINNING')
    if(not trade_obj):
        return m

    ins_obj = trade_obj.mbf_find_object('INSADDR', 'MBFE_BEGINNING')
    if(not ins_obj):
        return m

    ins = FTradeAllocation.get_instrument_from_order_book_string(ins_obj.mbf_get_value())

    if(not ins or not ins.generic or ins.instype <> 'Repo/Reverse'):
        return m

    clone_ins = ins.clone()
    clone_ins.generic = 0
    clone_ins.extern_id1 = ''
    clone_ins.extern_id2 = ''
    clone_ins.isin = ''
    
    # clone first and only leg
    leg = clone_ins.legs()[0]
    # Calculate start date
    leg.start_day = adjust_date(ins.spot_date(), leg.start_period, leg.pay_calnbr, leg.pay_day_method)
    # Calculate end date
    leg.end_day = adjust_date(leg.start_day, leg.end_period, leg.pay_calnbr, leg.pay_day_method)
    # Always set expiry_date in instrument
    clone_ins.exp_day = leg.end_day

    # Find a name only from instrument record information
    clone_ins.insid = 'Repo ' + str(leg.start_day) + ' ' + str(leg.end_day)
    
    # Set trade price as fixed rate in leg
    if(ins.quote_type == 'Coupon'):
        clone_ins.quote_type = 'Clean'
        price = trade_obj.mbf_find_object('PRICE', 'MBFE_BEGINNING')
        leg.fixed_rate = float(price.mbf_get_value())
    
    # Commit 
    clone_ins.commit()
    ael.poll()
    # Commit end
    
    # Change trade insaddr to insaddr.insid = ...
    ins_obj = trade_obj.mbf_find_object('INSADDR', 'MBFE_BEGINNING')
    if ins_obj:
        ins_obj = trade_obj.mbf_find_object('INSADDR', 'MBFE_BEGINNING')
        trade_obj.mbf_remove_object()
        trade_obj.mbf_add_string('INSADDR.INSID', clone_ins.insid)

    return m
